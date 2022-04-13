from sqlalchemy import Column,Integer,String, ForeignKey
from ..utils.db import BASE
from chalicelib.tables.account_table import UserInfoTable
from chalicelib.tables.evstation_status_table import EvStationStatusTable


class UserFavoriteTable(BASE):
    __tablename__ = "user_favorite"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    seq         = Column(Integer, primary_key=True, autoincrement=True)
    id          = Column(String(20), ForeignKey(UserInfoTable.id)) # user id email
    statId      = Column(String(50), ForeignKey(EvStationStatusTable.statId))
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
