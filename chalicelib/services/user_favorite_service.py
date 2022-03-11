import json
import os
from chalice import Blueprint, Response
from chalicelib.constants.configs import HEADERS, CORS_CONFIG

from chalicelib.schemes.user_favorite_scheme import UserFavoriteScheme

from chalicelib.utils.db import db_session, DATABASES

from chalicelib.services.query.user_favorite_query import *

from chalicelib.errors.bad_request_error import bad_request_error # 400
from chalicelib.errors.not_found_error import not_found_error # 404



user_favorite_route = Blueprint(__name__)

# Load schemes
user_fav_scheme = UserFavoriteScheme()

@user_favorite_route.route(
    path = '/search/favorites', 
    methods = ['GET', 'POST', 'DELETE'],
    cors = CORS_CONFIG, 
)
def handle_favorites() -> dict:
    """
    [get/remove create favorites] user favorite
    """
    e = user_favorite_route.current_request.to_dict()
    params = e.get('query_params')
    with db_session(DATABASES) as db:
        if user_favorite_route.current_request.method == 'GET':
            user_id = params.get('id')
            success, evtable_results, user_favorite_results = get_favorites_query(db, user_id)
            if not success:
                return bad_request_error(f'There is no user id = {user_id}')
            results = {
                'evstation': evtable_results,
                'userInfo': user_favorite_results
            }
            return Response(
                body=results,
                headers=HEADERS,
                status_code=200
            )

        elif user_favorite_route.current_request.method == 'DELETE':
            errors = user_fav_scheme.validate(params)
            if errors:
                return bad_request_error(errors)

            user_id = params.get('id')
            stat_id = params.get('statId')
            results = delete_favorites_query(db, user_id, stat_id)
            if not results:
                return not_found_error(f'There is no user id = "{user_id}" & stat_id = "{stat_id}"')
            else:
                return Response(
                    body={'message': 'success', 'stat_id': stat_id, 'id': user_id},
                    headers=HEADERS,
                    status_code=204
                )

        
        elif user_favorite_route.current_request.method == 'POST':
            item = json.loads(user_favorite_route.current_request.raw_body.decode())
            errors = user_fav_scheme.validate(item)
            if errors:
                return bad_request_error(errors)

            user_id = item.get('id')
            stat_id = item.get('statId')
            is_not_found, is_duplicated, success = add_favorite_query(db, user_id, stat_id)

            if success:
                return Response(
                    body={'message': 'success', 'id': user_id, 'stat_id': stat_id },
                    headers=HEADERS,
                    status_code=201
                )
                
            if is_duplicated:
                return bad_request_error(
                    message=f'Duplicate user id = "{user_id}" & stat_id = "{stat_id}"'
                )
            if is_not_found:
                return not_found_error(
                    message=f'Not found user id = "{user_id}" or stat id = "{stat_id}"'
                )

