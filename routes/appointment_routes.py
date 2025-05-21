from flask import Blueprint, render_template, request, redirect, url_for
from db import SessionLocal
from models.appointment import Appointment

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/')
def appointment_list():
    session = SessionLocal()
    appointments = session.query(Appointment).all()
    session.close()
    return render_template('appointment.html', appointments=appointments)

@appointment_bp.route('/add', methods=['POST'])
def add_appointment():
    session = SessionLocal()
    new_appointment = Appointment(
        Appointment_ID=request.form['Appointment_ID'],
        Patient_ID=request.form['Patient_ID'],
        Doctor_ID=request.form['Doctor_ID'],
        Appointment_Date=request.form['Appointment_Date'],
        Appointment_Time=request.form['Appointment_Time']
    )
    session.add(new_appointment)
    session.commit()
    session.close()
    return redirect(url_for('appointment.appointment_list'))
