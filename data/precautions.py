precautions = {
    "Malaria": ["Use mosquito nets", "Wear long sleeves", "Keep surroundings dry"],
    "Typhoid": ["Drink boiled water", "Eat hot/home-cooked food", "Maintain hand hygiene"],
    "Dengue": ["Stay hydrated with electrolytes", "Use papaya leaf extract", "Complete bed rest"],
    "Diabetes": ["Monitor blood sugar daily", "Limit sugar intake", "Daily 30-min exercise"],
    "Pneumonia": ["Complete antibiotic course", "Use a humidifier", "Get plenty of rest"],
    "Common Cold": ["Drink warm fluids", "Gargle with salt water", "Take Vitamin C"],
    "Hypertension": ["Reduce salt intake", "Practice meditation", "Avoid smoking and alcohol"],
    "Migraine": ["Rest in a dark room", "Avoid bright screens", "Apply cold compress"],
    "Jaundice": ["Eat a fat-free diet", "Drink sugarcane juice", "Avoid oily food"],
    "Arthritis": ["Apply warm compresses", "Low-impact exercises (Yoga)", "Manage body weight"],
    "Bronchial Asthma": ["Keep inhaler nearby", "Avoid dust and pollen", "Use steam inhalation"],
    "Psoriasis": ["Keep skin moisturized", "Take salt baths", "Avoid scratching the area"],
    "Gastroenteritis": ["Sip ORS or clear fluids", "Eat bland foods (Rice/Banana)", "Rest your stomach"],
    "Tuberculosis": ["Wear a mask in public", "Take meds at the same time", "High protein diet"],
    "Hypothyroidism": ["Take meds on empty stomach", "Regular thyroid checkups", "Exercise daily"],
    "Hyperthyroidism": ["Limit iodine intake", "Manage stress levels", "Monitor heart rate"],
    "Urinary Tract Infection": ["Drink 3-4 liters of water", "Drink cranberry juice", "Maintain hygiene"],
    "Chicken Pox": ["Use neem leaves in bath", "Stay isolated", "Avoid scratching blisters"],
    "Anaemia": ["Eat iron-rich food (Spinach)", "Take Vitamin B12", "Avoid caffeine with meals"],
    "GERD (Acid Reflux)": ["Avoid lying down after meals", "Limit spicy/fatty food", "Eat smaller meals"],
    "Sinusitis": ["Take steam inhalation", "Use nasal saline drops", "Stay hydrated"],
    "Appendicitis": ["Do not eat or drink", "Avoid pain meds", "Seek immediate surgery"],
    "Kidney Stones": ["Drink massive amounts of water", "Limit salt and spinach", "Avoid soda"],
    "Eczema": ["Use fragrance-free moisturizer", "Avoid harsh soaps", "Wear cotton clothes"],
    "Allergy": ["Identify and avoid triggers", "Take antihistamines", "Keep windows closed"],
    "Food Poisoning": ["Sip ORS frequently", "Avoid solid food for 8 hours", "Rest"],
    "Acne": ["Wash face twice daily", "Do not pop pimples", "Use non-oily products"],
    "Hepatitis A": ["Maintain hand hygiene", "Avoid alcohol", "Eat light, boiled food"],
    "Pleurisy": ["Take deep breaths slowly", "Rest in a comfortable position", "Avoid smoking"],
    "Peptic Ulcer": ["Avoid spicy food", "Limit caffeine", "Avoid NSAIDs like aspirin"],
    "Heart Attack": ["Chew an aspirin immediately", "Call emergency services", "Stay calm and sit down"],
    "Heart Failure": ["Limit salt and fluid intake", "Monitor weight daily", "Avoid heavy exertion"],
    "Chronic Kidney Disease": ["Follow low-protein diet", "Monitor blood pressure", "Limit salt"],
    "Kidney Infection": ["Drink plenty of water", "Complete antibiotic course", "Rest"],
    "Liver Cirrhosis": ["Absolute abstinence from alcohol", "Low salt diet", "Regular checkups"],
    "Liver Cancer": ["Maintain balanced nutrition", "Manage pain as directed", "Rest frequently"],
    "Brain Tumor": ["Manage seizures safely", "Ensure safe environment", "Regular MRI monitoring"],
    "Cataract": ["Use brighter lights", "Anti-glare sunglasses", "Schedule surgery"],
    "Glaucoma": ["Use eye drops daily", "Avoid eye strain", "Regular pressure tests"],
    "Stroke": ["Call 911 immediately", "Note the time of onset", "Keep the person calm"],
    "Vertigo": ["Lie down immediately", "Avoid sudden head moves", "Sit on the edge of the bed"],
    "Gallstones": ["Avoid fatty/fried meals", "Eat high-fiber foods", "Stay hydrated"],
    "Pancreatitis": ["Fast from solid food", "Stay hydrated with liquids", "Avoid alcohol"],
    "Pneumothorax": ["Avoid physical exertion", "Seek immediate ER care", "Do not smoke"],
    "Melanoma": ["Protect skin from sun", "Do not ignore changing moles", "Wear sunscreen"],
    "Meningitis": ["Seek immediate hospital care", "Rest in a quiet, dark room", "Hydrate"],
    "Parkinson's": ["Perform physical therapy", "Use assistive walking devices", "Speech exercises"],
    "Crohn's Disease": ["Avoid high-fiber during flares", "Manage stress", "Eat small meals"],
    "Macular Degeneration": ["Use magnifying tools", "Take AREDS2 vitamins", "Protect eyes from UV"],
    "Sepsis": ["Emergency: Seek ICU care", "Monitor oxygen levels", "Immediate antibiotics"]
}

disease_specialist_map = {
    # General Medicine / Infections
    "Malaria": "General Physician",
    "Typhoid": "General Physician",
    "Dengue": "General Physician",
    "Common Cold": "General Physician",
    "Chicken Pox": "General Physician",
    "Food Poisoning": "General Physician",
    "Allergy": "Allergist",
    "Sepsis": "Critical Care Specialist",
    
    # Respiratory (Lungs)
    "Pneumonia": "Pulmonologist",
    "Tuberculosis": "Pulmonologist",
    "Bronchial Asthma": "Pulmonologist",
    "Sinusitis": "ENT Specialist",
    "Pleurisy": "Pulmonologist",
    "Pneumothorax": "Pulmonologist",
    
    # Heart & Blood
    "Heart Attack": "Cardiologist",
    "Heart Failure": "Cardiologist",
    "Hypertension": "Cardiologist",
    "Anaemia": "Hematologist",
    "Stroke": "Neurologist",
    
    # Brain & Nervous System
    "Migraine": "Neurologist",
    "Brain Tumor": "Neurologist",
    "Vertigo": "Neurologist",
    "Parkinson's": "Neurologist",
    "Meningitis": "Neurologist",
    
    # Digestive System (Stomach/Liver/Pancreas)
    "Jaundice": "Gastroenterologist",
    "Gastroenteritis": "Gastroenterologist",
    "GERD (Acid Reflux)": "Gastroenterologist",
    "Peptic Ulcer": "Gastroenterologist",
    "Hepatitis A": "Hepatologist",
    "Liver Cirrhosis": "Hepatologist",
    "Liver Cancer": "Oncologist",
    "Gallstones": "Gastroenterologist",
    "Pancreatitis": "Gastroenterologist",
    "Crohn's Disease": "Gastroenterologist",
    "Appendicitis": "General Surgeon",
    
    # Endocrine (Hormones/Diabetes)
    "Diabetes": "Endocrinologist",
    "Hypothyroidism": "Endocrinologist",
    "Hyperthyroidism": "Endocrinologist",
    
    # Kidney & Urinary
    "Urinary Tract Infection": "Urologist",
    "Kidney Stones": "Urologist",
    "Chronic Kidney Disease": "Nephrologist",
    "Kidney Infection": "Nephrologist",
    
    # Skin & Bone
    "Psoriasis": "Dermatologist",
    "Eczema": "Dermatologist",
    "Acne": "Dermatologist",
    "Melanoma": "Dermatologist",
    "Arthritis": "Rheumatologist",
    
    # Eyes
    "Cataract": "Ophthalmologist",
    "Glaucoma": "Ophthalmologist",
    "Macular Degeneration": "Ophthalmologist"
}