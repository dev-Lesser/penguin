import os
import firebase_admin
from firebase_admin import credentials, messaging

class FirebaseMessage:
    auth_path = os.environ['FIREBASE_AUTH_PATH']
    cred = credentials.Certificate(auth_path)
    firebase_admin.initialize_app(cred)

    def send_message(self,token,name):
        message = messaging.Message(
            notification = messaging.Notification(
                title='안녕하세요 스마트차징입니다 ',
                body=name+'님 안녕하세요 방문해주셔서 반갑습니다',
            ),
            token=token,
        )


        response = messaging.send(message)
        return response