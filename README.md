# 🔐 BasicLogin – Android Authentication System

A robust, full-stack Android authentication system featuring **Email + OTP verification** and **Google Sign-In**.  
This project demonstrates a **secure production-style architecture** using **Kotlin** on Android and **Firebase Cloud Functions (Python)** on the backend, fully optimized for **local development using Firebase Emulator Suite**.

---

## 🚀 Features

- **Email & OTP Login**
  - Custom authentication flow
  - OTPs sent via real emails using Gmail SMTP
  - Backend-controlled OTP generation & validation

- **Google Sign-In**
  - Integrated with Google Identity Services
  - Uses Firebase Authentication with OAuth

- **Secure Backend**
  - OTP logic runs only on the server
  - Prevents client-side spoofing
  - Firestore-backed OTP storage with timestamps

- **Local Development with Emulators**
  - Firebase Auth Emulator
  - Firestore Emulator
  - Cloud Functions Emulator
  - No production data touched during development

- **Session Management**
  - Auto-login on app restart
  - Secure logout flow

- **Modern Android Stack**
  - Kotlin
  - View Binding
  - Activity Result APIs

---

## 🛠️ Tech Stack

**Frontend:** Android (Kotlin), XML, Gradle  
**Backend:** Firebase Cloud Functions (Python 3.10+), Firestore  
**Auth:** Firebase Authentication, Google OAuth  
**Tools:** Android Studio, Firebase CLI

---

## ⚙️ Prerequisites

- Android Studio (Koala or newer)
- Python 3.10+
- Node.js
- Firebase CLI (`npm install -g firebase-tools`)
- Gmail account with App Password

---

## 📥 Setup Guide

### Clone Repository
```bash
git clone https://github.com/your-username/BasicLogin.git
cd BasicLogin
```

### Backend Setup
```bash
cd functions
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Edit `functions/main.py`:
```python
SENDER_EMAIL = "your.email@gmail.com"
APP_PASSWORD = "xxxx xxxx xxxx xxxx"
```

### Firebase Setup
- Create Firebase project
- Enable Google Sign-In
- Add Android app: `com.example.basiclogin`
- Add SHA-1 (`./gradlew signingReport`)
- Download `google-services.json` → `app/`

### Run Emulators
```bash
firebase emulators:start
```

---

## 📱 Run App
- Open in Android Studio
- Sync Gradle
- Run on Android Emulator

Uses `10.0.2.2` for localhost.

---

## 📂 Project Structure
```text
BasicLogin/
├── app/
│   ├── src/main/java/com/example/basiclogin/
│   │   ├── Auth/Login.kt       # Login logic (OTP & Google)
│   │   ├── MainActivity.kt     # Home screen & Logout
│   ├── google-services.json    # Firebase Config (Ignored in git)
├── functions/
│   ├── main.py                 # Python Backend (OTP Logic)
│   ├── requirements.txt        # Python dependencies
├── firebase.json               # Emulator Config
└── README.md
```

---

## 📜 License
MIT License
