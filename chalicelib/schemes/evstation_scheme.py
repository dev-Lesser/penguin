"""
evstation 검색할 때 쓰는 스키마
"""
from marshmallow import Schema, fields, validate

class EvRecommendScheme(Schema):
    route = fields.List(
        fields.List(
            fields.Float(), 
            required=True, 
            validate=validate.Length(equal=2) # field 안 lat lng 의 pair
        ), 
        required=True, 
        validate=validate.Length(min=1)) # 최소 위경도 pair 1개
    distance = fields.Float(required=False)


class EvSearchScheme(Schema):
    maxx        = fields.Float(required=True)
    maxy        = fields.Float(required=True)
    minx        = fields.Float(required=True)
    miny        = fields.Float(required=True)
    currentXY   = fields.List(fields.Float(), required=False, validate=validate.Length(equal=2) )

    #[Filter]
    chgerType   = fields.List(
                    fields.String(
                        required=False, 
                        validate=validate.Length(equal=2) # 충전기타입 01~07
                    ),
                    validate=validate.Length(max=7)
                ) 
    stat        = fields.List(
                    fields.String(
                        required=False,     
                        validate=validate.ContainsOnly(choices=['1','2','3','4','5','9']) # 충전기상태 1~9
                    ), validate=validate.Length(max=3)
                ) 
    output      = fields.List(
                    fields.Integer(required=False,
                        validate=validate.Range(min=1, max=400)  # 충전 용량
                    ),
                    validate=validate.Length(equal=2)
                )
    method      = fields.List(fields.String(required=False,     validate=validate.Length(equal=2)))  # 충전방식 단독/동시
    zcode       = fields.List(fields.String(required=False,     validate=validate.Length(equal=2)), validate=validate.Length(max=3)) # 법정 코드
    parkingFree = fields.String(required=False,  validate=validate.ContainsOnly(choices=['Y','N']))
    busiId      = fields.List(fields.String(required=False), validate=validate.Length(max=3))
    limitYn     = fields.String(required=False,  validate=validate.ContainsOnly(choices=['Y','N']))
    
    # Ordering
    order       = fields.String(required=False, validate=validate.ContainsOnly(choices=['D','T']))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AutoCompleteScheme(Schema):
    statNm = fields.String(required=True, validate=validate.Length(min=2))
    offset = fields.Integer(required=False)
    limit = fields.Integer(required=False, validate=validate.Range(max=100, error="Value must be lower than 100"))
    
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}