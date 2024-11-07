from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from model import DiabetesModel
from file_io import load_users, save_users, load_predictions, save_predictions
import numpy as np  

from datetime import datetime  # Import datetime to handle timestamps
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ATI_FINAL'

users = load_users()
predictions = load_predictions()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

diabetes_model = DiabetesModel('./data/diabetes.csv')

@login_manager.user_loader
def load_user(user_id):
    user_data = users.get(user_id)
    if user_data:
        user = UserMixin()
        user.id = user_id
        user.email = user_data['email']
        user.password = user_data['password']
        return user
    return None

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('login'))

        users[email] = {'email': email, 'password': password}
        save_users(users)

        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = users.get(email)
        if user and user['password'] == password:
            user_obj = UserMixin()
            user_obj.id = email
            user_obj.email = user['email']
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    predictions = load_predictions()
    user_predictions = predictions.get(current_user.id, [])
    accuracy, report = diabetes_model.analyze_model()
    return render_template('dashboard.html', predictions=user_predictions, accuracy=accuracy, report=report)


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        try:
            pregnancies = int(request.form['pregnancies'])
            glucose = float(request.form['glucose'])
            blood_pressure = float(request.form['blood_pressure'])
            skin_thickness = float(request.form['skin_thickness'])
            insulin = float(request.form['insulin'])
            bmi = float(request.form['bmi'])
            pedigree_function = float(request.form['diabetes_pedigree_function'])
            age = int(request.form['age'])

            input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, pedigree_function, age]])
            prediction = diabetes_model.predict(input_data)

            result = "High risk" if prediction[0] == 1 else "Low risk"

            prediction_entry = {
                'id': len(predictions.get(current_user.id, [])) + 1,  
                'prediction_result': result,
                'created_at': datetime.now().isoformat() 
            }

            if current_user.id not in predictions:
                predictions[current_user.id] = []
            predictions[current_user.id].append(prediction_entry)
            save_predictions(predictions)

            return jsonify(prediction=result)
        except Exception as e:
            return jsonify(error=str(e)), 500
    else:
        return render_template('predict.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)