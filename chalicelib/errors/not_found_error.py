from chalice import Response

def not_found_error(message: str):
    return Response(
        status_code=404, 
        body=f'Not Found : {message}', 
    )