from flask import Blueprint, render_template, request, redirect, url_for
from db import SessionLocal
from models.admission import Admission
from models.patient import Patient
admission_bp = Blueprint('admission', __name__, url_prefix='/admission')

@admission_bp.route('/')
def admission_list():
    session = SessionLocal()
    admissions = session.query(Admission).all()
    session.close()
    return render_template('admission.html', admissions=admissions)

@admission_bp.route('/add', methods=['POST'])
def add_admission():
    session = SessionLocal()

    new_admission = Admission(
        Admission_ID=request.form['Admission_ID'],
        Patient_ID=request.form['Patient_ID'],
        Room_Num=int(request.form['Room_Num']),
        Admission_Date=request.form['Admission_Date'],
        Release_Date=request.form['Release_Date']
    )

    session.add(new_admission)
    session.commit()
    session.close()
    return redirect(url_for('admission.admission_list'))
