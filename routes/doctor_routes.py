from flask import Blueprint, render_template, request, redirect, url_for
from db import SessionLocal
from models.doctor import Doctor

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/')
def doctor_list():
    session = SessionLocal()
    doctors = session.query(Doctor).all()
    session.close()
    return render_template('doctor.html', doctors=doctors)

@doctor_bp.route('/add', methods=['POST'])
def add_doctor():
    session = SessionLocal()
    new_doctor = Doctor(
        Doctor_ID=request.form['Doctor_ID'],
        Doctor_FName=request.form['Doctor_FName'],
        Doctor_LName=request.form['Doctor_LName'],
        Department_ID=request.form['Department_ID'],
        Doctor_Contact_Number=request.form['Doctor_Contact_Number'],
        Visit_Fee=request.form['Visit_Fee'],
        Room_Num=request.form['Room_Num']
    )
    session.add(new_doctor)
    session.commit()
    session.close()
    return redirect(url_for('doctor.doctor_list'))
