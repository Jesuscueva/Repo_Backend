from config.seguridad import Usuario
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse
from models.categoria import CategoriaModel


class CategoriaController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument(
        'cat_nombre',
        required=True,
        type=str,
        help='Falta ingresar cat_nombre',
        location='json'
    )
    serializer.add_argument(
        'cat_orden',
        required=True,
        type= int,
        help='Falta ingresar cat_orden',
        location='json'
    )
    serializer.add_argument(
        'cat_estado',
        required=True,
        type= bool,
        help='Falta ingresar cat_estado',
        location='json'
    )
    @jwt_required()
    def post(self):
        print(current_identity)
        data = self.serializer.parse_args()
        nuevaCategoria = CategoriaModel( 
            data['cat_nombre'],
            data['cat_orden'],
            data['cat_estado'],
            current_identity['usuario_id']
        )
        nuevaCategoria.save()
        return {
            'success': True,
            'content': nuevaCategoria.json(),
            'message': "creado exitosamente"
        }, 201
    
    @jwt_required()
    def get(self):
        print(current_identity)
        categorias = CategoriaModel.query.filter_by(usuario=current_identity['usuario_id']).all()
        resultado = []
        for categoria in categorias:
            resultadoCategoria = categoria.json()
            conocimientos = []
            for conocimiento in categoria.conocimientos:
                conocimientos.append(conocimiento.json())
            resultadoCategoria['conocimiento'] = conocimientos 
            resultado.append(resultadoCategoria)
        print(categorias)
        return {
            'success': True,
            'content': resultado
        }
    @jwt_required()
    def delete(self, id):
        categoria = CategoriaModel.query.filter_by(categoriaId=id).first()
        categoria.delete()
        return {
            'success': True,
            'content': None,
            'message': "Se elimino correctamente"
        }