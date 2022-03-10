"""
check_user_info [post] user 자동로그인 처리
get_user_info [get] user 정보 가져오기
"""
import json
import os

from chalice import Blueprint, Response, CORSConfig
from chalicelib.schemes.account_scheme import UserInfoScheme, GetUserInfoScheme

from chalicelib.utils.db import db_session, DATABASES
from chalicelib.services.query.account_login_query import *

from chalicelib.errors.bad_request_error import bad_request_error # 400
from chalicelib.errors.not_found_error import not_found_error # 404

# db = db_session(DATABASES)

account_scheme = UserInfoScheme()
account_check_scheme = GetUserInfoScheme()

account_login_service_route = Blueprint(__name__)

HEADERS = {
    'Content-Type' : os.environ['CONTENT_TYPE'],
    'Access-Control-Allow-Origin' : os.environ['Access_Control_Allow_Origin']
}

CORS_CONFIG = CORSConfig(
    allow_origin=os.environ['ALLOW_ORIGIN'],
    allow_credentials=True
)

# auto login
@account_login_service_route.route(
    path = '/login/user-info', 
    methods = ['POST'],
    cors = CORS_CONFIG, 
)
def check_user_info() -> list:
    item = json.loads(account_login_service_route.current_request.raw_body.decode())
    errors = account_scheme.validate(item)
    if errors:
        return bad_request_error(errors)
    
    user_id = item.get('id')
    token = item.get('token')
    kind = item.get('kind')
    with db_session(DATABASES) as db:
        results = check_user_info_query(db, user_id, token, kind)
    
    return Response(
        body=results,
        headers=HEADERS,
        status_code=200
    )
#로그인정보 가져오기
@account_login_service_route.route(
    path = '/login/user-info',
    methods = ['GET'],
    cors = CORS_CONFIG
)
def get_user_info() -> list:
    e = account_login_service_route.current_request.to_dict()
    params = e.get('query_params')
    errors = account_check_scheme.validate(params)
    if errors:
        return bad_request_error(errors)
    
    user_id = params.get('id')
    kind = params.get('kind')
    with db_session(DATABASES) as db:
        results= get_user_info_query(db, user_id, kind)

    if not results:
        return not_found_error(f'No results user id = "{user_id}", kind = "{kind}"')
    return Response(
        body=results,
        headers=HEADERS,
        status_code=200
    )