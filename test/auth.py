import pyrebase 
config = {
  'apiKey': "AIzaSyAhw2tTF4I4cD_Mb0_o3-j4DhRqICzuUro",
  'authDomain': "auth-c6171.firebaseapp.com",
  'projectId': "auth-c6171",
  'storageBucket': "auth-c6171.appspot.com",
  'messagingSenderId': "439355952345",
  'appId': "1:439355952345:web:1319839a8898a4cf7382c8",
  'measurementId': "G-HSWNEQGPTT"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email = 'test@gmail.com'
password = '123456'

user = auth.create_user_with_email_and_password(email, password)
print(user)