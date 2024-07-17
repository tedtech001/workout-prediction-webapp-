import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def preprocess_input(data, scaler, le_gender, le_bmicase):
    # Perform feature scaling
    features = ['Weight', 'Height', 'BMI', 'Age']
    data[features] = scaler.transform(data[features])

    # Encode categorical variables
    data['Gender'] = le_gender.transform(data['Gender'])
    data['BMIcase'] = le_bmicase.transform(data['BMIcase'])

    return data
