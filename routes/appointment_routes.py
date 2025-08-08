from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from db import SessionLocal
from models.appointment import Appointment

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/')
def appointment_list():
    session_db = SessionLocal()
    appointments = session_db.query(Appointment).filter_by(IsDeleted=False).all()
    session_db.close()
    current_role = session.get('role', None)  # get current user role
    return render_template('appointment.html', appointments=appointments, current_role=current_role)

@appointment_bp.route('/add', methods=['POST'])
def add_appointment():
    if session.get('role') != 'manager':  # restrict add for manager only
        abort(403)  # Forbidden
    
    session_db = SessionLocal()
    new_appointment = Appointment(
        Appointment_ID=request.form['Appointment_ID'],
        Patient_ID=request.form['Patient_ID'],
        Doctor_ID=request.form['Doctor_ID'],
        Appointment_Date=request.form['Appointment_Date'],
        Appointment_Time=request.form['Appointment_Time']
    )
    session_db.add(new_appointment)
    session_db.commit()
    session_db.close()
    return redirect(url_for('appointment.appointment_list'))

@appointment_bp.route('/delete/<string:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    if session.get('role') != 'manager':  # restrict delete for manager only
        abort(403)
    
    session_db = SessionLocal()
    appointment = session_db.query(Appointment).filter_by(Appointment_ID=appointment_id).first()
    if appointment:
        appointment.IsDeleted = True
        session_db.commit()
    session_db.close()
    return redirect(url_for('appointment.appointment_list'))

@appointment_bp.route('/edit/<string:appointment_id>')
def edit_appointment(appointment_id):
    session_db = SessionLocal()
    appointment = session_db.query(Appointment).filter_by(Appointment_ID=appointment_id, IsDeleted=False).first()
    session_db.close()
    if appointment:
        return render_template('edit_appointment.html', appointment=appointment)
    return redirect(url_for('appointment.appointment_list'))

@appointment_bp.route('/update/<string:appointment_id>', methods=['POST'])
def update_appointment(appointment_id):
    if session.get('role') != 'manager':  # restrict update for manager only
        abort(403)
    
    session_db = SessionLocal()
    appointment = session_db.query(Appointment).filter_by(Appointment_ID=appointment_id, IsDeleted=False).first()
    if appointment:
        appointment.Patient_ID = request.form['Patient_ID']
        appointment.Doctor_ID = request.form['Doctor_ID']
        appointment.Appointment_Date = request.form['Appointment_Date']
        appointment.Appointment_Time = request.form['Appointment_Time']
        session_db.commit()
    session_db.close()
    return redirect(url_for('appointment.appointment_list'))
