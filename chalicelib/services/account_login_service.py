"""
check_user_info [post] user 자동로그인 처리
get_user_info [get] user 정보 가져오기
"""
import json

from chalice import Blueprint, Response
from chalicelib.constants.configs import DEV_CORS_CONFIG, DEV_HEADERS
from chalicelib.schemes.account_scheme import UserInfoScheme, GetUserInfoScheme

from chalicelib.utils.db import db_session, DATABASES
from chalicelib.services.query.account_login_query import *

from chalicelib.errors.bad_request_error import bad_request_error # 400
from chalicelib.errors.not_found_error import not_found_error # 404

# db = db_session(DATABASES)

account_scheme = UserInfoScheme()
account_check_scheme = GetUserInfoScheme()

account_login_service_route = Blueprint(__name__)

# auto login
@account_login_service_route.route(
    path = '/login/user-info', 
    methods = ['POST'],
    cors = DEV_CORS_CONFIG, 
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
        headers=DEV_HEADERS,
        status_code=200
    )
#로그인정보 가져오기
@account_login_service_route.route(
    path = '/login/user-info',
    methods = ['GET'],
    cors = DEV_CORS_CONFIG
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
        headers=DEV_HEADERS,
        status_code=200
    )