# 🎓 AI Student Performance Predictor

A full-stack Machine Learning web application that predicts student performance based on study patterns and academic indicators.

---
## 📌 Features

- 🔐 User Authentication (Login/Register)
- 👨‍🎓 Student Performance Prediction (ML Model)
- 📊 Admin Dashboard with Analytics
- 📈 Charts (Pass vs Fail, Student Scores)
- 📋 Prediction History
- 🧑‍💼 Role-Based Access (Admin & Student)
- 🗑️ Admin Controls (View & Delete Records)

---

## 🧠 Machine Learning

- Algorithm: Random Forest Classifier
- Features Used:
  - Student ID
  - Student Name
  - Study Hours
  - Attendance
  - Sleep Hours
  - Weekly Study Hours
  - Previous Scores

---

## 🛠️ Tech Stack

### Frontend:
- HTML
- CSS (Bootstrap)
- JavaScript
- Chart.js

### Backend:
- Python (Flask)
- Flask-Login
- Flask-SQLAlchemy

### Database:
- SQLite

---

## 📊 Dashboard Features

- Total Students Count
- Total Predictions
- 📊 Pass vs Fail Pie Chart
- 📈 Student Score Bar Chart
- Prediction Summary Table

---

## 🔐 Authentication System

- Login & Registration
- Session Management
- Role-Based Access Control:
  - Admin → Full access
  - Student → Limited access

---

## 📂 Project Structure

Student_ml_app/
│
│
├── templates/
│ ├── home.html
│ ├── login.html
│ ├── admin_dashboard.html
│ ├── admin.html
│ ├── history.html
│ ├── view.html
│ ├── index.html
│ ├── register.html
│
├── instance
│ ├──database.db
│
│
└── artifacts
│ ├──model.pkl ├──model.pkl
│ ├──scaler.pkl
│ ├──student_performance.csv
│ ├──studentperformancefactors.csv
│
│
│
├── app.py
├── requirements.txt
├── Procfile
└── runtime.txt

---

## 🌍 Deployment

Deployed using:
- Render (Free Hosting)
- Gunicorn

---

## 🎯 Objective

To help educators and students identify academic performance early and take corrective actions using data-driven insights.

---

## 🚀 Future Improvements

- 📊 Advanced analytics dashboard
- 📈 Real-time data tracking
- ☁️ PostgreSQL integration
- 📱 Mobile-friendly UI
- 🤖 Improved ML model accuracy

---

## 👨‍💻 Author

Name- AIZA GHANCHI

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!