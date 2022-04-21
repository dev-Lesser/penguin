import os
import json
import time
from sqlalchemy import func, or_, and_, between
from multiprocessing import Manager, Process

import requests
from chalicelib.constants.configs import KILOMETER, EVSTATION_COLUMNS
from chalicelib.tables.evstation_table import EvStationTable
from chalicelib.utils.utils import AlchemyEncoder
from chalicelib.tables.evstation_status_table import EvStationStatusTable
from chalicelib.tables.filter_table import FilterTable

def search_evstation_query(db, item) -> list:
    data = db.query(
        EvStationTable.lat,
        EvStationTable.lng,
        EvStationTable.busiId,
        EvStationTable.busiNm,
        EvStationTable.statId,
        EvStationTable.chgerType,
        EvStationStatusTable.statUpdDt,
        EvStationStatusTable.stat,
        EvStationTable.statNm,
        func.count(EvStationStatusTable.statId),
        EvStationTable.addr,
        EvStationTable.parkingFree,
        EvStationStatusTable.stat,
        EvStationTable.method,
        EvStationTable.output
    )\
    .join(EvStationStatusTable, 
        (EvStationTable.statId==EvStationStatusTable.statId)
        &(EvStationTable.chgerId==EvStationStatusTable.chgerId))\
    .filter(
        EvStationTable.lat.between(item.get('minx'), item.get('maxx')) # latitude
        &  EvStationTable.lng.between(item.get('miny'), item.get('maxy'))# longitude
    )\
    .group_by(EvStationStatusTable.statId)
    
    # 
    filters = {key: val for key, val in item.items() if key not in ['minx','miny','maxx','maxy', 
                                                                    'currentXY', 'order', 'offset','limit']}
    current_xy= item.get('currentXY')

    if filters:
        data = search_evstation_query_filter_builder(data, filters)
    
    if current_xy:
        data = data.order_by(func.pow(
                (EvStationTable.lng - current_xy[1]),2) + func.pow((EvStationTable.lat-current_xy[0]),2)\
                .asc())
        results = list()
        if item.get('order') == 'T':
            # time 기준 ordering 일 때 pagination 으로 받아옴
            offset = item.get('offset') if item.get('offset') else 0
            limit = item.get('limit') if item.get('limit') else 5
            data = data.offset(offset).limit(limit).all() 
            results = search_evstation_query_order_builder(data, current_xy)
        else:
            # distance 기준 ordering 일때 그냥 all 로 리스트를 받아옴
            data = data.all() 
            for i in data:
                r = {}
                for idx, column_name in enumerate(EVSTATION_COLUMNS):
                    r[column_name] = i[idx]
                results.append(r)

    return results 

def get_time_from_naver_map(result, current_xy, current_time, durations):

    lat, lng = result[:2]

    params = {
        'start': f'{current_xy[1]},{current_xy[0]}',
        'goal': f'{lng},{lat}',
        'departureTime': current_time,
        'mode': 'TIME',
        'lang': 'ko',
    }
    url = os.environ['NAVER_MAP_URL']
    res = requests.get(url, params=params)

    if not res.json()['paths']:
        duration = 0
    else:
        duration = res.json()['paths'][0]['duration'] # 첫번째 최적경로
    result_item = {'duration': duration}

    for key, value in zip(EVSTATION_COLUMNS, result):
        result_item[key] = value


    durations.append(result_item)


def search_evstation_query_order_builder(data, current_xy):
    results = data
    current_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))

    processes = []
    durations = Manager().list()

    for res in results:
        process = Process(target=get_time_from_naver_map, args=(res, current_xy, current_time, durations))
        processes.append(process)
    for process in processes:
        process.start()
    for process in processes:
        process.join()

    results = [v for v in sorted(durations, key=lambda x : x['duration'])]

    return results


def search_evstation_query_filter_builder(data, filters: dict):
    for key, ft in filters.items():
        filter_query = []
        for value in ft:
            if key == 'output': # 충전용량 min max
                max_output, min_output = max(ft), min(ft)
                filter_query.append(between(getattr(EvStationTable, key), min_output, max_output))    
                break # where between 2번 중복 방지
            elif key == 'parkingFree' or key == 'limitYn':
                filter_query.append(and_(getattr(EvStationTable, key) == value))
            else: 
                filter_query.append(or_(getattr(EvStationTable, key) == value))
        data = data.filter(or_(*filter_query))

    return data

def search_evstation_seq_query(db, stat_id) -> list:
    data = db.query(EvStationTable).join(EvStationStatusTable, 
                EvStationTable.statId==EvStationStatusTable.statId)\
                .filter(EvStationStatusTable.statId == stat_id)\
                .all()

    results = json.loads(json.dumps(data, cls=AlchemyEncoder))
    return results

def recommend_evstation_query_builder(routes: list, distance) -> or_:
    route_filters = []
    for route in routes:
        route_filters.append(
            (
                func.degrees(
                    func.acos(
                        func.sin(func.radians(EvStationTable.lat)) * func.sin(func.radians(route[0])) + 
                        func.cos(func.radians(EvStationTable.lat)) * func.cos(func.radians(route[0])) * 
                        func.cos(func.radians(EvStationTable.lng - route[1]))
                    )
                ) * KILOMETER
            ) < distance
        )
    return or_(*route_filters)


def recommend_evstation_query(db, routes, distance) -> list: 
    build_query = recommend_evstation_query_builder(routes, distance)

    results = db.query(EvStationTable).filter(build_query).all()
    results = json.loads(json.dumps(results, cls=AlchemyEncoder))

    return results

def get_search_filter_query(db) -> dict:
    data = db.query(FilterTable).all()
    filters = {}
    for i in data:
        item = i.as_dict()
        filters.setdefault(item.get('from_column'), [])
        filters[item.get('from_column')].append({
            'filter': item.get('name'), 
            'desc': item.get('info')
            })
    
    return filters


def get_autocomplete_query(db, keyword: str, offset: int, limit: int) -> dict:
    keyword = "%{}%".format(keyword)
    data = db.query(EvStationTable.statNm).distinct(EvStationTable.statNm)\
        .filter(EvStationTable.statNm.like(keyword)).offset(offset).limit(limit).all()
    
    results = [i[0] for i in data]
    return results