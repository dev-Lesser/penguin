import json
from sqlalchemy.ext.declarative import DeclarativeMeta
import datetime

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x !='registry']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    if type(data) == datetime.datetime:
                        fields[field] = data.isoformat()
                    # else:
                    #     fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

        
def create_response(data, metadata):
    body = {
        'data': data,
        'count': len(data),
        'metadata': {meta.get('name'): meta.get('value') for meta in metadata}
    }
    return body