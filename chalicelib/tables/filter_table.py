from sqlalchemy import Column, Integer, String



from ..utils.db import BASE

class FilterTable(BASE):
    __tablename__ = "filter"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    seq         = Column(Integer, primary_key=True)
    name        = Column(String(255))
    from_column = Column(String(255))
    info        = Column(String(255))
    
        
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
