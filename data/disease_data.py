import pandas as pd
import numpy as np
import random

# --- 1. The Master Data ---
disease_data = {
    "Malaria": {"symptoms": ["High Fever", "Chills", "Sweating", "Headache", "Nausea"], "specialist": "Infectious Disease Specialist"},
    "Typhoid": {"symptoms": ["Sustained Fever", "Headache", "Abdominal Pain", "Constipation", "Weakness"], "specialist": "Internal Medicine"},
    "Dengue": {"symptoms": ["High Fever", "Severe Joint Pain", "Skin Rash", "Vomiting", "Pain behind eyes"], "specialist": "Infectious Disease Specialist"},
    "Diabetes": {"symptoms": ["Frequent Urination", "Increased Thirst", "Blurred Vision", "Fatigue", "Slow healing sores"], "specialist": "Endocrinologist"},
    "Pneumonia": {"symptoms": ["Cough with phlegm", "Fever", "Chills", "Difficulty breathing", "Chest Pain"], "specialist": "Pulmonologist"},
    "Common Cold": {"symptoms": ["Sneezing", "Runny Nose", "Sore Throat", "Mild Cough", "Stuffy Nose"], "specialist": "General Physician"},
    "Hypertension": {"symptoms": ["Severe Headache", "Fatigue", "Confusion", "Chest Pain", "Difficulty breathing"], "specialist": "Cardiologist"},
    "Migraine": {"symptoms": ["Throbbing Headache", "Nausea", "Light Sensitivity", "Sound Sensitivity", "Blurred Vision"], "specialist": "Neurologist"},
    "Jaundice": {"symptoms": ["Yellow Skin", "Yellow Eyes", "Dark Urine", "Fatigue", "Abdominal Pain"], "specialist": "Gastroenterologist"},
    "Arthritis": {"symptoms": ["Joint Pain", "Joint Stiffness", "Swelling", "Redness", "Decreased range of motion"], "specialist": "Rheumatologist"},
    "Bronchial Asthma": {"symptoms": ["Wheezing", "Shortness of breath", "Chest tightness", "Coughing", "Rapid breathing"], "specialist": "Pulmonologist"},
    "Psoriasis": {"symptoms": ["Red patches", "Silvery scales", "Dry cracked skin", "Itching", "Swollen joints"], "specialist": "Dermatologist"},
    "Gastroenteritis": {"symptoms": ["Watery Diarrhea", "Stomach Cramps", "Nausea", "Vomiting", "Low-grade fever"], "specialist": "Gastroenterologist"},
    "Tuberculosis": {"symptoms": ["Persistent Cough", "Chest Pain", "Coughing up blood", "Fatigue", "Night Sweats"], "specialist": "Pulmonologist"},
    "Hypothyroidism": {"symptoms": ["Fatigue", "Weight Gain", "Cold intolerance", "Dry Skin", "Muscle Weakness"], "specialist": "Endocrinologist"},
    "Hyperthyroidism": {"symptoms": ["Weight Loss", "Rapid Heartbeat", "Sweating", "Irritability", "Nervousness"], "specialist": "Endocrinologist"},
    "Urinary Tract Infection": {"symptoms": ["Burning urination", "Frequent urge", "Cloudy urine", "Pelvic Pain", "Strong smell"], "specialist": "Urologist"},
    "Chicken Pox": {"symptoms": ["Itchy Rash", "Fluid-filled blisters", "Fever", "Fatigue", "Loss of appetite"], "specialist": "General Physician"},
    "Anaemia": {"symptoms": ["Fatigue", "Pale Skin", "Shortness of breath", "Dizziness", "Cold hands/feet"], "specialist": "Hematologist"},
    "GERD (Acid Reflux)": {"symptoms": ["Heartburn", "Regurgitation", "Chest Pain", "Difficulty swallowing", "Chronic Cough"], "specialist": "Gastroenterologist"},
    "Sinusitis": {"symptoms": ["Facial Pain", "Blocked Nose", "Headache", "Sore Throat", "Postnasal drip"], "specialist": "ENT Specialist"},
    "Appendicitis": {"symptoms": ["Lower right Pain", "Nausea", "Vomiting", "Loss of appetite", "Fever"], "specialist": "General Surgeon"},
    "Kidney Stones": {"symptoms": ["Severe side pain", "Painful urination", "Pink/Red urine", "Nausea", "Vomiting"], "specialist": "Urologist"},
    "Sepsis": {"symptoms": ["High heart rate", "Confusion", "Extreme shivering", "Shortness of breath", "Clammy skin"], "specialist": "Emergency Medicine"},
    "Heart Attack": {"symptoms": ["Chest Pain", "Shortness of breath", "Nausea", "Lightheadedness", "Cold Sweat"], "specialist": "Cardiologist"},
    "Heart Failure": {"symptoms": ["Shortness of breath", "Fatigue", "Swelling in legs", "Rapid heart rate", "Persistent cough"], "specialist": "Cardiologist"},
    "Chronic Kidney Disease": {"symptoms": ["Fatigue", "Swollen ankles", "Shortness of breath", "Blood in urine", "Itchy skin"], "specialist": "Nephrologist"},
    "Kidney Infection": {"symptoms": ["Back pain", "High Fever", "Painful urination", "Shaking chills", "Nausea"], "specialist": "Nephrologist"},
    "Liver Cirrhosis": {"symptoms": ["Yellow skin", "Abdominal swelling", "Easy bruising", "Itchy skin", "Fatigue"], "specialist": "Hepatologist"},
    "Liver Cancer": {"symptoms": ["Weight loss", "Upper abdominal pain", "Yellow eyes", "White chalky stool", "Fatigue"], "specialist": "Oncologist"},
    "Brain Tumor": {"symptoms": ["Severe Headache", "Seizures", "Vision changes", "Balance issues", "Personality changes"], "specialist": "Neurosurgeon"},
    "Cataract": {"symptoms": ["Blurred vision", "Night blindness", "Halos around lights", "Fading colors", "Double vision"], "specialist": "Ophthalmologist"},
    "Glaucoma": {"symptoms": ["Eye pain", "Headache", "Blurred vision", "Redness in eye", "Nausea"], "specialist": "Ophthalmologist"},
    "Stroke": {"symptoms": ["Facial drooping", "Arm weakness", "Speech difficulty", "Sudden confusion", "Dizziness"], "specialist": "Neurologist"},
    "Vertigo": {"symptoms": ["Dizziness", "Loss of balance", "Nausea", "Ringing in ears", "Swaying sensation"], "specialist": "ENT Specialist"},
    "Gallstones": {"symptoms": ["Upper right pain", "Back pain", "Nausea", "Vomiting", "Fever with chills"], "specialist": "Gastroenterologist"},
    "Pancreatitis": {"symptoms": ["Upper abdominal pain", "Tenderness", "Fever", "Rapid pulse", "Oily stools"], "specialist": "Gastroenterologist"},
    "Pneumothorax": {"symptoms": ["Sharp chest pain", "Shortness of breath", "Rapid heart rate", "Dry cough", "Fatigue"], "specialist": "Pulmonologist"},
    "Melanoma (Skin)": {"symptoms": ["Changing mole", "Irregular borders", "Dark pigment", "Itching", "Bleeding skin"], "specialist": "Dermatologist"},
    "Meningitis": {"symptoms": ["Stiff neck", "High fever", "Severe headache", "Confusion", "Seizures"], "specialist": "Neurologist"},
    "Parkinson's": {"symptoms": ["Tremors", "Slow movement", "Rigid muscles", "Impaired posture", "Speech changes"], "specialist": "Neurologist"},
    "Crohn's Disease": {"symptoms": ["Abdominal cramps", "Diarrhea", "Fatigue", "Weight loss", "Blood in stool"], "specialist": "Gastroenterologist"},
    "Macular Degeneration": {"symptoms": ["Blurred vision", "Dark spots", "Distorted vision", "Reduced central vision", "Need for bright light"], "specialist": "Ophthalmologist"},
    "Acne": {"symptoms": ["Whiteheads", "Blackheads", "Red Bumps", "Pus-filled lumps", "Tenderness"], "specialist": "Dermatologist"},
    "Food Poisoning": {"symptoms": ["Nausea", "Vomiting", "Watery Diarrhea", "Abdominal Pain", "Fever"], "specialist": "Internal Medicine"},
    "Allergy": {"symptoms": ["Sneezing", "Itchy Eyes", "Runny Nose", "Skin Rash", "Swelling"], "specialist": "Allergist"},
    "Eczema": {"symptoms": ["Dry Skin", "Severe Itching", "Red/Brown patches", "Small Bumps", "Thickened skin"], "specialist": "Dermatologist"},
    "Hepatitis A": {"symptoms": ["Yellow Skin", "Sudden Nausea", "Abdominal Pain", "Dark Urine", "Fatigue"], "specialist": "Hepatologist"},
    "Pleurisy": {"symptoms": ["Sharp Chest Pain", "Shortness of breath", "Cough", "Fever", "Rapid heart rate"], "specialist": "Pulmonologist"},
    "Peptic Ulcer": {"symptoms": ["Burning Stomach", "Bloating", "Heartburn", "Nausea", "Fatigue"], "specialist": "Gastroenterologist"}
}

# --- 2. Training Data Generator ---
def get_training_data():
    all_symptoms = sorted(list(set([s for d in disease_data.values() for s in d['symptoms']])))
    rows = []
    for disease, info in disease_data.items():
        # Create 10 variations per disease for better AI accuracy
        for _ in range(10):
            row = {s: 0 for s in all_symptoms}
            row['Disease'] = disease
            # AI logic: Even if the user only has 3 out of 5 symptoms, detect the disease
            num_symptoms = random.randint(3, len(info['symptoms']))
            for s in random.sample(info['symptoms'], num_symptoms):
                row[s] = 1
            rows.append(row)
    return pd.DataFrame(rows), all_symptoms