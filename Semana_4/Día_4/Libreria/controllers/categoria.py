from flask_restful import reqparse, Resource
from models.categoria import CategoriaModel

serializer = reqparse.RequestParser()
serializer.add_argument(
    'categoria_descripcion',
    type=str,
    required=True,
    help="Falta categoria_descripcion",
    location= 'json' # por defecto intenta buscar en todos los campos posibles y si lo encuentr no dara error pero si queremos indicar exactament porque medio me lo tiene que pasar debemos  indicar el location
)

class CategoriaController(Resource):
    def get(self):
        categorias = CategoriaModel.query.all()
        print(categorias)
        resultadoCategoria=[]
        for categoria in categorias:
            resultadoCategoria.append(categoria.json())
        return{
            'success': True,
            'contenet': resultadoCategoria,
            'message': "Data recibida"
        }
    def post(Self):
        data = serializer.parse_args()
        nuevaCategoria = CategoriaModel(data['categoria_descripcion'])
        nuevaCategoria.save()
        return {
            'success': True,
            'content': nuevaCategoria.json(),
            'message': 'Categoria creada exitosamente'
        }, 201