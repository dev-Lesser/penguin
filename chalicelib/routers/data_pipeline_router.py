import os
import time
import xml.etree.ElementTree as ET
import requests

from chalice import Blueprint
from chalicelib.utils.db import db_session, DATABASES
from chalicelib.tables.evstation_status_table import EvStationStatusTable


#[TODO] Database update evtable
service_key = os.environ['EV_SERVICE_KEY']
url = 'http://apis.data.go.kr/B552584/EvCharger/getChargerInfo'
zcodes = ['42', '41', '48', '47', '29', '27', '30', '26', '36', '11', '31', '28', '46', '45', '50', '44', '43']

db = db_session(DATABASES)
data_pipeline_route = Blueprint(__name__)

#[TODO] Code convention
# 1. evtable update, multiprocessing
# 2. station_status update
@data_pipeline_route.schedule('rate(1 hour)')
def upsert_station_status():
    output = {}
    status_column_names = ['busiId','statId', 'chgerId','stat','statUpdDt','lastTsdt','lastTedt','nowTsdt']
    url = 'http://apis.data.go.kr/B552584/EvCharger/getChargerStatus'
    for zcode in zcodes:
        page= 1
        results = []
        db = db_session(DATABASES)
        while True:
            params = {
                        'serviceKey': service_key,
                        'pageNo': page,
                        'numOfRows':9999,
                        'period':'10',
                        'zcode': zcode
                    }
            res = requests.get(url, params=params)
            tree = ET.fromstring(res.text)
            iter_element = tree.iter(tag="item") # 
            tmp_r = []
            for element in iter_element: 
                r = {}
                for element in iter_element: 
                    r = {} 
                    for name in status_column_names:
                        rtext = element.find(name).text
                        if rtext == 'null':
                            rtext = None
                        r[name] = rtext #
                    tmp_r.append(r) #
            if not tmp_r:
                break
            results.extend(tmp_r)
            page += 1
        
        stat_ids = list(set([res.get('statId') for res in results]))
        stat_ids = [{'statId': sid } for sid in stat_ids]

        r = [EvStationStatusTable(**res)  for res in results ]
        insert_cnt, update_cnt = 0,0
        for res in results:
            stat_id = res.get('statId')
            chager_id = res.get('chgerId')
            is_exist = db.query(EvStationStatusTable).filter(
                EvStationStatusTable.statId == stat_id,
                EvStationStatusTable.chgerId == chager_id
            ).first()
            if not is_exist:
                insert_cnt +=1
                res['created_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                res['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                db.add(EvStationStatusTable(**res))
            else:
                update_cnt +=1
                res['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                db.query(EvStationStatusTable).filter(
                    EvStationStatusTable.statId == stat_id,
                    EvStationStatusTable.chgerId == chager_id
                ).update(res)

        print(f'insert cnt {insert_cnt} / update cnt {update_cnt}')


        output[zcode] = [insert_cnt, update_cnt]
        db.commit()
    print(output)
    return output