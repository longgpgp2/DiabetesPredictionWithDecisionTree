from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PredictionForm(FlaskForm):
    pregnancies = IntegerField('Pregnancies', validators=[DataRequired(), NumberRange(min=0)])
    glucose = FloatField('Glucose', validators=[DataRequired(), NumberRange(min=0)])
    blood_pressure = FloatField('Blood Pressure', validators=[DataRequired(), NumberRange(min=0)])
    skin_thickness = FloatField('Skin Thickness', validators=[DataRequired(), NumberRange(min=0)])
    insulin = FloatField('Insulin', validators=[DataRequired(), NumberRange(min=0)])
    bmi = FloatField('BMI', validators=[DataRequired(), NumberRange(min=0)])
    diabetes_pedigree_function = FloatField('Diabetes Pedigree Function', validators=[DataRequired(), NumberRange(min=0)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Predict')