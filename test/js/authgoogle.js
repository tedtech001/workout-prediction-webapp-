// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyB0a9V8e2Pn2V7iHVXxQooZhvZ-ISBQTZE",
  authDomain: "fit-twebapp.firebaseapp.com",
  projectId: "fit-twebapp",
  storageBucket: "fit-twebapp.appspot.com",
  messagingSenderId: "803865654166",
  appId: "1:803865654166:web:b5834e2a0b14c7755e63b7",
  measurementId: "G-YEDWY797B5"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);