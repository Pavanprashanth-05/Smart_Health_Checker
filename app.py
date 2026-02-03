from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import numpy as np 
from sklearn.ensemble import RandomForestClassifier 
from datetime import datetime
import random 
import os
import sys

# Ensure the current directory is in the path for Vercel to find the 'data' folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- DATA IMPORTS ---
try:
    from data.disease_data import get_training_data, disease_data 
    from data.precautions import precautions 
    from data.hospitals import hospitals 
except ImportError as e:
    print(f"Import Error: {e}")

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'your_health_ai_secret_key'

# DATABASE FIX FOR VERCEL
# Use /tmp for Vercel, or local sqlite for testing
if os.environ.get('VERCEL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/users.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
# Initialize with empty values to prevent crash if data load fails
symptoms_list = []
model = None

try:
    df, symptoms_list = get_training_data() 
    X = df[symptoms_list].values 
    y = df['Disease'].values 
    model = RandomForestClassifier(n_estimators=10, random_state=42).fit(X, y) 
except Exception as e:
    print(f"Model Training Error: {e}")

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
    flash('Invalid credentials.', 'danger')
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
        flash('Success! Please log in.', 'success')
    return redirect(url_for('login'))

@app.route('/index') 
@login_required
def index(): 
    return render_template('index.html', symptoms=symptoms_list, states=sorted(hospitals.keys())) 

@app.route('/predict', methods=['POST']) 
@login_required
def predict(): 
    if model is None:
        return "Model not loaded correctly. Check Vercel logs."
        
    name = request.form.get('name') 
    state = request.form.get('state') 
    user_symptoms = [request.form.get(f's{i}') for i in range(1, 5)] 
    active = [s.replace('_', ' ') for s in user_symptoms if s and s != ""] 
    
    if not active: return "<h3>Please select symptoms!</h3>" 

    input_data = np.zeros(len(symptoms_list)).reshape(1, -1) 
    for i, s in enumerate(symptoms_list): 
        if s in user_symptoms:  
            input_data[0][i] = 1 
     
    prediction = model.predict(input_data)[0] 
    specialist_needed = disease_data.get(prediction, {}).get('specialist', 'General Physician') 
    recommended_hospitals = hospitals.get(state, {}).get(specialist_needed, ["General Hospital"]) 

    return render_template('result.html', name=name, disease=prediction, 
                           precautions=precautions.get(prediction, ["Consult a doctor"]), 
                           hospitals=recommended_hospitals, state=state, 
                           date=datetime.now().strftime("%d %b %Y"), 
                           report_id=random.randint(10000, 99999)) 

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/get_bg')
def get_bg():
    return send_from_directory('templates', '22.jpeg')

# Critical for Vercel to create DB on startup
with app.app_context():
    db.create_all()

if __name__ == '__main__': 
    app.run(debug=True)
