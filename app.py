from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd 
import numpy as np 
from sklearn.ensemble import RandomForestClassifier 
from datetime import datetime
from flask import send_from_directory
import random 
import os

# --- DATA IMPORTS ---
# Ensure these files exist in your /data folder
from data.disease_data import get_training_data, disease_data 
from data.precautions import precautions 
from data.hospitals import hospitals 

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'your_health_ai_secret_key'
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

# --- ML MODEL SETUP ---
df, symptoms_list = get_training_data() 
X = df[symptoms_list] 
y = df['Disease'] 
model = RandomForestClassifier(n_estimators=100, random_state=42).fit(X, y) 

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
    
    # Get symptoms from form
    user_symptoms = [request.form.get(f's{i}') for i in range(1, 5)] 
    active = [s.replace('_', ' ') for s in user_symptoms if s and s != ""] 
    symptoms_string = ", ".join(active) 

    if not active:  
        return "<h3>Please select symptoms!</h3>" 

    # --- REPLACE PANDAS LOGIC WITH THIS ---
    # Create a 2D array of zeros with shape (1, number_of_symptoms)
    input_data = np.zeros(len(symptoms_list)).reshape(1, -1) 
    
    # Fill the array: if the symptom is in our list, set that index to 1
    for i, s in enumerate(symptoms_list): 
        if s in user_symptoms:  
            input_data[0][i] = 1 
     
    # Make prediction using the Numpy array instead of a DataFrame
    prediction = model.predict(input_data)[0] 
    # ---------------------------------------

    specialist_needed = disease_data.get(prediction, {}).get('specialist', 'General Physician') 
    state_data = hospitals.get(state, {}) 
    recommended_hospitals = state_data.get(specialist_needed, ["General Medical Center"]) 

    current_date = datetime.now().strftime("%d %b %Y") 
    report_id = random.randint(10000, 99999) 

    return render_template('result.html',   
                            name=name, age=age, gender=gender, disease=prediction,  
                            precautions=precautions.get(prediction, ["Consult a professional"]), 
                            hospitals=recommended_hospitals, state=state, symptoms=symptoms_string, 
                            date=current_date, report_id=report_id)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/get_bg')
def get_bg():
    # This looks for 11.jpeg inside your templates folder
    return send_from_directory('templates', '22.jpeg')

if __name__ == '__main__': 
    with app.app_context():
        db.create_all()
    app.run(debug=True)
