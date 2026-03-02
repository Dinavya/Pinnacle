from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from models import db, Resume, JobRecommendation
from skills import extract_skills_from_text, get_skill_recommendations, JOB_ROLES
import pdfplumber
import json
import os
from datetime import datetime
from io import BytesIO, StringIO
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.secret_key = 'your-secret-key-change-in-production'

db.init_app(app)

# Add custom Jinja2 filter for JSON parsing
@app.template_filter('from_json')
def from_json(json_string):
    """Parse JSON string in templates"""
    try:
        return json.loads(json_string) if json_string else []
    except:
        return []

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ==================== Database Initialization ====================
with app.app_context():
    db.create_all()

# ==================== Helper Functions ====================

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def extract_email(text):
    """Extract email from text"""
    import re
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else ""

def extract_phone(text):
    """Extract phone number from text"""
    import re
    phone_pattern = r'(\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})'
    matches = re.findall(phone_pattern, text)
    return ''.join(matches[0]) if matches else ""

def extract_name(text):
    """Extract name from text (usually first line or first meaningful text)"""
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line and len(line.split()) >= 2 and len(line) < 50:
            return line
    return "Unknown"

def parse_resume(pdf_path):
    """Parse resume and extract information"""
    text = extract_text_from_pdf(pdf_path)
    
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills_from_text(text)
    
    # Calculate score based on skills and information completeness
    score = len(skills) * 10
    if email: score += 10
    if phone: score += 5
    
    return {
        'name': name,
        'email': email,
        'phone': phone,
        'skills': skills,
        'raw_text': text,
        'score': min(score, 100)
    }

def calculate_leaderboard_score(resume):
    """Calculate score for leaderboard ranking"""
    from skills import PRIORITY_SKILLS
    skills = resume.get_skills_list()
    base_score = len(skills) * 10
    
    # Bonus for priority skills
    priority_bonus = 0
    for skill in skills:
        if skill in PRIORITY_SKILLS:
            priority_bonus += 15
    
    return min(base_score + priority_bonus, 100)

# ==================== Routes ====================

@app.route('/')
def index():
    """Home page"""
    total_resumes = Resume.query.count()
    return render_template('index.html', total_resumes=total_resumes)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload resume"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if not file.filename.endswith('.pdf'):
            flash('Please upload a PDF file', 'error')
            return redirect(request.url)
        
        try:
            # Save file
            filename = f"{datetime.now().timestamp()}_{file.filename}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # Parse resume
            parsed_data = parse_resume(file_path)
            
            # Save to database
            resume = Resume(
                name=parsed_data['name'],
                email=parsed_data['email'],
                phone=parsed_data['phone'],
                file_path=file_path,
                score=parsed_data['score']
            )
            resume.set_skills_list(parsed_data['skills'])
            
            db.session.add(resume)
            db.session.commit()
            
            # Generate skill recommendations
            skill_recommendations = get_skill_recommendations(parsed_data['skills'])
            for rec in skill_recommendations[:5]:  # Top 5 skill recommendations
                job_rec = JobRecommendation(
                    resume_id=resume.id,
                    job_title=rec['skill_name'],  # Store skill name as job_title
                    match_score=rec['value'],  # Store priority value
                    required_skills=json.dumps(rec['job_titles']),  # Jobs requiring this skill
                    missing_skills=json.dumps([]),  # Not used for skills
                    learning_suggestions=json.dumps(rec['learning_resource'])
                )
                db.session.add(job_rec)
            
            db.session.commit()
            
            flash('Resume uploaded successfully!', 'success')
            return redirect(url_for('view_resume', resume_id=resume.id))
            
        except Exception as e:
            flash(f'Error processing resume: {str(e)}', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/resume/<int:resume_id>')
def view_resume(resume_id):
    """View resume details"""
    resume = Resume.query.get_or_404(resume_id)
    jobs = JobRecommendation.query.filter_by(resume_id=resume_id).all()
    
    return render_template('resume_detail.html', resume=resume, jobs=jobs)

@app.route('/download/<int:resume_id>/<format>')
def download_resume(resume_id, format):
    """Download resume data"""
    resume = Resume.query.get_or_404(resume_id)
    
    if format == 'json':
        data = {
            'name': resume.name,
            'email': resume.email,
            'phone': resume.phone,
            'skills': resume.get_skills_list(),
            'uploaded_at': resume.uploaded_at.isoformat()
        }
        return jsonify(data)
    
    elif format == 'csv':
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Field', 'Value'])
        writer.writerow(['Name', resume.name])
        writer.writerow(['Email', resume.email])
        writer.writerow(['Phone', resume.phone])
        writer.writerow(['Skills', ', '.join(resume.get_skills_list())])
        writer.writerow(['Score', resume.score])
        
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', 
                        as_attachment=True, 
                        download_name=f'{resume.name}_resume.csv')
    
    return jsonify({'error': 'Invalid format'}), 400

@app.route('/resume/<int:resume_id>/delete', methods=['POST'])
def delete_resume(resume_id):
    """Delete a resume"""
    resume = Resume.query.get_or_404(resume_id)
    
    try:
        # Delete the file
        if resume.file_path and os.path.exists(resume.file_path):
            os.remove(resume.file_path)
        
        # Delete associated job recommendations
        JobRecommendation.query.filter_by(resume_id=resume_id).delete()
        
        # Delete the resume from database
        db.session.delete(resume)
        db.session.commit()
        
        flash('Resume deleted successfully!', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting resume: {str(e)}', 'error')
        return redirect(url_for('view_resume', resume_id=resume_id))

@app.route('/dashboard')
def dashboard():
    """Dashboard with analytics"""
    total_resumes = Resume.query.count()
    
    # Get all skills
    all_resumes = Resume.query.all()
    skills_count = {}
    for resume in all_resumes:
        for skill in resume.get_skills_list():
            skills_count[skill] = skills_count.get(skill, 0) + 1
    
    # Sort by count
    top_skills = sorted(skills_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return render_template('dashboard.html', 
                         total_resumes=total_resumes,
                         top_skills=top_skills)

@app.route('/leaderboard')
def leaderboard():
    """Skills leaderboard"""
    resumes = Resume.query.all()
    
    # Calculate scores
    leaderboard_data = []
    for resume in resumes:
        score = calculate_leaderboard_score(resume)
        leaderboard_data.append({
            'name': resume.name,
            'email': resume.email,
            'skills': ', '.join(resume.get_skills_list()),
            'skill_count': len(resume.get_skills_list()),
            'score': score
        })
    
    # Sort by score
    leaderboard_data = sorted(leaderboard_data, key=lambda x: x['score'], reverse=True)
    
    return render_template('leaderboard.html', leaderboard=leaderboard_data)

@app.route('/jobs')
def jobs():
    """Skill recommendations"""
    all_skills = []
    resumes = Resume.query.all()
    
    if not resumes:
        return render_template('jobs.html', recommendations=[], empty_state=True)
    
    for resume in resumes:
        skill_recommendations = get_skill_recommendations(resume.get_skills_list())
        for rec in skill_recommendations:
            all_skills.append({
                'resume_id': resume.id,
                'candidate': resume.name,
                'email': resume.email,
                'skill_name': rec['skill_name'],
                'priority_score': rec['value'],
                'jobs_requiring': rec['jobs_requiring'],
                'job_titles': rec['job_titles'],
                'learning_resource': rec['learning_resource']
            })
    
    # Sort by priority score
    all_skills = sorted(all_skills, key=lambda x: x['priority_score'], reverse=True)
    
    return render_template('skill.html', recommendations=all_skills, empty_state=False, is_skills=True)

@app.route('/regenerate-recommendations', methods=['POST'])
def regenerate_recommendations():
    """Regenerate skill recommendations for all resumes"""
    try:
        resumes = Resume.query.all()
        count = 0
        
        for resume in resumes:
            # Delete existing recommendations
            JobRecommendation.query.filter_by(resume_id=resume.id).delete()
            
            # Generate new skill recommendations
            skill_recommendations = get_skill_recommendations(resume.get_skills_list())
            for rec in skill_recommendations[:5]:  # Top 5
                job_rec = JobRecommendation(
                    resume_id=resume.id,
                    job_title=rec['skill_name'],  # Store skill name
                    match_score=rec['value'],  # Priority value
                    required_skills=json.dumps(rec['job_titles']),  # Jobs requiring this skill
                    missing_skills=json.dumps([]),
                    learning_suggestions=json.dumps(rec['learning_resource'])
                )
                db.session.add(job_rec)
            count += 1
        
        db.session.commit()
        flash(f'Regenerated skill recommendations for {count} resumes!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error regenerating recommendations: {str(e)}', 'error')
    
    return redirect(url_for('jobs'))

@app.route('/search')
def search():
    """Search resumes"""
    query = request.args.get('q', '')
    skill_filter = request.args.get('skill', '')
    
    results = Resume.query
    
    if query:
        results = results.filter(
            (Resume.name.ilike(f'%{query}%')) |
            (Resume.email.ilike(f'%{query}%'))
        )
    
    results = results.all()
    
    if skill_filter:
        results = [r for r in results if skill_filter in r.get_skills_list()]
    
    return render_template('search.html', results=results, query=query)

@app.route('/api/dashboard-data')
def api_dashboard_data():
    """API endpoint for dashboard data"""
    from datetime import datetime, timedelta
    
    all_resumes = Resume.query.all()
    skills_count = {}
    
    # Get top skills
    for resume in all_resumes:
        for skill in resume.get_skills_list():
            skills_count[skill] = skills_count.get(skill, 0) + 1
    
    top_skills = sorted(skills_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Get upload trend (last 30 days)
    today = datetime.utcnow().date()
    trend_data = {}
    for i in range(29, -1, -1):  # Last 30 days
        date = today - timedelta(days=i)
        trend_data[date.strftime('%Y-%m-%d')] = 0
    
    for resume in all_resumes:
        if resume.uploaded_at:
            date_str = resume.uploaded_at.date().strftime('%Y-%m-%d')
            if date_str in trend_data:
                trend_data[date_str] += 1
    
    # Convert to sorted lists
    trend_dates = sorted(trend_data.keys())
    trend_counts = [trend_data[date] for date in trend_dates]
    
    # Format dates for display (show every 5 days to avoid clutter)
    trend_labels = []
    for i, date_str in enumerate(trend_dates):
        if i % 5 == 0 or i == len(trend_dates) - 1:
            trend_labels.append(date_str)
        else:
            trend_labels.append('')
    
    return jsonify({
        'total_resumes': len(all_resumes),
        'total_skills': len(skills_count),
        'top_skills': dict(top_skills),
        'labels': [skill[0] for skill in top_skills],
        'data': [skill[1] for skill in top_skills],
        'trend_labels': trend_dates,
        'trend_data': trend_counts,
        'trend_display_labels': trend_labels
    })

@app.route('/api/leaderboard-data')
def api_leaderboard_data():
    """API endpoint for leaderboard data"""
    resumes = Resume.query.all()
    leaderboard_data = []
    
    for resume in resumes:
        score = calculate_leaderboard_score(resume)
        leaderboard_data.append({
            'name': resume.name,
            'skills': resume.get_skills_list(),
            'skill_count': len(resume.get_skills_list()),
            'score': score
        })
    
    leaderboard_data = sorted(leaderboard_data, key=lambda x: x['score'], reverse=True)
    
    return jsonify(leaderboard_data[:20])

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)