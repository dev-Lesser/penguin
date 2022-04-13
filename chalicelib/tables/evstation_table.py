from sqlalchemy import Column, Integer, String, Float
from ..utils.db import BASE

class EvStationTable(BASE):
    __tablename__ = "evtable"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    seq         = Column(Integer, primary_key=True, autoincrement=True)
    statNm      = Column(String(50))
    statId      = Column(String(50), unique=True)
    chgerId     = Column(String(20))
    chgerType   = Column(String(20))
    stat        = Column(String(5))
    addr        = Column(String(200))
    location    = Column(String(200))
    lat         = Column(Float)
    lng         = Column(Float)
    useTime     = Column(String(100))
    busiId      = Column(String(10))
    bnm         = Column(String(20))
    busiNm      = Column(String(10))
    busiCall    = Column(String(20))
    output      = Column(String(20))
    method      = Column(String(20))
    zcode       = Column(String(10))
    parkingFree = Column(String(20))
    note        = Column(String(10))
    limitYn     = Column(String(5))
    limitDetail = Column(String(200))
    delYn       = Column(String(5))
    delDetail   = Column(String(200))
    
    def __init__(self, seq, statNm, statId, chgerId, chgerType, stat, addr, location,
        lat, lng, useTime, busiId, bnm, busiNm, busiCall, output, method,
        zcode, parkingFree, note, limitYn, limitDetail, delYn, delDetail
    ):
        self.seq            = seq
        self.statNm         = statNm   
        self.statId         = statId 
        self.chgerId        = chgerId 
        self.chgerType      = chgerType 
        self.stat           = stat
        self.addr           = addr
        self.location       = location 
        self.lat            = lat
        self.lng            = lng 
        self.useTime        = useTime 
        self.busiId         = busiId 
        self.bnm            = bnm
        self.busiNm         = busiNm 
        self.busiCall       = busiCall 
        self.output         = output 
        self.method         = method 
        self.zcode          = zcode 
        self.parkingFree    = parkingFree
        self.note           = note
        self.limitYn        = limitYn
        self.limitDetail    = limitDetail
        self.delYn          = delYn
        self.delDetail      = delDetail


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
