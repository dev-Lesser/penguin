"""
search_evstation [post] -> 위경도 dict
search_evstation_seq [get] -> stat_id
recommend_evstation [post] -> 위경도 list 묶음, distance default 10
"""

import json

from chalice import Blueprint, Response
from chalicelib.schemes.evstation_scheme import EvSearchScheme, EvRecommendScheme, AutoCompleteScheme
from chalicelib.constants.configs import DEV_CORS_CONFIG, DEV_HEADERS, EVSTATION_COLUMNS

from chalicelib.utils.utils import create_response
from chalicelib.utils.db import db_session, DATABASES

from chalicelib.services.query.evstation_query import *

from chalicelib.errors.bad_request_error import bad_request_error # 400
from chalicelib.errors.not_found_error import not_found_error # 404

db = db_session(DATABASES)

evstation_service_route = Blueprint(__name__)

# Load schemes
evsearch_scheme = EvSearchScheme()
evrecommend_scheme = EvRecommendScheme()
evsearch_autocomplete_scheme = AutoCompleteScheme()

@evstation_service_route.route(
    path = '/search/evstation', 
    methods = ['POST'],
    cors = DEV_CORS_CONFIG, 
)
def search_evstation() -> dict:
    """
    위경도를 받아와서 query build 후 처리
    """
    item = json.loads(evstation_service_route.current_request.raw_body.decode())
    errors = evsearch_scheme.validate(item)
    if errors:
        return bad_request_error(errors)
    results = []
    data =  search_evstation_query(db=db, item=item)
  
    for i in data:
        r = {}
        for idx, column_name in enumerate(EVSTATION_COLUMNS):
            r[column_name] = i[idx]

      
        results.append(r)

    body = create_response(
        data=results, 
        metadata=[
            {'name': 'item', 'value': item},
        ]
    )
    return Response(
        body=body,
        headers=DEV_HEADERS,
        status_code=200
    )

@evstation_service_route.route(
    path = '/station/{stat_id}', 
    methods = ['GET'],
    cors = DEV_CORS_CONFIG, 
)
def search_evstation_seq(stat_id: str) -> dict:
    """
    statId 를 통한 충전소 검색
    """

    results = search_evstation_seq_query(db=db, stat_id=stat_id)
    if not results:
        return not_found_error(f'No results staId = "{stat_id}"')
    body = create_response(
        data=results, 
        metadata=[
            {'name': 'statId', 'value': stat_id},
        ]
    )
    return Response(
        body=body,
        headers=DEV_HEADERS,
        status_code=200
    )


@evstation_service_route.route(
    path = '/station/recommend', 
    methods = ['POST'],
    cors = DEV_CORS_CONFIG, 
)
def recommend_evstation() -> dict:
    """
    post data type
    # route = [(위도, 경도), ...] 
    [Ref] https://stackoverflow.com/questions/3528754/get-results-from-mysql-based-on-latitude-longitude
    """
    item = json.loads(evstation_service_route.current_request.raw_body.decode()) 
    errors = evrecommend_scheme.validate(item)
    if errors:
        return bad_request_error(errors)
    

    route = item.get('route') if item.get('route') else None
    distance = item.get('distance') if item.get('distance') else 10 # km

    routes = list(set([tuple(r) for r in route])) # 중복제거
    results = recommend_evstation_query(db, routes, distance)
    
    body = create_response(
        data=results, 
        metadata=[
            {'name': 'distance', 'value': distance},
        ]
    )
    
    return Response(
        body=body,
        headers=DEV_HEADERS,
        status_code=200
    )

@evstation_service_route.route(
    path = '/evstation/filter', 
    methods = ['GET'],
    cors = DEV_CORS_CONFIG, 
)
def get_search_filter() -> dict:
    results = get_search_filter_query(db=db)
    return Response(
        body=results,
        headers=DEV_HEADERS,
        status_code=200
    )

@evstation_service_route.route(
    path = '/search/autocomplete', 
    methods = ['GET'],
    cors = DEV_CORS_CONFIG, 
)
def get_autocomplete() -> dict:
    e = evstation_service_route.current_request.to_dict()
    params = e.get('query_params')
    errors = evsearch_autocomplete_scheme.validate(params)
    if errors:
        return bad_request_error(errors)
    keyword = params.get('statNm')
    offset = params.get('offset') if params.get('offset') else 0
    limit = params.get('limit') if params.get('limit') else 10

    results = get_autocomplete_query(db, keyword=keyword, offset=offset, limit=limit)
    
    
    
    body = create_response(
        data=results, 
        metadata=[
            {'name': 'keyword', 'value': keyword},
        ]
    )
    
    return Response(
        body=body,
        headers=DEV_HEADERS,
        status_code=200
    )