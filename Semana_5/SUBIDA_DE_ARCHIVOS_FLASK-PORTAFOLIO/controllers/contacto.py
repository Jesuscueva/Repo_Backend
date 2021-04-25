from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.contacto import ContactoModel
from config.utils import enviarCorreo

class ContactoController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    # @jwt_required()
    def post(self):
        
        self.serializer.add_argument(
            'contacto_nombre',
            type=str,
            required=True,
            help="Falta el contacto_nombre",
            location='json'
        )
        self.serializer.add_argument(
            'contacto_email',
            type=str,
            required=True,
            help="Falta el contacto_email",
            location='json'
        )
        self.serializer.add_argument(
            'contacto_fono',
            type=str,
            required=True,
            help="Falta el contacto_fono",
            location='json'
        )
        self.serializer.add_argument(
            'contacto_mensaje',
            type=str,
            required=True,
            help="Falta el contacto_mensaje",
            location='json'
        )
        self.serializer.add_argument(
            'contacto_fecha',
            type=str,
            required=True,
            help="Falta el contacto_fecha",
            location='json'
        )
        self.serializer.add_argument(
            'usuario_id',
            type=int,
            required=True,
            help="Falta el usuario",
            location='json'
        )
        data = self.serializer.parse_args()
        nuevoContacto = ContactoModel(
            data['contacto_nombre'],
            data['contacto_email'],
            data['contacto_fono'],
            data['contacto_mensaje'],
            data['contacto_fecha'],
            data['usuario_id']
        )
        nuevoContacto.save()
        if enviarCorreo(data['contacto_email'], data['contacto_nombre']):
            return {
                'success': True,
                'content': None,
                'message': "Creado exitosamente"
            }
        else:
            return {
                'success': False,
                'content': None,
                'message': "Hubo un error al enviar correo"
            }
    def get(self):
        pass