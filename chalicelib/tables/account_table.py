from enum import unique
from sqlalchemy import Column,Integer,String,DateTime

from ..utils.db import BASE, ENGINE


class UserInfoTable(BASE):
    __tablename__ = "user_info"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    seq = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(20), unique=True)
    token = Column(String(1000))
    kind = Column(String(20))
    login_time = Column(DateTime)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
