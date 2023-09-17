import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from qsolink.database import Base
from qsolink.qsolink import app, get_db
from qsolink.models import Qsos


# Create an in-memory SQLite database for testing
engine = create_engine('sqlite:///:memory:')
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope='module')
def test_db():
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture(scope='module')
def client():
    with TestClient(app) as client:
        yield client


def test_create_qso(client, test_db):
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

    response = client.post('/', json=qso_data)
    assert response.status_code == 200
    assert response.json() == qso_data

    # Verify that the QSO was saved in the database
    qso = test_db.query(Qsos).filter_by(callsign=qso_data['callsign']).first()
    assert qso is not None
    assert qso.date == qso_data['date']
    assert qso.timeon == qso_data['timeon']
    assert qso.band == qso_data['band']


def test_read_api(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == []