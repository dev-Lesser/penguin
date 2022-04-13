import json
import sys
sys.path.append('./')
from app import app
from chalice.test import Client
from test_unit_data import UnitTestData

def test_index():
    with Client(app) as client:
        response = client.http.get('/')
        assert response.status_code == 200
        assert response.json_body == {'messege':'success'}


def test_search_evstation_seq():
    with Client(app) as client:
        response = client.http.get(f'/station/{UnitTestData.search_evstation_seq_data}')
        assert response.status_code == 200
        

def test_search_evstation():
    with Client(app) as client:
        response = client.http.post(
            '/search/evstation',
            headers={'Content-Type':'application/json'},
            body=json.dumps(UnitTestData.search_evstation_data)
        )
        assert response.status_code == 200


def test_recommend_evstation():
    with Client(app) as client:
        response = client.http.post(
            '/station/recommend',
            headers={'Content-Type':'application/json'},
            body=json.dumps(UnitTestData.recommand_evstation_data)
        )
        assert response.status_code == 200
