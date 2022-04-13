import json
from sqlalchemy import func, or_, and_
from chalicelib.constants.configs import KILOMETER
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
        func.count(EvStationTable.statId),
        EvStationTable.addr,
        EvStationTable.parkingFree,
        EvStationStatusTable.stat,
        EvStationTable.method
    )\
    .join(EvStationStatusTable, EvStationTable.statId==EvStationStatusTable.statId)\
    .filter(
        EvStationTable.lat.between(item.get('minx'), item.get('maxx')) # latitude
    )\
    .filter(
        EvStationTable.lng.between(item.get('miny'), item.get('maxy')) # longitude
    )\
    .group_by(EvStationTable.statId)

    filters = {key: val for key, val in item.items() if key not in ['minx','miny','maxx','maxy', 'currentXY']}
    current_xy= item.get('currentXY')

    if filters:
        data = search_evstation_query_filter_builder(data, filters)
    
    if current_xy:
        data = data.order_by(func.pow((EvStationTable.lng - current_xy[1]),2) + func.pow((EvStationTable.lat-current_xy[0]),2).asc())
  

    return data.all()


def search_evstation_query_filter_builder(data, filters: dict):
    filter_query = []
    for key, ft in filters.items():
        if key == 'stat':
            filter_query.append(getattr(EvStationStatusTable, key) == ft)
        else: filter_query.append(getattr(EvStationTable, key) == ft)
    data = data.filter(and_(*filter_query))

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
            (func.degrees(
                func.acos(
                    func.sin(func.radians(EvStationTable.lat)) * func.sin(func.radians(route[0])) + 
                    func.cos(func.radians(EvStationTable.lat)) * func.cos(func.radians(route[0])) * 
                    func.cos(func.radians(EvStationTable.lng - route[1]))
                )) * KILOMETER) < distance
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
        if item.get('from_column') not in filters.keys():
            filters[item.get('from_column')] = [{'filter': item.get('name'), 'desc': item.get('info')}]
        else:
            filters[item.get('from_column')].append({'filter': item.get('name'), 'desc': item.get('info')})
    
    return filters