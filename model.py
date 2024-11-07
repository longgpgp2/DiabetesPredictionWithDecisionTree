import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

class DiabetesModel:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = DecisionTreeClassifier(random_state=42)
        self.scaler = StandardScaler()
        self.load_data()
        self.train_model()

    def load_data(self):
        data = pd.read_csv(self.data_path)
        X = data.drop('Outcome', axis=1)
        y = data['Outcome']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    def train_model(self):
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.model.fit(self.X_train_scaled, self.y_train)

    def predict(self, input_data):
        input_data_scaled = self.scaler.transform(input_data)
        return self.model.predict(input_data_scaled)

    def analyze_model(self):
        X_test_scaled = self.scaler.transform(self.X_test)
        predictions = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(self.y_test, predictions)
        report = classification_report(self.y_test, predictions, output_dict=True)
        return accuracy, report

    def get_scaler(self):
        return self.scaler