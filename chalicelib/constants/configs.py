
from chalice import CORSConfig

DEV_CORS_CONFIG = CORSConfig(
    allow_origin='*',
    allow_credentials=True
)

DEV_HEADERS = {
    'Content-Type': 'application/json', 
    'Access-Control-Allow-Origin': '*'
}

EVSTATION_COLUMNS = ["lat","lng", "busiId", "businNm","statId", "chgerType", 
    "statUpdDt" ,"stat", "statNm", "count", "addr", "parkingFree" ,"stat", 'method', 'output']

KILOMETER = 60 * 1.1515 * 1.609344
