import json
from chalicelib.utils.utils import AlchemyEncoder
from chalicelib.tables.account_table import UserInfoTable
import time
def check_user_info_query(db, user_id, token, kind) -> list:
    user = db.query(UserInfoTable)\
			.filter(UserInfoTable.id == user_id)\
			.first()

    if user:
        user = db.query(UserInfoTable)\
			.filter(
				UserInfoTable.id == user_id,
				UserInfoTable.token == token
			).first()
        
        if not user:
            update_item = {
                'id': user_id,
                'kind': kind,
                'token': token,
                'login_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            }
            user = db.query(UserInfoTable).filter(UserInfoTable.id == user_id).update(update_item)
            # user.fmtoken = fmtoken # 의미를 모르겠음
            db.commit()

	# 결과가 없으면 insert
    else:
        insert_user = UserInfoTable()
        insert_user.id = user_id
        insert_user.kind = kind
        insert_user.token = token
        insert_user.login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # insert_user.fm_token = fmtoken

        db.add(insert_user)
        db.commit()

    user = db.query(UserInfoTable)\
		.filter(UserInfoTable.id == user_id)\
		.all()

    results = json.loads(json.dumps(user, cls=AlchemyEncoder))
    return results

def get_user_info_query(db, user_id: str, kind) -> list:
    results = db.query(UserInfoTable).filter(UserInfoTable.id == user_id, UserInfoTable.kind == kind).all()

    results = json.loads(json.dumps(results, cls=AlchemyEncoder))
    return results