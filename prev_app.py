import pandas as pd
from flask import Flask, request, render_template, jsonify
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

app = Flask(__name__)

# Load and prepare the dataset
data = pd.read_csv('./data/diabetes.csv')
X = data.drop('Outcome', axis=1)
y = data['Outcome']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model using Decision Tree Classifier
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate the model (optional)
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))

@app.route('/')
def home():
    return render_template('index.html')

# Return a Json string for the Post endpoint
@app.route('/predict', methods=['POST'])
def predict():
    features = [float(x) for x in request.form.values()]
    final_features = scaler.transform([features])
    prediction = model.predict(final_features)
    
    output = "High risk of diabetes" if prediction[0] == 1 else "Low risk of diabetes"
    
    return jsonify({'prediction': output})

if __name__ == "__main__":
    app.run(debug=True)