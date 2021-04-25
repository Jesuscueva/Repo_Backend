import re
from flask_restful import Resource, reqparse
from models.sede import SedeModel

serializer = reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
    'sede_ubicacion',
    type=str,
    required= True,
    help='Falta la sede_ubicacion0',
    location='json',
    dest='ubicacion'
)
serializer.add_argument(
    'sede_latitud',
    type=float,
    required=True,
    help='Falta la sede_latitud',
    location='json',
    dest='latitud'
)
serializer.add_argument(
    'sede_longitud',
    type=float,
    required=True,
    help='Falta la sede_longitud',
    location='json',
    dest='longitud'
)

class SedeController(Resource):
    def post(self):
        data = serializer.parse_args()
        nuevaSede = SedeModel(data['ubicacion'], data['latitud'], data['longitud'])
        nuevaSede.save()
        return{
            'success': True,
            'content': nuevaSede.json(),
            'message': "Sede creada exitosamente"
        }, 201
    def get(self):
        sedes = SedeModel.query.all()
        resultado = []
        for sede in sedes:
            resultado.append(sede.json())
        return{
            'success': True,
            'content': resultado,
            'message': "llego la data"
        }


class LibroSedeController(Resource):
    def get(self, id_sede):
        sede = SedeModel.query.filter_by(sedeId = id_sede).first()
        print(sede.libro)
        sedeLibros = sede.libro
        libros=[]
        for sedeLibro in sedeLibros:
            # libros.append(sedeLibro.libroSede.json())
            libro = sedeLibro.libroSede.json()
            libro['autor'] = sedeLibro.libroSede.autorLibro.json()
            libro['categoria'] = sedeLibro.libroSede.categoriaLibro.json()
            del libro['categoria']['categoria_id']
            del libro['autor_id']
            libros.append(libro)
            # print(sedeLibro.libroSede.json())
        resultado = sede.json()
        resultado['libros'] = libros
        return{
            'success': True,
            'content': resultado
        }

class   LibroCategoriaSedeController(Resource):
    def get(self):
        serializer.remove_argument('sede_latitud')
        serializer.remove_argument('sede_ubicacion')
        serializer.remove_argument('sede_longitud')
        serializer.add_argument(
            'categoria',
            type=int,
            required=True,
            help='Falta colocar categoria',
            location='args'
        )
        serializer.add_argument(
            'sede',
            type=int,
            required=True,
            help='Falta la sede',
            location='args' #Sirve para que lo mande por el querystring ( de forma dinamica)
        )
        data = serializer.parse_args()
        sede = SedeModel.query.filter_by(sedeId = data['sede']).first()
        print(data)
        print("-------------------")
        sedes = sede.libro
        libros = []
        for sedelibrito in sedes:
            # data['categoria'] = sedelibrito.libroSede.categoriaLibro.json()
            # print(sedelibrito.libroSede.categoriaLibro.json())
            if(sedelibrito.libroSede.categoria == data['categoria']):
                libros.append(sedelibrito.libroSede.json())
        
        return{
            'succes': True,
            'content': libros
        }
