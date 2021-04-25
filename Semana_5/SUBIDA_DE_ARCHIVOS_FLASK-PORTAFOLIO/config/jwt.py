# funcion para customizar el emnsaje de erroral usar JWT

def manejo_error_jwt(error):
    print(error.status_code)
    print(error.error)
    print(error.description)
    print(error.headers)
    respuesta = {
        'success': False,
        'content': None,
        'message': None
    }
    if error.error == 'Invalid token':
        respuesta['message'] = 'Token invalida'
    elif error.error == 'Authorization Required':
        respuesta['message']= 'Se necesita una token para esta peticion'
    else:
        respuesta['message'] = 'Sucedio otro error, comuniquese con el backend'
    return respuesta, 401