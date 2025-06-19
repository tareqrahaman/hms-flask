from flask import Blueprint, render_template, request, redirect, url_for
from db import SessionLocal
from models.patient import Patient

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/')
def patient_list():
    session = SessionLocal()
    patients = session.query(Patient).filter_by(IsDeleted=False).all()
    session.close()
    return render_template('patient.html', patients=patients)

@patient_bp.route('/add', methods=['POST'])
def add_patient():
    session = SessionLocal()
    new_patient = Patient(
        Patient_ID=request.form['Patient_ID'],
        Patient_FName=request.form['Patient_FName'],
        Patient_LName=request.form['Patient_LName'],
        Patient_Contact_Number=request.form['Patient_Contact_Number'],
        IsInpatient='IsInpatient' in request.form,
        AnyTestTaken='AnyTestTaken' in request.form,
        Patient_Address=request.form['Patient_Address']
    )
    session.add(new_patient)
    session.commit()
    session.close()
    return redirect(url_for('patient.patient_list'))

@patient_bp.route('/delete/<string:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    session = SessionLocal()
    patient = session.query(Patient).filter_by(Patient_ID=patient_id).first()
    if patient:
        patient.IsDeleted = True
        session.commit()
    session.close()
    return redirect(url_for('patient.patient_list'))

