from flask import Flask, request, jsonify, session, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cv_app.db'  # SQLite database
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class PersonalDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    school = db.Column(db.String(150), nullable=False)
    degree = db.Column(db.String(150), nullable=False)
    field_of_study = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)

class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill = db.Column(db.String(100), nullable=False)

class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    certification = db.Column(db.String(150), nullable=False)

class Hobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hobby = db.Column(db.String(100), nullable=False)

class GeneratedCV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cv_content = db.Column(db.Text, nullable=False)

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful!"})
    return jsonify({"message": "Invalid credentials!"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully!"})

@app.route('/profile', methods=['GET', 'PUT'])
def profile():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized!"}), 401

    user = User.query.get(session['user_id'])

    if request.method == 'PUT':
        data = request.get_json()
        user.email = data.get('email', user.email)
        if 'password' in data:
            user.password = generate_password_hash(data['password'], method='sha256')
        db.session.commit()
        return jsonify({"message": "Profile updated successfully!"})

    return jsonify({"username": user.username, "email": user.email})

@app.route('/personal-details', methods=['GET', 'POST'])
def personal_details():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized!"}), 401

    if request.method == 'POST':
        data = request.get_json()
        personal_detail = PersonalDetail(
            user_id=session['user_id'],
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            address=data['address']
        )
        db.session.add(personal_detail)
        db.session.commit()
        return jsonify({"message": "Personal details added successfully!"})

    personal_details = PersonalDetail.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{
        "name": pd.name,
        "email": pd.email,
        "phone": pd.phone,
        "address": pd.address
    } for pd in personal_details])

@app.route('/education', methods=['GET', 'POST'])
def education():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized!"}), 401

    if request.method == 'POST':
        data = request.get_json()
        education = Education(
            user_id=session['user_id'],
            school=data['school'],
            degree=data['degree'],
            field_of_study=data['field_of_study'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            description=data['description']
        )
        db.session.add(education)
        db.session.commit()
        return jsonify({"message": "Education details added successfully!"})

    education_details = Education.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{
        "school": ed.school,
        "degree": ed.degree,
        "field_of_study": ed.field_of_study,
        "start_date": ed.start_date,
        "end_date": ed.end_date,
        "description": ed.description
    } for ed in education_details])

@app.route('/work-experience', methods=['GET', 'POST'])
def work_experience():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized!"}), 401

    if request.method == 'POST':
        data = request.get_json()
        work_experience = WorkExperience(
            user_id=session['user_id'],
            company=data['company'],
            job_title=data['job_title'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            description=data['description']
        )
        db.session.add(work_experience)
        db.session.commit()
        return jsonify({"message": "Work experience added successfully!"})

    work_experience_details = WorkExperience.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{
        "company": we.company,
        "job_title": we.job_title,
        "start_date": we.start_date,
        "end_date": we.end_date,
        "description": we.description
    } for we in work_experience_details])

@app.route('/skills', methods=['GET', 'POST'])
def skills():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized!"}), 401

    if request.method == 'POST':
        data = request.get_json()
        skill = Skill(
            user_id=session['user_id'],
            skill=data['skill']
        )
        db.session.add(skill)
        db.session.commit()
        return jsonify({"message": "Skill added successfully!"})

    skills = Skill.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{
        "skill": sk.skill
    } for sk in skills])

@app.route('/certifications', methods=['GET', 'POST'])
def certifications():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized!"}), 401

    if request.method == 'POST':
        data = request.get_json()
        certification = Certification(
            user_id=session['user_id'],
            certification=data['certification']
        )
        db.session.add(certification)
        db.session.commit()
        return jsonify({"message": "Certification added successfully!"})

    certifications = Certification.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{
        "certification": cert.certification
    } for cert in certifications])

@app.route('/hobbies', methods=['GET', 'POST'])
def hobbies():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized!"}), 401

    if request.method == 'POST':
        data = request.get_json()
        hobby = Hobby(
            user_id=session['user_id'],
            hobby=data['hobby']
        )
        db.session.add(hobby)
        db.session.commit()
        return jsonify({"message": "Hobby added successfully!"})

    hobbies = Hobby.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{
        "hobby": hb.hobby
    } for hb in hobbies])

@app.route('/generate-cv', methods=['POST'])
def generate_cv():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized!"}), 401

    # Collect all data from the database
    personal_detail = PersonalDetail.query.filter_by(user_id=session['user_id']).first()
    education_details = Education.query.filter_by(user_id=session['user_id']).all()
    work_experience_details = WorkExperience.query.filter_by(user_id=session['user_id']).all()
    skills = Skill.query.filter_by(user_id=session['user_id']).all()
    certifications = Certification.query.filter_by(user_id=session['user_id']).all()
    hobbies = Hobby.query.filter_by(user_id=session['user_id']).all()

    # Example of a simple template
    cv_content = f"""
    Name: {personal_detail.name}
    Email: {personal_detail.email}
    Phone: {personal_detail.phone}
    Address: {personal_detail.address}

    Education:
    """
    for ed in education_details:
        cv_content += f"""
        School: {ed.school}
        Degree: {ed.degree}
        Field of Study: {ed.field_of_study}
        Start Date: {ed.start_date}
        End Date: {ed.end_date}
        Description: {ed.description}
        """

    cv_content += "\nWork Experience:\n"
    for we in work_experience_details:
        cv_content += f"""
        Company: {we.company}
        Job Title: {we.job_title}
        Start Date: {we.start_date}
        End Date: {we.end_date}
        Description: {we.description}
        """

    cv_content += "\nSkills:\n"
    for sk in skills:
        cv_content += f"- {sk.skill}\n"

    cv_content += "\nCertifications:\n"
    for cert in certifications:
        cv_content += f"- {cert.certification}\n"

    cv_content += "\nHobbies:\n"
    for hb in hobbies:
        cv_content += f"- {hb.hobby}\n"

    # Save generated CV
    generated_cv = GeneratedCV(user_id=session['user_id'], cv_content=cv_content)
    db.session.add(generated_cv)
    db.session.commit()

    return jsonify({"message": "CV generated successfully!", "cv_content": cv_content})

if __name__ == '__main__':
    app.run(debug=True)

