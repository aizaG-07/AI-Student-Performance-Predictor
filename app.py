from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import joblib
import numpy as np
import os


# ======================
# APP SETUP
# ======================

app = Flask(__name__)
app.secret_key = "secret123"

app.config['SECRET_KEY'] = 'df3216cb90a8f5bda1a1edd8794cc44d'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# ======================
# DATABASE MODELS
# ======================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    is_admin = db.Column(db.Boolean, default=False) 


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)

    student_id = db.Column(db.String(50))
    student_name = db.Column(db.String(100))

    hours = db.Column(db.Float)
    attendance = db.Column(db.Float)
    sleep = db.Column(db.Float)
    study = db.Column(db.Float)
    score = db.Column(db.Float)

    result = db.Column(db.String(10))

# ======================
# LOGIN MANAGER
# ======================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ======================
# LOAD MODEL
# ======================

model = joblib.load("Artifacts/model.pkl")
scaler = joblib.load("Artifacts/scaler.pkl")

# ======================
# ROUTES
# ======================

@app.route('/')
def home():
    return render_template('home.html')

# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        is_admin = True if username == "admin" else False

        user = User(
            username=username,
            email=request.form['email'],
            password=request.form['password'],
            is_admin=is_admin
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()

        if user and user.password == request.form['password']:
            login_user(user)
            return redirect('/predict_page')

    return render_template('login.html')

# ---------- LOGOUT ----------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# ---------- PREDICT PAGE ----------
@app.route('/predict_page')
@login_required
def predict_page():
    return render_template('index.html')

# ---------- PREDICT ----------
@app.route('/predict', methods=['POST'])
@login_required
def predict():
    student_id = request.form['student_id']
    student_name = request.form['student_name']

    hours = float(request.form['hours'])
    attendance = float(request.form['attendance'])
    sleep = float(request.form['sleep'])
    study = float(request.form['study'])
    score = float(request.form['score'])

    data = np.array([[hours, attendance, sleep, study, score]])
    data = scaler.transform(data)

    prediction = model.predict(data)
    result = "PASS" if prediction[0] == 1 else "FAIL"

    new_pred = Prediction(
        user_id=current_user.id,
        student_id=student_id,
        student_name=student_name,
        hours=hours,
        attendance=attendance,
        sleep=sleep,
        study=study,
        score=score,
        result=result
    )

    db.session.add(new_pred)
    db.session.commit()

    return render_template('index.html', prediction_text=result)

# ---------- HISTORY ----------
@app.route('/history')
@login_required
def history():
    preds = Prediction.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', predictions=preds)

# ---------- ADMIN ----------
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return "Access Denied"

    users = User.query.all()
    predictions = Prediction.query.all()

    total_users = len(users)
    total_predictions = len(predictions)

    # 🔥 COUNT PASS / FAIL
    pass_count = Prediction.query.filter_by(result="PASS").count()
    fail_count = Prediction.query.filter_by(result="FAIL").count()

    # 🔥 GET SCORES
    scores = [p.score for p in predictions]
    names = [p.student_name for p in predictions]

    return render_template(
        'admin_dashboard.html',
        total_users=total_users,
        total_predictions=total_predictions,
        pass_count=pass_count,
        fail_count=fail_count,
        scores=scores,
        names=names
    )

# ---------- ADMIN DATA ----------
@app.route('/admin/data')
@login_required
def admin_data():
    if not current_user.is_admin:
        return "🚫 Access Denied"

    predictions = Prediction.query.all()
    return render_template('admin.html', predictions=predictions)

# ---------- VIEW ----------
@app.route('/view/<int:id>')
@login_required
def view_prediction(id):
    if not current_user.is_admin:
        return "🚫 Access Denied"

    pred = Prediction.query.get(id)
    return render_template('view.html', p=pred)

# ---------- DELETE ----------
@app.route('/delete/<int:id>')
@login_required
def delete_prediction(id):
    if not current_user.is_admin:
        return "🚫 Access Denied"

    pred = Prediction.query.get(id)
    db.session.delete(pred)
    db.session.commit()
    return redirect('/admin/data')

# ======================
# RUN APP
# ======================

if __name__ == "__main__":
    app.run(debug=True)
    
# ======================
# DEPLOYMENT
# ======================

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

