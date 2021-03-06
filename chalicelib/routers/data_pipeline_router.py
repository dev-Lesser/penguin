import os
import time
import xml.etree.ElementTree as ET
import requests

from chalice import Blueprint
from chalicelib.utils.db import db_session, DATABASES
from chalicelib.tables.station_status_table import StationStatusTable

service_key = os.environ['EV_SERVICE_KEY']

url = 'http://apis.data.go.kr/B552584/EvCharger/getChargerInfo'

column_names = ['statNm','statId','chgerId','chgerType','addr','location','lat','lng','useTime',
    'busiId','bnm','busiNm','busiCall','stat','statUpdDt','lastTsdt','lastTedt','nowTsdt',
    'output','method','zcode','parkingFree','note','limitYn','limitDetail','delYn','delDetail'
]
zcodes = ['42', '41', '48', '47', '29', '27', '30', '26', '36', '11', '31', '28', '46', '45', '50', '44', '43']

db = db_session(DATABASES)

data_pipeline_route = Blueprint(__name__)

@data_pipeline_route.schedule('rate(1 hour)')
def upsert_db():
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

        r = [StationStatusTable(**res)  for res in results ]
        insert_cnt, update_cnt = 0,0
        for res in results:
            stat_id = res.get('statId')
            chager_id = res.get('chgerId')
            is_exist = db.query(StationStatusTable).filter(
                StationStatusTable.statId == stat_id,
                StationStatusTable.chgerId == chager_id
            ).first()
            if not is_exist:
                insert_cnt +=1
                res['created_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                res['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                db.add(StationStatusTable(**res))
            else:
                update_cnt +=1
                res['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                db.query(StationStatusTable).filter(
                    StationStatusTable.statId == stat_id,
                    StationStatusTable.chgerId == chager_id
                ).update(res)

        print(f'insert cnt {insert_cnt} / update cnt {update_cnt}')


        output[zcode] = [insert_cnt, update_cnt]
        db.commit()
    print(output)
    return output