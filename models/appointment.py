from sqlalchemy import Column, String, Date, Time, ForeignKey
from models import Base

class Appointment(Base):
    __tablename__ = 'Appointment'

    Appointment_ID = Column(String(20), primary_key=True)
    Patient_ID = Column(String(20), ForeignKey('Patient.Patient_ID'))
    Doctor_ID = Column(String(20), ForeignKey('Doctor.Doctor_ID'))
    Appointment_Date = Column(Date)
    Appointment_Time = Column(Time)
