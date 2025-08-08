from flask import Blueprint, render_template, request, redirect, url_for, session
from db import SessionLocal
from models.admission import Admission
from models.patient import Patient
from flask import session, abort

admission_bp = Blueprint('admission', __name__)

@admission_bp.route('/')
def admission_list():
    session_db = SessionLocal()
    admissions = session_db.query(Admission).filter_by(IsDeleted=False).all()
    session_db.close()
    current_role = session.get('role', None)
    return render_template('admission.html', admissions=admissions, current_role=current_role)

@admission_bp.route('/add', methods=['POST'])
def add_admission():
    if session.get('role') != 'manager':
        abort(403)  # Forbidden
    
    session_db = SessionLocal()

    new_admission = Admission(
        Admission_ID=request.form['Admission_ID'],
        Patient_ID=request.form['Patient_ID'],
        Room_Num=int(request.form['Room_Num']),
        Admission_Date=request.form['Admission_Date'],
        Release_Date=request.form['Release_Date']
    )

    session_db.add(new_admission)
    session_db.commit()
    session_db.close()
    return redirect(url_for('admission.admission_list'))

@admission_bp.route('/delete/<string:admission_id>', methods=['POST'])
def delete_admission(admission_id):
    session = SessionLocal()
    admission = session.query(Admission).filter_by(Admission_ID=admission_id).first()
    if admission:
        admission.IsDeleted = True
        session.commit()
    session.close()
    return redirect(url_for('admission.admission_list'))


@admission_bp.route('/edit/<string:admission_id>')
def edit_admission(admission_id):
    session = SessionLocal()
    admission = session.query(Admission).filter_by(Admission_ID=admission_id, IsDeleted=False).first()
    session.close()
    if admission:
        return render_template('edit_admission.html', admission=admission)
    return redirect(url_for('admission.admission_list'))


@admission_bp.route('/update/<string:admission_id>', methods=['POST'])
def update_admission(admission_id):
    session = SessionLocal()
    admission = session.query(Admission).filter_by(Admission_ID=admission_id, IsDeleted=False).first()
    if admission:
        admission.Patient_ID = request.form['Patient_ID']
        admission.Room_Num = int(request.form['Room_Num'])
        admission.Admission_Date = request.form['Admission_Date']
        admission.Release_Date = request.form['Release_Date']
        session.commit()
    session.close()
    return redirect(url_for('admission.admission_list'))

