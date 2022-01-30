import sqlalchemy
from sqlalchemy import create_engine,Column,Integer,String, DateTime, ForeignKey
from sqlalchemy import engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base=declarative_base()

class Patients(Base):

    __tablename__="patients"

    id= Column(Integer,primary_key=True)
    name= Column(String,)
    age=Column(Integer)
    gender=Column(String)

    def __str__(self) -> str:
        return self.name

class Images(Base):

    __tablename__="images"
    id= Column(Integer,primary_key=True)
    path=Column(String,)
    type=Column(Integer,default=-1)
    patient=Column(ForeignKey('patients.id'))
    upload_date=Column(DateTime, default=datetime.now())

    def __str__(self) -> str:
        return self.patient.name

if __name__=="__main__":
   engine= create_engine('sqlite:///db.sqlite3')
   Base.metadata.create_all(engine)

    

