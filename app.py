from flask import Flask, render_template, request, redirect, url_for, session
from routes.patient_routes import patient_bp
from routes.admission_routes import admission_bp
from routes.doctor_routes import doctor_bp
from routes.appointment_routes import appointment_bp
from db import SessionLocal
from models.patient import Patient
from models.doctor import Doctor
from models.admission import Admission
from models.appointment import Appointment

from jinja2 import FileSystemLoader

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = True
app.jinja_loader = FileSystemLoader('templates')

app.secret_key = 'Monia47'

app.register_blueprint(patient_bp, url_prefix='/patients')
app.register_blueprint(admission_bp, url_prefix='/admissions')
app.register_blueprint(doctor_bp, url_prefix='/doctors')
app.register_blueprint(appointment_bp, url_prefix='/appointments')

USERS = {
    'staff1': {'password': 'staffpass', 'role': 'staff'},
    'manager1': {'password': 'managerpass', 'role': 'manager'}
}


@app.route('/')
def home():
    session_db = SessionLocal()
    num_patients = session_db.query(Patient).count()
    num_doctors = session_db.query(Doctor).count()
    num_admissions = session_db.query(Admission).count()
    num_appointments = session_db.query(Appointment).count()

    inpatients = session_db.query(Patient).filter_by(IsInpatient=True).count()
    outpatients = num_patients - inpatients
    session_db.close()


    return render_template(
        'index.html',
        num_patients=num_patients,
        num_doctors=num_doctors,
        num_admissions=num_admissions,
        num_appointments=num_appointments,
        inpatients=inpatients,
        outpatients=outpatients
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USERS and USERS[username]['password'] == password:
            session['user'] = username
            session['role'] = USERS[username]['role']  # store role
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.context_processor
def inject_user_status():
    return {
        'is_logged_in': 'user' in session,
        'current_role': session.get('role', None)
    }



if __name__ == '__main__':
    app.run(debug=True)
