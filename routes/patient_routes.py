from flask import Blueprint, render_template, request, redirect, url_for, session as flask_session, abort
from db import SessionLocal
from models.patient import Patient

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/')
def patient_list():
    db_session = SessionLocal()
    patients = db_session.query(Patient).filter_by(IsDeleted=False).all()
    db_session.close()
    current_role = flask_session.get('role')
    return render_template('patient.html', patients=patients, current_role=current_role)

@patient_bp.route('/add', methods=['POST'])
def add_patient():
    # Only managers can add patients
    if flask_session.get('role') != 'manager':
        abort(403)
    db_session = SessionLocal()
    new_patient = Patient(
        Patient_ID=request.form['Patient_ID'],
        Patient_FName=request.form['Patient_FName'],
        Patient_LName=request.form['Patient_LName'],
        Patient_Contact_Number=request.form['Patient_Contact_Number'],
        IsInpatient='IsInpatient' in request.form,
        AnyTestTaken='AnyTestTaken' in request.form,
        Patient_Address=request.form['Patient_Address']
    )
    db_session.add(new_patient)
    db_session.commit()
    db_session.close()
    return redirect(url_for('patient.patient_list'))

@patient_bp.route('/delete/<string:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    # Only managers can delete
    if flask_session.get('role') != 'manager':
        abort(403)
    db_session = SessionLocal()
    patient = db_session.query(Patient).filter_by(Patient_ID=patient_id).first()
    if patient:
        patient.IsDeleted = True
        db_session.commit()
    db_session.close()
    return redirect(url_for('patient.patient_list'))

@patient_bp.route('/edit/<string:patient_id>')
def edit_patient(patient_id):
    # Only managers can edit
    if flask_session.get('role') != 'manager':
        abort(403)
    db_session = SessionLocal()
    patient = db_session.query(Patient).filter_by(Patient_ID=patient_id, IsDeleted=False).first()
    db_session.close()
    if patient:
        return render_template('edit_patient.html', patient=patient)
    return redirect(url_for('patient.patient_list'))

@patient_bp.route('/update/<string:patient_id>', methods=['POST'])
def update_patient(patient_id):
    # Only managers can update
    if flask_session.get('role') != 'manager':
        abort(403)
    db_session = SessionLocal()
    patient = db_session.query(Patient).filter_by(Patient_ID=patient_id, IsDeleted=False).first()
    if patient:
        patient.Patient_FName = request.form['Patient_FName']
        patient.Patient_LName = request.form['Patient_LName']
        patient.Patient_Contact_Number = request.form['Patient_Contact_Number']
        patient.Patient_Address = request.form['Patient_Address']
        patient.IsInpatient = 'IsInpatient' in request.form
        patient.AnyTestTaken = 'AnyTestTaken' in request.form
        db_session.commit()
    db_session.close()
    return redirect(url_for('patient.patient_list'))
