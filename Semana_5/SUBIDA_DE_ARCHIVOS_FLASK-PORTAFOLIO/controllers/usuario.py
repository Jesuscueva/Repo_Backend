import bcrypt
from models.usuario import UsuarioModel
from flask_restful import Resource, reqparse

class RegistroController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument(
        'usuario_nombre',
        type=str,
        required=True,
        help='Falta el usuario_nombre',
        location='json'
    )
    serializer.add_argument(
        'usuario_apellido',
        type=str,
        required=True,
        help='Falta el usuario_apellido',
        location='json'
    )
    serializer.add_argument(
        'usuario_correo',
        type=str,
        required=True,
        help='Falta el usuario_correo',
        location='json'
    )
    serializer.add_argument(
        'usuario_titulo',
        type=str,
        required=True,
        help='Falta el usuario_titulo',
        location='json'
    )
    serializer.add_argument(
        'usuario_info',
        type=str,
        required=True,
        help='Falta el usuario_info',
        location='json'
    )
    serializer.add_argument(
        'usuario_cv',
        type=str,
        required=True,
        help='Falta el usuario_cv',
        location='json'
    )
    serializer.add_argument(
        'usuario_superuser',
        type=bool,
        required=True,
        help='Falta el usuario_superuser',
        location='json'
    )
    serializer.add_argument(
        'usuario_password',
        type=str,
        required=True,
        help='Falta el usuario_password',
        location='json'
    )
    serializer.add_argument(
        'usuario_foto',
        type=str,
        help='Falta el usuario_foto',
        location='json'
    )

    def post(self):
        data = self.serializer.parse_args()
        nuevoUsuario = UsuarioModel(data['usuario_nombre'],
                        data['usuario_apellido'],
                        data['usuario_correo'],
                        data['usuario_password'],
                        data['usuario_titulo'],
                        data['usuario_info'],
                        data['usuario_cv'],
                        data['usuario_superuser'],  
                        data['usuario_foto'])
        nuevoUsuario.save()
        return {
            'success': True,
            'content': nuevoUsuario.json(),
            'message': 'Usuario creado exitosamente'
        },201

class LoginController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument(
        'correo',
        type=str,
        required=True,
        help='Falta el correo',
        location='json'
    )
    serializer.add_argument(
        'password',
        required=True,
        type=str,
        help='Falta el password',
        location='json'
    )
    def post(self):
        data = self.serializer.parse_args()
        print(data['correo'])
        print(UsuarioModel.query.all()[0])
        usuario = UsuarioModel.query.filter_by(usuarioCorreo =data['correo']).first()
        print(usuario)
        if usuario:
            password = bytes(data['password'], 'utf-8')
            hash = bytes(usuario.usuarioPassword, 'utf-8')
            if bcrypt.checkpw(password, hash):
                print("las contrseñas coinciden")
            else:
                print('las contraseñas no coinciden')
        return{
            'success': True
        }