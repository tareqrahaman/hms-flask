from sqlalchemy import Column, String, Boolean
from models import Base

class Patient(Base):
    __tablename__ = 'Patient'

    Patient_ID = Column(String(20), primary_key=True)
    Patient_FName = Column(String(15))
    Patient_LName = Column(String(15))
    Patient_Contact_Number = Column(String(20))
    IsInpatient = Column(Boolean, nullable=False, default=False)
    AnyTestTaken = Column(Boolean, nullable=False, default=False)
    Patient_Address = Column(String(40))
    IsDeleted = Column(Boolean, nullable=False, default=False)
