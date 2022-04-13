from sqlalchemy import Column, Integer, String, ForeignKey
from chalicelib.tables.evstation_table import EvStationTable


from ..utils.db import BASE

class EvStationStatusTable(BASE):
    __tablename__ = "station_status"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    seq         = Column(Integer, primary_key=True, autoincrement=True)
    busiId      = Column(String(2))
    statId      = Column(String(50), ForeignKey(EvStationTable.statId))
    chgerId     = Column(String(20))
    stat        = Column(String(10))
    statUpdDt   = Column(String(20))
    lastTsdt    = Column(String(20))
    lastTedt    = Column(String(20))
    nowTsdt     = Column(String(20))
        
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
