from .models import Qsos
from .database import engine, SessionLocal, Base
from datetime import date, time
from fastapi import FastAPI, HTTPException, Depends
from fastapi_versioning import VersionedFastAPI, version
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session


app = FastAPI()
Base.metadata.create_all(bind=engine)


# Dependency to get the SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Qso(BaseModel):
    dateon: date
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


@app.get('/')
@version(1, 0)
def read_api(db: Session = Depends(get_db)):
    return db.query(Qsos).all()


@app.post('/')
@version(1, 0)
def create_qso(qso: Qso, db: Session = Depends(get_db)):

    qso_model = Qsos(**qso.model_dump())

    try:
        db.add(qso_model)
        db.commit()
    except Exception as e:
        print(f"Error occurred while adding QSO to the database: {e}")
        db.rollback()


@app.put('/{qso_id}')
@version(1, 0)
def update_qso(qso_id: int, qso: Qso, db: Session = Depends(get_db)):

    qso_model = db.query(Qsos).filter(Qsos.id == qso_id).first()

    if qso_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'ID {qso_id} : Does not exist'
        )

    for key, value in qso.model_dump():
        setattr(qso_model, key,value)

    try:
        db.add(qso_model)
        db.commit()
    except Exception as e:
        print(f"Error occurred while updating QSO in the database: {e}")
        db.rollback()

    return qso


@app.delete('/{qso_id}')
@version(1, 0)
def delete_qso(qso_id: int, qso: Qso, db: Session = Depends(get_db)):

    qso_model = db.query(Qsos).filter(Qsos.id == qso_id).first()

    if qso_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'ID {qso_id} : Does not exist'
        )

    try:
        db.query(Qsos).filter(Qsos.id == qso_id).delete()
        db.commit()
    except Exception as e:
        print(f"Error occurred while deleting QSO from the database: {e}")
        db.rollback()

    return qso


app = VersionedFastAPI(app, 
    default_api_version=(1, 0),
    dependencies=[Depends(get_db)]    
)
