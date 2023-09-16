import models
from database import engine, SessionLocal
from datetime import date, time
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import engine, SessionLocal


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Qso(BaseModel):
    date: date
    timeon: time
    callsign: str = Field(min_length=1, max_length=15)
    band: int
    mode: str = Field(min_length=1, max_length=15)
    city: str = Field(max_length=100)
    state: str = Field(max_length=100)
    county: str = Field(max_length=100)
    country: str = Field(max_length=100)
    name: str = Field(max_length=100)
    qslr: bool
    qsls: bool
    rstr: int
    rsts: int
    power: int
    remarks: str = Field(max_length=1500)


Qsos = []


@app.get('/')
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Qsos).all()


@app.post('/')
def create_qso(qso: Qso, db: Session = Depends(get_db)):

    qso_model = models.Qsos()
    qso_model.date = qso.date
    qso_model.timeon = qso.timeon
    qso_model.callsign = qso.callsign
    qso_model.band = qso.band
    qso_model.mode = qso.mode
    qso_model.city = qso.city
    qso_model.state = qso.state
    qso_model.county = qso.county
    qso_model.country = qso.country
    qso_model.name = qso.name
    qso_model.qslr = qso.qslr
    qso_model.qsls = qso.qsls
    qso_model.rstr = qso.rstr
    qso_model.rsts = qso.rsts
    qso_model.power = qso.power
    qso_model.remarks = qso.remarks

    db.add(qso_model)
    db.commit()


@app.put('/{qso_id}')
def update_qso(qso_id: int, qso: Qso, db: Session = Depends(get_db)):

    qso_model = db.query(models.Qsos).filter(models.Qsos.id == qso_id).first()

    if qso_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'ID {qso_id} : Does not exist'
        )

    qso_model.date = qso.date
    qso_model.timeon = qso.timeon
    qso_model.callsign = qso.callsign
    qso_model.band = qso.band
    qso_model.mode = qso.mode
    qso_model.city = qso.city
    qso_model.state = qso.state
    qso_model.county = qso.county
    qso_model.country = qso.country
    qso_model.name = qso.name
    qso_model.qslr = qso.qslr
    qso_model.qsls = qso.qsls
    qso_model.rstr = qso.rstr
    qso_model.rsts = qso.rsts
    qso_model.power = qso.power
    qso_model.remarks = qso.remarks

    db.add(qso_model)
    db.commit()
    return qso


@app.delete('/{qso_id}')
def delete_qso(qso_id: int, qso: Qso, db: Session = Depends(get_db)):

    qso_model = db.query(models.Qsos).filter(models.Qsos.id == qso_id).first()

    if qso_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'ID {qso_id} : Does not exist'
    )

    db.query(models.Qsos).filter(models.Qsos.id == qso_id).delete()
    db.commit()
    return qso

