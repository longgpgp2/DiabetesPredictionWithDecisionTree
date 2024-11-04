import pandas as pd
import requests

test_data = pd.read_csv('./data/test_diabetes.csv')

url = 'http://127.0.0.1:5000/predict'

for index, row in test_data.iterrows():
    data = {
        'pregnancies': row['Pregnancies'],
        'glucose': row['Glucose'],
        'blood_pressure': row['BloodPressure'],
        'skin_thickness': row['SkinThickness'],
        'insulin': row['Insulin'],
        'bmi': row['BMI'],
        'diabetes_pedigree_function': row['DiabetesPedigreeFunction'],
        'age': row['Age']
    }
    
    response = requests.post(url, data=data)
    
    print(f"Test Case {index + 1}:")
    print(f"  Input Data:")
    print(f"    Pregnancies: {data['pregnancies']}")
    print(f"    Glucose: {data['glucose']}")
    print(f"    Blood Pressure: {data['blood_pressure']}")
    print(f"    Skin Thickness: {data['skin_thickness']}")
    print(f"    Insulin: {data['insulin']}")
    print(f"    BMI: {data['bmi']}")
    print(f"    Diabetes Pedigree Function: {data['diabetes_pedigree_function']}")
    print(f"    Age: {data['age']}")
    print(f"  Response: {response.json()}\n")