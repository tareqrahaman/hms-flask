from sqlalchemy import Column, String, SmallInteger, Date, ForeignKey
from models import Base

class Admission(Base):
    __tablename__ = 'Admission'

    Admission_ID = Column(String(20), primary_key=True)
    Patient_ID = Column(String(20), ForeignKey('Patient.Patient_ID'))
    Room_Num = Column(SmallInteger, ForeignKey('Room.Room_Num'))
    Admission_Date = Column(Date, nullable=False)
    Release_Date = Column(Date, nullable=False)
