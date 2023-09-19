from sqlalchemy import Column, Integer, String, Date, Time, Boolean
from .database import Base


class Qsos(Base):
    __tablename__ = 'qsos'
    id = Column(Integer, primary_key=True, index=True)
    dateon = Column(Date)
    timeon = Column(Time)
    callsign = Column(String, index=True, nullable=False)
    band = Column(Integer, nullable=False)
    mode = Column(String, nullable=False)
    city = Column(String)
    state = Column(String)
    county = Column(String)
    country = Column(String)
    name = Column(String)
    qslr = Column(Boolean, default=False, index=True)
    qsls = Column(Boolean, default=False, index=True)
    rstr = Column(Integer, nullable=False)
    rsts = Column(Integer, nullable=False)
    power = Column(Integer, nullable=False)
    remarks = Column(String)
