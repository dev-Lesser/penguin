from chalice import Response

def bad_request_error(message: str):
    return Response(
        status_code=400, 
        body=f'Bad Request : {message}', 
    )