from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from db import SessionLocal
from models.doctor import Doctor

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/')
def doctor_list():
    session_db = SessionLocal()
    doctors = session_db.query(Doctor).filter_by(IsDeleted=False).all()
    session_db.close()
    current_role = session.get('role', None)
    return render_template('doctor.html', doctors=doctors, current_role=current_role)

@doctor_bp.route('/add', methods=['POST'])
def add_doctor():
    if session.get('role') != 'manager':
        abort(403)  # Forbidden
    
    session_db = SessionLocal()
    new_doctor = Doctor(
        Doctor_ID=request.form['Doctor_ID'],
        Doctor_FName=request.form['Doctor_FName'],
        Doctor_LName=request.form['Doctor_LName'],
        Department_ID=request.form['Department_ID'],
        Doctor_Contact_Number=request.form['Doctor_Contact_Number'],
        Visit_Fee=request.form['Visit_Fee'],
        Room_Num=request.form['Room_Num']
    )
    session_db.add(new_doctor)
    session_db.commit()
    session_db.close()
    return redirect(url_for('doctor.doctor_list'))

@doctor_bp.route('/delete/<string:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    if session.get('role') != 'manager':
        abort(403)
    
    session_db = SessionLocal()
    doctor = session_db.query(Doctor).filter_by(Doctor_ID=doctor_id).first()
    if doctor:
        doctor.IsDeleted = True
        session_db.commit()
    session_db.close()
    return redirect(url_for('doctor.doctor_list'))

@doctor_bp.route('/edit/<string:doctor_id>')
def edit_doctor(doctor_id):
    if session.get('role') != 'manager':
        abort(403)
    
    session_db = SessionLocal()
    doctor = session_db.query(Doctor).filter_by(Doctor_ID=doctor_id, IsDeleted=False).first()
    session_db.close()
    if doctor:
        return render_template('edit_doctor.html', doctor=doctor)
    return redirect(url_for('doctor.doctor_list'))

@doctor_bp.route('/update/<string:doctor_id>', methods=['POST'])
def update_doctor(doctor_id):
    if session.get('role') != 'manager':
        abort(403)
    
    session_db = SessionLocal()
    doctor = session_db.query(Doctor).filter_by(Doctor_ID=doctor_id, IsDeleted=False).first()
    if doctor:
        doctor.Doctor_FName = request.form['Doctor_FName']
        doctor.Doctor_LName = request.form['Doctor_LName']
        doctor.Department_ID = request.form['Department_ID']
        doctor.Doctor_Contact_Number = request.form['Doctor_Contact_Number']
        doctor.Visit_Fee = request.form['Visit_Fee']
        doctor.Room_Num = request.form['Room_Num']
        session_db.commit()
    session_db.close()
    return redirect(url_for('doctor.doctor_list'))

