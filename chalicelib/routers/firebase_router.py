"""
send_message [get] firebase 메세지 전송
"""
import json
import os
from chalice import Blueprint, Response, CORSConfig
from chalicelib.errors.bad_request_error import bad_request_error # 400
from chalicelib.schemes.firebase_message_scheme import FirebaseMessageScheme
from chalicelib.utils.firebase_utils import FirebaseMessage

firebase_msg_scheme = FirebaseMessageScheme()
firebase_route = Blueprint(__name__)
HEADERS = {
    'Content-Type' : os.environ['CONTENT_TYPE'],
    'Access-Control-Allow-Origin' : os.environ['Access_Control_Allow_Origin']
}

CORS_CONFIG = CORSConfig(
    allow_origin=os.environ['ALLOW_ORIGIN'],
    allow_credentials=True
)

@firebase_route.route(
    path = '/send-message', 
    methods = ['POST'],
    cors = CORS_CONFIG, 
)
def send_massage() -> dict:
    item = json.loads(firebase_route.current_request.raw_body.decode())
    errors = firebase_msg_scheme.validate(item)
    if errors:
        return bad_request_error(errors)

    token = item.get('token')
    name = item.get('name')
    
    fm = FirebaseMessage()
    results = fm.send_message(token, name)

    return Response(
        body=results,
        headers=HEADERS,
        status_code=200
    )