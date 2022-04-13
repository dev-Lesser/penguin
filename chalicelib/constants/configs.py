
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
    "statUpdDt" ,"stat", "statNm", "count", "addr", "parkingFree" ,"stat", 'method']

KILOMETER = 60 * 1.1515 * 1.609344


        #   "USER_NAME": "b8e8b02e0d4c9b",
        #   "USER_PASSWORD": "64d89129",
        #   "DB_HOST": "us-cdbr-east-05.cleardb.net",
        #   "DB_NAME": "heroku_799e9030d4a1024",
