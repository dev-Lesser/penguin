from chalicelib.tables.account_table import UserInfoTable
from chalicelib.tables.evstation_table import EvStationTable
from chalicelib.tables.user_favorite_table import UserFavoriteTable
from sqlalchemy.exc import IntegrityError

def get_favorites_query(db, user_id) -> tuple:
    """
    user_info JOIN evtable
    """
    check_user = db.query(UserInfoTable).filter(UserInfoTable.id == user_id).first()
    if not check_user:
        return (False, False, False)
    data = db.query(EvStationTable, UserFavoriteTable)\
        .filter(UserFavoriteTable.id == user_id)\
        .join(EvStationTable, UserFavoriteTable.statId==EvStationTable.statId).all()

    evtable_results = [i._mapping.get('EvStationTable').as_dict() for i in data]
    user_favorite_results = [i._mapping.get('UserFavoriteTable').as_dict()  for i in data]

    user_favorite_results = list(map(dict, set(tuple(sorted(d.items())) for d in user_favorite_results)))

    return (True, evtable_results, user_favorite_results)

def delete_favorites_query(db, user_id, stat_id) -> int:
    try:
        success = db.query(UserFavoriteTable).filter(
            UserFavoriteTable.id == user_id, 
            UserFavoriteTable.statId == stat_id
        ).delete()

        db.commit()
    finally:
        return success
    

def add_favorite_query(db, user_id, stat_id) -> tuple:
    """
    user_info add fav statId
    """
    is_not_found = False
    is_duplicated = False
    item = db.query(UserFavoriteTable).filter(
        UserFavoriteTable.id == user_id, 
        UserFavoriteTable.statId == stat_id).first() 
    if item: # user id 와 seq 가 중복
        is_duplicated = True
        return (is_not_found, is_duplicated, False)

    insert_fav = UserFavoriteTable()
    insert_fav.id = user_id
    insert_fav.statId = stat_id
    try:
        db.add(insert_fav)
        db.commit()
    except IntegrityError:
        is_not_found = True
        return (is_not_found, is_duplicated, False) # duplicated


    return (is_not_found, is_duplicated, True)