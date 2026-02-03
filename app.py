from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import numpy as np 
from sklearn.ensemble import RandomForestClassifier 
from datetime import datetime
import random 
import os

# --- DATA IMPORTS ---
from data.disease_data import get_training_data, disease_data 
from data.precautions import precautions 
from data.hospitals import hospitals 

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'your_health_ai_secret_key'

# VERCEL FIX: Database must be in /tmp
if os.environ.get('VERCEL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/users.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ML MODEL SETUP (Reduced complexity to fit 250MB limit) ---
df, symptoms_list = get_training_data() 
X = df[symptoms_list].values 
y = df['Disease'].values 
model = RandomForestClassifier(n_estimators=10, random_state=42).fit(X, y) 

@app.route('/') 
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html') 

@app.route('/login_submit', methods=['POST'])
def login_submit():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        login_user(user)
        return redirect(url_for('index'))
    flash('Invalid credentials, please try again.', 'danger')
    return redirect(url_for('login'))

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    if User.query.filter_by(email=email).first():
        flash('Email already exists.', 'danger')
    else:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Success! You can now log in.', 'success')
    return redirect(url_for('login'))

@app.route('/index') 
@login_required
def index(): 
    return render_template('index.html', symptoms=symptoms_list, states=sorted(hospitals.keys())) 

@app.route('/predict', methods=['POST']) 
@login_required
def predict(): 
    name = request.form.get('name') 
    age = request.form.get('age') 
    gender = request.form.get('gender') 
    state = request.form.get('state') 
    user_symptoms = [request.form.get(f's{i}') for i in range(1, 5)] 
    active = [s.replace('_', ' ') for s in user_symptoms if s and s != ""] 
    symptoms_string = ", ".join(active) 

    if not active: return "<h3>Please select symptoms!</h3>" 

    input_data = np.zeros(len(symptoms_list)).reshape(1, -1) 
    for i, s in enumerate(symptoms_list): 
        if s in user_symptoms:  
            input_data[0][i] = 1 
     
    prediction = model.predict(input_data)[0] 
    specialist_needed = disease_data.get(prediction, {}).get('specialist', 'General Physician') 
    state_data = hospitals.get(state, {}) 
    recommended_hospitals = state_data.get(specialist_needed, ["General Medical Center"]) 

    current_date = datetime.now().strftime("%d %b %Y") 
    report_id = random.randint(10000, 99999) 

    return render_template('result.html', name=name, age=age, gender=gender, disease=prediction, 
                           precautions=precautions.get(prediction, ["Consult a professional"]), 
                           hospitals=recommended_hospitals, state=state, symptoms=symptoms_string, 
                           date=current_date, report_id=report_id) 

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/get_bg')
def get_bg():
    return send_from_directory('templates', '22.jpeg')

if __name__ == '__main__': 
    # This part only runs locally
    with app.app_context():
        db.create_all()
    app.run(debug=True)
else:
    # This part runs on Vercel
    with app.app_context():
        db.create_all()
