
import os
from chalice import CORSConfig

HEADERS = {
    'Content-Type' : os.environ['CONTENT_TYPE'],
    'Access-Control-Allow-Origin' : os.environ['Access_Control_Allow_Origin']
}

CORS_CONFIG = CORSConfig(
    allow_origin=os.environ['ALLOW_ORIGIN'],
    allow_credentials=True
)
EVSTATION_COLUMNS = ["lat","lng", "busiId", "businNm","statId", "chgerType", 
    "statUpdDt" ,"stat", "statNm", "count", "addr", "parkingFree" ,"stat", 'method', 'output']

KILOMETER = 60 * 1.1515 * 1.609344
