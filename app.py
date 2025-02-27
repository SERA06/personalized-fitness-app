from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import logging
from dotenv import load_dotenv
import os
import numpy as np
import joblib
from mappings.mappings import activity_mapping, intensity_mapping, bmi_mapping, health_condition_mapping
from mappings.motivation_messages import motivation_messages

logging.basicConfig(level=logging.ERROR)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == "True"
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Database Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

model = joblib.load('model/personalized_fitness_model_2.0.pkl')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        action = request.form.get('action')

        user = User.query.filter_by(email=email).first()

        if action == "register":
            if user:
                flash('Email already registered. Please log in.', 'danger')
                return redirect(url_for('login'))
            
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('fitness_check'))

        elif action == "login":
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('fitness_check'))
            else:
                flash('Invalid login credentials. Try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = Message(subject=f"New Contact Form Submission from {name}",
                      recipients=['fitnessrecommend@gmail.com'],  
                      body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")

        try:
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            flash("Failed to send message. Please try again later.", "danger")
            logging.error(f"Mail Error: {str(e)}")

        return redirect(url_for('contact')) 

    return render_template('contact.html')


@app.route('/Fitness-Check')
@login_required
def fitness_check():
    return render_template('input.html')

@app.route('/Set-Goal', methods=['GET'])
def set_goal():
    return render_template('goal.html')

@app.route('/Your-Activity', methods=['POST'])
@login_required
def your_activity():
    try:
        bmi_category = request.form.get('BMI_category', 'normal').strip().lower()
        weight = float(request.form.get('weight_kg', 0))
        height = float(request.form.get('height_cm', 0))
        fitness_level = int(request.form.get('fitness_level', 10))
        goal = request.form.get('goal', 'stay fit')  
        calories_burned_cal = float(request.form.get('calories_burned', 50))  
        calories_burned = calories_burned_cal / 40  
        duration = float(request.form.get('duration', 0))
        intensity = request.form.get('intensity', 'medium').strip().lower()
        health_condition = request.form.get('health_condition', 'None').strip()

        if weight <= 0 or height <= 0 or fitness_level < 0 or duration <= 0 or calories_burned_cal < 0:
            return "Invalid input values. Please enter valid data.", 400

        bmi_value = bmi_mapping.get(bmi_category, 1)  
        intensity_value = intensity_mapping.get(intensity, 1)  
        health_condition_value = health_condition_mapping.get(health_condition, 0)

        input_features = np.array([[calories_burned, duration, weight, intensity_value, fitness_level, height, bmi_value, health_condition_value]], dtype=np.float32)

        activity_index = int(model.predict(input_features).item())  

        goal_based_default = {
            "lose weight": "Running",
            "build muscle": "Weight Training",  
            "stay fit": "Yoga"
        }
        recommended_activity = activity_mapping.get(activity_index, goal_based_default.get(goal, "Walking"))
        motivation_message = motivation_messages.get(recommended_activity, "Stay active and keep pushing forward!")
        calories_burned_cal = calories_burned * 40  

        return render_template('result.html', 
                               activity=recommended_activity, 
                               duration=duration, 
                               calories=calories_burned_cal, 
                               goal=goal, 
                               motivation_message=motivation_message)

    except Exception as e:
        logging.error(f"Error in recommendation: {str(e)}")
        return f"An error occurred: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)
