PRIORITY_SKILLS = {
    'AI': ['artificial intelligence', 'ai', 'machine learning', 'ml', 'deep learning', 'neural network'],
    'Python': ['python', 'py'],
    'Java': ['java'],
    'JavaScript': ['javascript', 'js', 'node.js', 'nodejs'],
    'Web': ['html', 'css', 'react', 'vue', 'angular', 'flask', 'django'],
    'Database': ['sql', 'mysql', 'postgresql', 'mongodb', 'firebase'],
    'Cloud': ['aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes'],
    'DevOps': ['docker', 'kubernetes', 'ci/cd', 'jenkins', 'git'],
}

JOB_ROLES = {
    'Machine Learning Engineer': {
        'required_skills': ['Python', 'AI', 'Mathematics', 'Statistics'],
        'keywords': ['python', 'ml', 'ai', 'tensorflow', 'keras', 'scikit-learn', 'pandas'],
        'min_match': 3,
        'description': 'Build and deploy ML models, work with data pipelines'
    },
    'Backend Developer': {
        'required_skills': ['Python', 'Java', 'Database', 'API Design'],
        'keywords': ['python', 'java', 'django', 'flask', 'sql', 'postgresql', 'rest', 'api'],
        'min_match': 3,
        'description': 'Develop server-side applications, manage databases'
    },
    'Frontend Developer': {
        'required_skills': ['JavaScript', 'HTML', 'CSS', 'React/Vue/Angular'],
        'keywords': ['javascript', 'html', 'css', 'react', 'vue', 'angular', 'ui', 'ux'],
        'min_match': 3,
        'description': 'Build responsive web interfaces, create user experiences'
    },
    'Full Stack Developer': {
        'required_skills': ['JavaScript', 'Python', 'Database', 'Frontend'],
        'keywords': ['javascript', 'python', 'react', 'django', 'flask', 'sql', 'html', 'css'],
        'min_match': 4,
        'description': 'Work on both frontend and backend, full application development'
    },
    'Data Scientist': {
        'required_skills': ['Python', 'Statistics', 'SQL', 'Visualization'],
        'keywords': ['python', 'pandas', 'numpy', 'matplotlib', 'sql', 'statistics', 'analysis'],
        'min_match': 3,
        'description': 'Analyze data, create insights, build predictive models'
    },
    'DevOps Engineer': {
        'required_skills': ['Docker', 'Kubernetes', 'CI/CD', 'Cloud'],
        'keywords': ['docker', 'kubernetes', 'ci/cd', 'jenkins', 'aws', 'azure', 'git', 'linux'],
        'min_match': 3,
        'description': 'Manage infrastructure, automate deployments, monitor systems'
    },
    'Mobile Developer': {
        'required_skills': ['Android/iOS', 'JavaScript', 'React Native'],
        'keywords': ['android', 'ios', 'swift', 'kotlin', 'react native', 'flutter', 'mobile'],
        'min_match': 2,
        'description': 'Develop mobile applications for iOS and Android'
    },
}

LEARNING_SUGGESTIONS = {
    'Python': 'Complete Python fundamentals on Coursera or Udemy to strengthen your backend development skills',
    'Machine Learning': 'Explore Andrew Ng\'s Machine Learning Specialization or fast.ai courses for deep learning concepts',
    'Web Development': 'Master modern web frameworks with freeCodeCamp or Codecademy courses',
    'Cloud': 'Pursue AWS Solutions Architect or Azure Administrator certifications from official training paths',
    'DevOps': 'Learn Docker containerization and Kubernetes orchestration through hands-on projects',
    'Java': 'Build enterprise applications with Java Spring Boot framework through online tutorials',
    'JavaScript': 'Master JavaScript ES6+ and async programming for modern frontend development',
    'React': 'Build component-based UIs with React and master state management with Redux or Context API',
    'Docker': 'Master containerization, Dockerfile optimization, and Docker Compose for microservices',
    'Kubernetes': 'Learn container orchestration, deployments, and cluster management with Kubernetes',
    'AWS': 'Get certified with AWS (Solutions Architect, Developer, or DevOps Engineer) certifications',
    'SQL': 'Master database design, optimization, and advanced queries for relational databases',
}

# All available skills ranked by industry demand
ALL_SKILLS = ['Python', 'JavaScript', 'AWS', 'Docker', 'Kubernetes', 'React', 'Java', 'SQL', 
              'Cloud', 'DevOps', 'AI', 'Database', 'Web', 'Data Science', 'Linux'
              ]

SKILL_VALUE = {
    'Python': 95,
    'JavaScript': 90,
    'AWS': 88,
    'Docker': 85,
    'Kubernetes': 84,
    'React': 82,
    'Java': 80,
    'SQL': 85,
    'Cloud': 80,
    'DevOps': 82,
    'AI': 92,
    'Database': 78,
    'Web': 75,
    'Data Science': 88,
    'Linux': 79,
}

def extract_skills_from_text(text):
    """Extract skills from resume text"""
    text_lower = text.lower()
    found_skills = set()
    
    for priority, keywords in PRIORITY_SKILLS.items():
        for keyword in keywords:
            if keyword in text_lower:
                found_skills.add(priority)
    
    return list(found_skills)

def get_job_recommendations(skills_list):
    """Get job recommendations based on skills"""
    recommendations = []
    skills_lower = [s.lower() for s in skills_list]
    
    for job_title, job_info in JOB_ROLES.items():
        match_score = 0
        matched_skills = []
        
        for keyword in job_info['keywords']:
            for skill in skills_lower:
                if keyword.lower() in skill.lower() or skill.lower() in keyword.lower():
                    if keyword not in matched_skills:
                        matched_skills.append(keyword)
                    match_score += 1
                    break
        
        # Calculate percentage match
        match_percentage = (match_score / len(job_info['keywords'])) * 100 if job_info['keywords'] else 0
        
        if match_score >= job_info['min_match']:
            missing_skills = []
            for required in job_info['required_skills']:
                if not any(required.lower() in s.lower() or s.lower() in required.lower() for s in skills_list):
                    missing_skills.append(required)
            
            # Generate learning suggestion
            learning_suggestion = job_info['description']
            for skill in missing_skills:
                if skill in LEARNING_SUGGESTIONS:
                    learning_suggestion = LEARNING_SUGGESTIONS[skill]
                    break
            
            recommendations.append({
                'title': job_title,
                'score': min(match_percentage, 100),
                'matched_skills': len(matched_skills),
                'missing_skills': missing_skills,
                'description': job_info['description'],
                'learning_path': learning_suggestion
            })
    
    return sorted(recommendations, key=lambda x: x['score'], reverse=True)

def get_skill_recommendations(skills_list):
    """Get skill recommendations based on current skills"""
    current_skills = set(skills_list)
    recommendations = []
    
    # Get all available skills from jobs
    all_job_skills = set()
    for job_info in JOB_ROLES.values():
        all_job_skills.update(job_info['required_skills'])
    
    # Find missing skills
    missing_skills = all_job_skills - current_skills
    
    for skill in missing_skills:
        if skill in SKILL_VALUE:
            # Count how many jobs require this skill
            jobs_requiring = 0
            job_titles = []
            for job_title, job_info in JOB_ROLES.items():
                if skill in job_info['required_skills']:
                    jobs_requiring += 1
                    job_titles.append(job_title)
            
            # Get learning resource
            learning_resource = LEARNING_SUGGESTIONS.get(skill, f'Learn {skill} through online courses and practice')
            
            recommendations.append({
                'skill_name': skill,
                'priority_score': SKILL_VALUE.get(skill, 70),
                'jobs_requiring': jobs_requiring,
                'job_titles': job_titles[:3],  # Top 3 jobs
                'learning_resource': learning_resource,
                'value': SKILL_VALUE.get(skill, 70)
            })
    
    # Sort by value score
    return sorted(recommendations, key=lambda x: x['value'], reverse=True)