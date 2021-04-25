import re
from models.usuario import UsuarioModel
import bcrypt

class Usuario(object):
    def __init__(self,  id, username):
        self.id = id
        self.username = username
    
    def __str__(self):
        return "Usuario con el id='%s' y username='%s'"%(self.id, self.username)
    
def autenticador(username, password):
    """Este es el metodo encargado en mi JWT de validar que las credenciales
    fueron ingresadas correctamente
    """
    if username and password:
        # Ahora valido si ese usuario existe en la base de datos
        usuario= UsuarioModel.query.filter_by(usuarioCorreo=username).first()
        if usuario:
            if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(usuario.usuarioPassword, 'utf-8')):
                print("correctamente logeado")
                return Usuario(usuario.usuarioId, usuario.usuarioCorreo)
            else:
                print("La contraseña no coincide")
                return None
        else:
            print("No se encontro usuario")
    else:
        print('Falta el usuario o la password')
        return None

def identificador(payload):
    """Este es el metodo encargado en mi JWT de validar que las credenciales
    fueron ingresadas correctamente
    """
    print(payload)
    if payload['identity']:
        usuario = UsuarioModel.query.filter_by(usuarioId=payload['identity']).first()
        if usuario:
            return {
                "usuario_id": usuario.usuarioId,
                "usuario_correo": usuario.usuarioCorreo,
                "usuario_superuser": usuario.usuarioSuperUser
            }
        else:
            # el usuario en la token no existe en mi bd (eso es imposible)
            return None
    else:
        #en mi payload no hay nada almacenado en mi llave identity
        return None
