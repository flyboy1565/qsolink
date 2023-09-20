import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from qsolink.qsolink import Qso, app, Base, engine
from qsolink.models import Qsos
from qsolink.database import get_db

# Define test database URL
TEST_DATABASE_URL = "sqlite:///./testdb.db"

# Create a new SQLAlchemy session for each test
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = {"db":override_get_db}

# Create a test client
client = TestClient(app)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Pytest fixtures for setting up and tearing down the test database
@pytest.fixture(scope="module", autouse=True)
def setup_test_database():
    if not database_exists(TEST_DATABASE_URL):
        print("creating database")
        create_database(TEST_DATABASE_URL)

    Base.metadata.create_all(bind=engine)
    yield
    print("dropping database")
    drop_database(TEST_DATABASE_URL)



app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_api():
    response = client.get('/v1_0')
    assert response.status_code == 200
    assert response.json() == []


def test_create_qso():
    qso_data = {
        'dateon': '2022-01-01',
        'timeon': '12:00:00',
        'callsign': 'W1ABC',
        'band': 20,
        'mode': 'SSB',
        'city': 'New York',
        'state': 'NY',
        'county': 'New York',
        'country': 'USA',
        'name': 'John Doe',
        'qslr': True,
        'qsls': False,
        'rstr': 59,
        'rsts': 59,
        'power': 100,
        'remarks': 'Test QSO'
    }
    response = client.post('/v1_0', json=qso_data)

    assert response.status_code == 200, response.text
    session = TestingSessionLocal()
    qso = session.query(Qsos).filter_by(callsign=qso_data['callsign']).first()
    assert qso is not None
    assert qso.dateon == datetime.strptime(qso_data['dateon'], '%Y-%m-%d').date()
    assert qso.timeon == datetime.strptime(qso_data['timeon'], '%H:%M:%S').time()

