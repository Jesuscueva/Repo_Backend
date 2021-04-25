from config.seguridad import Usuario
from flask.globals import request
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse
from models.redSocial import RedSocialModel

class RedSocialControllers(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument(
        'rs_nombre',
        type=str,
        required=True,
        help='Falta el rs_nombre',
        location='json'
    )
    serializer.add_argument(
        'rs_imagen',
        type=str,
        required=True,
        help='Falta el rs_imagen',
        location='json'
    )
    @jwt_required()
    def post(self):
        print(current_identity)
        # Solamente un usuario que es super usuario puede hacer un registro, sino indicar que no tiene los privilegios suficientes
        identidad_usuario = current_identity
        
        if identidad_usuario['usuario_superuser']:
            data = self.serializer.parse_args()
            nuevaRedSocial = RedSocialModel(data['rs_nombre'], data['rs_imagen'])
            nuevaRedSocial.save()
            return{
            'success': True,
            'content': nuevaRedSocial.json(),
            'message':'se creo la nueva red social'
            }
        else:
            return {
                'success': False,
                'content': None,
                'message': 'Usuario no dispone de suficiente privilegios'
            }
            
        
    def put(self):
        pass
    def get(self):
        print(request.host_url)
        lista_redes= RedSocialModel.query.all()
        resultado = []
        for red in lista_redes:
            temporal = red.json()
            temporal['rs_imagen']= request.host_url+'devolverImagen/'+temporal['rs_imagen']
            resultado.append(temporal)
        return {
            'success': True,
            'content': resultado,
            'message': None
        }
