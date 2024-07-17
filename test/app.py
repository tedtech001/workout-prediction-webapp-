import datetime
from flask import Flask, jsonify, request, render_template, redirect, send_from_directory, session, url_for
import joblib
import pandas as pd
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Enable CORS for the app
CORS(app)

# Load the pre-trained model and encoders
model = joblib.load('fitness_model.pkl')
scaler = joblib.load('scaler.pkl')
le_gender = joblib.load('le_gender.pkl')

# Initialize Firebase Admin SDK
cred = credentials.Certificate('C:/Users/Administrator/Desktop/test/clientsectet.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Define features for scaling
features = ['Weight', 'Height', 'BMI', 'Age']

# Define the exercise_plans dictionary
exercise_plans = {
    1: """Plan 1:<br>
    Monday:<br>
    Cardio: 30 min running (Warm-up: 5 min light jogging, Main Workout: 30 min running, Cool-down: 5 min stretching)<br>
    Strength: Upper Body (Push-ups, Dumbbell Bench Press, Bicep Curls, Tricep Dips, Plank)<br><br>
    
    Tuesday:<br>
    Cardio: 30 min cycling (Warm-up: 5 min light cycling, Main Workout: 30 min cycling, Cool-down: 5 min stretching)<br>
    Strength: Lower Body (Squats, Lunges, Leg Press, Calf Raises, Deadlifts)<br><br>
    
    Wednesday:<br>
    Cardio: 30 min brisk walking (Warm-up: 5 min light walking, Main Workout: 30 min brisk walking, Cool-down: 5 min stretching)<br>
    Strength: Core (Sit-ups, Russian Twists, Bicycle Crunches, Leg Raises, Plank)<br><br>
    
    Thursday:<br>
    Cardio: 30 min running (Warm-up: 5 min light jogging, Main Workout: 30 min running, Cool-down: 5 min stretching)<br>
    Strength: Full Body (Burpees, Dumbbell Rows, Squats, Push-ups, Mountain Climbers)<br><br>
    
    Friday:<br>
    Cardio: 30 min jogging (Warm-up: 5 min light jogging, Main Workout: 30 min jogging, Cool-down: 5 min stretching)<br>
    Strength: Upper Body (Bench Press, Dumbbell Flyes, Overhead Press, Bicep Curls, Tricep Dips)""",

    2: """Plan 2:<br>
    Monday:<br>
    Cardio: 30 min jogging (Warm-up: 5 min light jogging, Main Workout: 30 min jogging, Cool-down: 5 min stretching)<br>
    Strength: Full Body Workout (Burpees, Dumbbell Rows, Squats, Push-ups, Mountain Climbers)<br><br>
    
    Tuesday:<br>
    Cardio: 30 min cycling (Warm-up: 5 min light cycling, Main Workout: 30 min cycling, Cool-down: 5 min stretching)<br>
    Strength: Upper Body (Push-ups, Dumbbell Bench Press, Bicep Curls, Tricep Dips, Plank)<br><br>
    
    Wednesday:<br>
    Cardio: 30 min brisk walking (Warm-up: 5 min light walking, Main Workout: 30 min brisk walking, Cool-down: 5 min stretching)<br>
    Strength: Lower Body (Squats, Lunges, Leg Press, Calf Raises, Deadlifts)<br><br>
    
    Thursday:<br>
    Cardio: 30 min running (Warm-up: 5 min light jogging, Main Workout: 30 min running, Cool-down: 5 min stretching)<br>
    Strength: Core (Sit-ups, Russian Twists, Bicycle Crunches, Leg Raises, Plank)<br><br>
    
    Friday:<br>
    Cardio: 30 min jogging (Warm-up: 5 min light jogging, Main Workout: 30 min jogging, Cool-down: 5 min stretching)<br>
    Strength: Upper Body (Bench Press, Dumbbell Flyes, Overhead Press, Bicep Curls, Tricep Dips)""",

    3: """Plan 3:<br>
    Monday:<br>
    Cardio: 30 min brisk walking (Warm-up: 5 min light walking, Main Workout: 30 min brisk walking, Cool-down: 5 min stretching)<br>
    Strength: Upper Body (Dumbbell Shoulder Press, Lat Pulldowns, Chest Flyes, Tricep Extensions, Bicep Curls)<br><br>
    
    Tuesday:<br>
    Cardio: 30 min cycling (Warm-up: 5 min light cycling, Main Workout: 30 min cycling, Cool-down: 5 min stretching)<br>
    Strength: Lower Body (Squats, Lunges, Leg Press, Calf Raises, Deadlifts)<br><br>
    
    Wednesday:<br>
    Cardio: 30 min jogging (Warm-up: 5 min light jogging, Main Workout: 30 min jogging, Cool-down: 5 min stretching)<br>
    Strength: Full Body Workout (Burpees, Dumbbell Rows, Squats, Push-ups, Mountain Climbers)<br><br>
    
    Thursday:<br>
    Cardio: 30 min running (Warm-up: 5 min light jogging, Main Workout: 30 min running, Cool-down: 5 min stretching)<br>
    Strength: Core (Sit-ups, Russian Twists, Bicycle Crunches, Leg Raises, Plank)<br><br>
    
    Friday:<br>
    Cardio: 30 min brisk walking (Warm-up: 5 min light walking, Main Workout: 30 min brisk walking, Cool-down: 5 min stretching)<br>
    Strength: Upper Body (Dumbbell Shoulder Press, Lat Pulldowns, Chest Flyes, Tricep Extensions, Bicep Curls)""",

    4: """Plan 4:<br>
    Monday:<br>
    Cardio: 30 min running (Warm-up: 5 min light jogging, Main Workout: 30 min running, Cool-down: 5 min stretching)<br>
    Strength: Full Body Workout (Burpees, Dumbbell Rows, Squats, Push-ups, Mountain Climbers)<br><br>
    
    Tuesday:<br>
    Cardio: 30 min cycling (Warm-up: 5 min light cycling, Main Workout: 30 min cycling, Cool-down: 5 min stretching)<br>
    Strength: Upper Body (Push-ups, Dumbbell Bench Press, Bicep Curls, Tricep Dips, Plank)<br><br>
    
    Wednesday:<br>
    Cardio: 30 min jogging (Warm-up: 5 min light jogging, Main Workout: 30 min jogging, Cool-down: 5 min stretching)<br>
    Strength: Lower Body (Squats, Lunges, Leg Press, Calf Raises, Deadlifts)<br><br>
    
    Thursday:<br>
    Cardio: 30 min brisk walking (Warm-up: 5 min light walking, Main Workout: 30 min brisk walking, Cool-down: 5 min stretching)<br>
    Strength: Core (Sit-ups, Russian Twists, Bicycle Crunches, Leg Raises, Plank)<br><br>
    
    Friday:<br>
    Cardio: 30 min running (Warm-up: 5 min light jogging, Main Workout: 30 min running, Cool-down: 5 min stretching)<br>
    Strength: Full Body Workout (Burpees, Dumbbell Rows, Squats, Push-ups, Mountain Climbers)""",

    5: """Plan 5:<br>
    Monday:<br>
    Cardio: 30 min cycling (Warm-up: 5 min light cycling, Main Workout: 30 min cycling, Cool-down: 5 min stretching)<br>
    Strength: Upper Body (Incline Dumbbell Press, Seated Row, Overhead Press, Lat Pulldown, Tricep Extensions)<br><br>
    
    Tuesday:<br>
    Cardio: 30 min jogging (Warm-up: 5 min light jogging, Main Workout: 30 min jogging, Cool-down: 5 min stretching)<br>
    Strength: Full Body Workout (Burpees, Dumbbell Rows, Squats, Push-ups, Mountain Climbers)<br><br>
    
    Wednesday:<br>
    Cardio: 30 min brisk walking (Warm-up: 5 min light walking, Main Workout: 30 min brisk walking, Cool-down: 5 min stretching)<br>
    Strength: Lower Body (Squats, Lunges, Leg Press, Calf Raises, Deadlifts)<br><br>
    
    Thursday:<br>
    Cardio: 30 min running (Warm-up: 5 min light jogging, Main Workout: 30 min running, Cool-down: 5 min stretching)<br>
    Strength: Core (Sit-ups, Russian Twists, Bicycle Crunches, Leg Raises, Plank)<br><br>
    
    Friday:<br>
    Cardio: 30 min cycling (Warm-up: 5 min light cycling, Main Workout: 30 min cycling, Cool-down: 5 min stretching)<br>
    Strength: Upper Body (Incline Dumbbell Press, Seated Row, Overhead Press, Lat Pulldown, Tricep Extensions)""",

    6: """Plan 6:<br>
    Monday:<br>
    Cardio: 30 min jogging (Warm-up: 5 min light jogging, Main Workout: 30 min jogging, Cool-down: 5 min stretching)<br>
    Strength: Full Body Workout (Burpees, Dumbbell Rows, Squats, Push-ups, Mountain Climbers)<br><br>
    
    Tuesday:<br>
    Cardio: 30 min brisk walking (Warm-up: 5 min light walking, Main Workout: 30 min brisk walking, Cool-down: 5 min stretching)<br>
    Strength: Upper Body (Push-ups, Dumbbell Bench Press, Bicep Curls, Tricep Dips, Plank)<br><br>
    
    Wednesday:<br>
    Cardio: 30 min running (Warm-up: 5 min light jogging, Main Workout: 30 min running, Cool-down: 5 min stretching)<br>
    Strength: Lower Body (Squats, Lunges, Leg Press, Calf Raises, Deadlifts)<br><br>
    
    Thursday:<br>
    Cardio: 30 min cycling (Warm-up: 5 min light cycling, Main Workout: 30 min cycling, Cool-down: 5 min stretching)<br>
    Strength: Core (Sit-ups, Russian Twists, Bicycle Crunches, Leg Raises, Plank)<br><br>
    
    Friday:<br>
    Cardio: 30 min jogging (Warm-up: 5 min light jogging, Main Workout: 30 min jogging, Cool-down: 5 min stretching)<br>
    Strength: Full Body Workout (Burpees, Dumbbell Rows, Squats, Push-ups, Mountain Climbers)""",

    7: """Plan 7:<br>
    Monday:<br>
    Cardio: 30 min running (Warm-up: 5 min light jogging, Main Workout: 30 min running, Cool-down: 5 min stretching)<br>
    Strength: Upper Body (Bench Press, Dumbbell Flyes, Overhead Press, Bicep Curls, Tricep Dips)<br><br>
    
    Tuesday:<br>
    Cardio: 30 min cycling (Warm-up: 5 min light cycling, Main Workout: 30 min cycling, Cool-down: 5 min stretching)<br>
    Strength: Full Body Workout (Burpees, Dumbbell Rows, Squats, Push-ups, Mountain Climbers)<br><br>
    
    Wednesday:<br>
    Cardio: 30 min jogging (Warm-up: 5 min light jogging, Main Workout: 30 min jogging, Cool-down: 5 min stretching)<br>
    Strength: Lower Body (Squats, Lunges, Leg Press, Calf Raises, Deadlifts)<br><br>
    
    Thursday:<br>
    Cardio: 30 min brisk walking (Warm-up: 5 min light walking, Main Workout: 30 min brisk walking, Cool-down: 5 min stretching)<br>
    Strength: Core (Sit-ups, Russian Twists, Bicycle Crunches, Leg Raises, Plank)<br><br>
    
    Friday:<br>
    Cardio: 30 min running (Warm-up: 5 min light jogging, Main Workout: 30 min running, Cool-down: 5 min stretching)<br>
    Strength: Upper Body (Bench Press, Dumbbell Flyes, Overhead Press, Bicep Curls, Tricep Dips)"""
}



@app.route('/')
def home():
    return render_template('home.html')

# Serve images from the images directory
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('C:/Users/Administrator/Desktop/test/images', filename)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    weight = float(data['weight'])
    height = float(data['height'])
    bmi = float(data['bmi'])
    gender = data['gender']
    age = int(data['age'])

    # Handle Gender encoding
    gender_encoded = le_gender.transform([gender])[0]

    # Create a DataFrame for the input data
    input_data = pd.DataFrame({
        'Weight': [weight],
        'Height': [height],
        'BMI': [bmi],
        'Gender': [gender_encoded],
        'Age': [age]
    })

    # Scale the features
    input_data[features] = scaler.transform(input_data[features])

    # Make a prediction
    recommendation = model.predict(input_data)[0]
    exercises = exercise_plans.get(recommendation, "No plan found")

    return redirect(url_for('show_prediction', recommendation=int(recommendation), exercises=exercises))

@app.route('/prediction/<int:recommendation>')
def show_prediction(recommendation):
    exercises = request.args.get('exercises', '')
    return render_template('predict.html', recommendation=recommendation, exercises=exercises)

@app.route('/routines')
def routines():
    return render_template('routines.html')

# Serve CSS file from the main directory
@app.route('/routine.css')
def serve_css():
    return send_from_directory('.', 'routine.css')

@app.route('/predict.css')
def serve_predict_css():
    return send_from_directory('.', 'predict.css')

@app.route('/style.css')
def serve_style_css():
    return send_from_directory('.', 'style.css')

@app.route('/home.css')
def serve_home_css():
    return send_from_directory('.', 'home.css')

@app.route('/login', methods=['POST'])
def login():
    user_info = request.json.get('user')
    if user_info:
        session['user'] = user_info
        return jsonify(success=True)
    return jsonify(success=False), 401

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        # Process the feedback form submission
        feedback_data = request.json
        user_uid = feedback_data.get('uid')
        feedback_details = {
            'date': feedback_data.get('date'),
            'dayOfWeek': feedback_data.get('dayOfWeek'),
            'cardio': feedback_data.get('cardio'),
            'cardioDuration': feedback_data.get('cardioDuration'),
            'upperBody': feedback_data.get('upperBody'),
            'upperBodySets': feedback_data.get('upperBodySets'),
            'upperBodyReps': feedback_data.get('upperBodyReps'),
            'lowerBody': feedback_data.get('lowerBody'),
            'lowerBodySets': feedback_data.get('lowerBodySets'),
            'lowerBodyReps': feedback_data.get('lowerBodyReps'),
            'core': feedback_data.get('core'),
            'coreSets': feedback_data.get('coreSets'),
            'coreReps': feedback_data.get('coreReps'),
            'fullBody': feedback_data.get('fullBody'),
            'fullBodySets': feedback_data.get('fullBodySets'),
            'fullBodyReps': feedback_data.get('fullBodyReps'),
            'comments': feedback_data.get('comments'),
            'timestamp': datetime.utcnow()
        }

        # Add the feedback to Firestore
        db.collection('feedback').add(feedback_details)

        return jsonify({'success': True})

    return render_template('feedback.html')


@app.route('/feedback.css')
def serve_feedback_css():
    return send_from_directory('.', 'feedback.css')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Handle sign up logic (e.g., register new user)
        # Redirect to the login page after successful sign-up
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/google_login', methods=['POST'])
def google_login():
    user_info = request.json.get('user')
    if user_info:
        session['user'] = user_info
        return jsonify(success=True)
    return jsonify(success=False), 401

if __name__ == '__main__':
    app.run(debug=True)
