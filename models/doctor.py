from sqlalchemy import Column, String, Numeric, SmallInteger, ForeignKey, Boolean
from models import Base

class Doctor(Base):
    __tablename__ = 'Doctor'

    Doctor_ID = Column(String(20), primary_key=True)
    Doctor_FName = Column(String(15))
    Doctor_LName = Column(String(15))
    Department_ID = Column(String(20), ForeignKey('Department.Department_ID'))
    Doctor_Contact_Number = Column(String(20))
    Visit_Fee = Column(Numeric(10, 2))
    Room_Num = Column(SmallInteger, ForeignKey('Room.Room_Num'))
    IsDeleted = Column(Boolean, nullable=False, default=False)

