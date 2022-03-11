from chalice import Chalice, Response
from chalicelib.services.evstation_service import evstation_service_route
from chalicelib.services.account_login_service import account_login_service_route
from chalicelib.services.user_favorite_service import user_favorite_route


# from chalicelib.routers.firebase_router import firebase_route
app = Chalice(app_name='penguin')

# ADD 공간쿼리 blueprint
app.register_blueprint(evstation_service_route) 

# login blueprint
app.register_blueprint(account_login_service_route) 

# user favorite blueprint
app.register_blueprint(user_favorite_route) 

# using firebase  blueprint
# app.register_blueprint(firebase_route)

# [TODO] App version parameter 관리
@app.route('/')
def index():
    return Response(
        body={'messege':'success'},
        status_code=200
    )
