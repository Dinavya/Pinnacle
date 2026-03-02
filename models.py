from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    education = db.Column(db.Text)
    experience = db.Column(db.Text)
    skills = db.Column(db.Text)  # JSON string of skills
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(200))
    score = db.Column(db.Float, default=0.0)
    
    def __repr__(self):
        return f'<Resume {self.name}>'
    
    def get_skills_list(self):
        import json
        try:
            return json.loads(self.skills) if self.skills else []
        except:
            return []
    
    def set_skills_list(self, skills_list):
        import json
        self.skills = json.dumps(skills_list)

class JobRecommendation(db.Model):
    __tablename__ = 'job_recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    job_title = db.Column(db.String(120), nullable=False)
    match_score = db.Column(db.Float)
    required_skills = db.Column(db.Text)
    missing_skills = db.Column(db.Text)
    learning_suggestions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<JobRecommendation {self.job_title}>'