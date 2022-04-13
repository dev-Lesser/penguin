from chalice import Response

def auth_fail_error(message: str):
    return Response(
        status_code=404, 
        body=f'Auth failed : {message}', 
    )