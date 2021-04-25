from models.sedeLibro import SedeLibroModel
from flask_restful import reqparse, Resource
from models.libro import LibroModel

serializer = reqparse.RequestParser()
serializer.add_argument(
    'libro_nombre',
    type= str,
    required = True,
    help = 'Falta agregar el libro_nombre',
    location = 'json'
)
serializer.add_argument(
    'libro_cant',
    type= int,
    required = True,
    help = 'Falta agregar el libro_cant',
    location = 'json'
)
serializer.add_argument(
    'libro_edicion',
    type= str,
    required = True,
    help = 'Falta agregar el libro_edicion',
    location = 'json'
)
serializer.add_argument(
    'autor_id',
    type= int,
    required = True,
    help = 'Falta agregar el autor_id',
    location = 'json'
)
serializer.add_argument(
    'categoria_id',
    type= int,
    required = True,
    help = 'Falta agregar el categoria_id',
    location = 'json'
)






class LibrosController(Resource):
    def post(self):
        data = serializer.parse_args()
        nuevoLibro = LibroModel(data['libro_nombre'], data['libro_cant'], data['libro_edicion'], data['autor_id'], data['categoria_id'])
        nuevoLibro.save()
        return {
            'success': True,
            'contenet': nuevoLibro.json(),
            'message': 'Se creo el libro exitosamente'
        }
    def get(self):
        libros = LibroModel.query.all()
        print(libros[0].autorLibro.json())
        print(libros[0].categoriaLibro.json())
        resultado = []
        for libro in libros:
            resultadoTemporal = libro.json()
            resultadoTemporal['autor'] = libro.autorLibro.json()
            resultadoTemporal['categoria'] = libro.categoriaLibro.json()
            del resultadoTemporal['autor_id'] #Forma de eliminar una llave de un diccionario
            del resultadoTemporal['categoria_id']
            resultado.append(resultadoTemporal)
            # resultado.append(libro.json())
        return{
            'success': True,
            'content': resultado,
            'message': "Data recibida"
        }
class RegistroLibroController(Resource):
    def post(self):
        serializer = reqparse.RequestParser(bundle_errors=True)
        serializer.add_argument(
            'libro_id',
            type=int,
            required=True,
            help='Falta el libro_id',
            location='json'
        )
        serializer.add_argument(
            'sedes',
            type=list,
            required=True,
            help='Falta las sedes',
            location='json'
        )
        data = serializer.parse_args()
        print(data)
        try:
            for sede in data['sedes']:
                print(sede)
                SedeLibroModel(sede['sede_id'], data['libro_id']).save()
            return{
                'success': True,
                'content': None,
                'message': 'Se vinculo correctamente el libro con las sedes'
            }, 201
        except: 
            return{
                'success': False,
                'content': None,
                'message': "Error al registrar los libros con las sedes, vuelva a intentarlo nuevamente"
            }, 500