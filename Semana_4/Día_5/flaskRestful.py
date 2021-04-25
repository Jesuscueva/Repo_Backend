from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

app = Flask(__name__)
productos = []

# primero creo la instancia de mi clase API para poder declarar las rutas de mis Resource
api = Api(app)
# SI YO QUIERO PERMITIR TODOS LOS ACCESOS A TODOS LOS METODOS Y DEL CUALQUIER DOMINIO Y CUALQUIER HEADER
# PARA INDICAR QUE RECURSOS(RESOURCE) PUEDEN SER ACCEDIDOS SE TIENE QUE INDICAR QUE ENDPOINT Y QUE ORIGINES PUEDEN SER ACCEDIDOS
CORS(app, 
      # resource captura un diccionario en la llave se debe indicar los endpoints que vamos a declarar seguido de su lista de argumentos en el cual pueden ser los "origins" (origenes), "methods" (metodos), "headers" (cabeceras), defecto: * 
    #  resources={r"/producto/*":{"origins":"*"}, "/almacen":{"origins":"mipagina.com"}}, 
    #  origins=['mipagina.com','otrapagina.com'], # sirve para indicar que dominios pueden acceder a mi API, defecto: *
    #  methods=['POST', 'PUT', 'DELETE', 'GET'], # para indicar que metodos pueden acceder a nuesta API , por defecto el GET siempre va a poder, defecto: *
    )
@app.route('/', methods=['GET', 'POST'])
def start():
    return "Bienvenido"

  # ESTE ES MI VALIDAOR QUE SE VA A ENCARGAR DE FILTRAR ANTES DE PROCEDER CON LA LOGICA
serializer = reqparse.RequestParser()
serializer.add_argument(
    'producto_nombre',
    type=str,
    required=True,
    help='Falta el producto_nombre',
    location='json'
)
serializer.add_argument(
    'producto_precio',
    type=float,
    required=True,
    help='Falta el producto_precio',
    location='json'
)
serializer.add_argument(
    'producto_cantidad',
    type=int,
    required=True,
    help='Falta el producto_cantidad',
    location='json'
)


# el servicio restful
class Producto(Resource):
    def post(self):
        print('Ingreso al post')
        #Request.data devielve todo lo que manda el front en formato texto plano
        # request.get_json() devuelve lo que manda el front pero en formato de diccionario
        # nuevoProducto= request.get_json()
        nuevoProducto= serializer.parse_args()
        productos.append(nuevoProducto)
        return {
                'success':True,
                'content': nuevoProducto,
                'message': 'Producto creado exitosamente'
                }, 201
    # devolver todos los productos
    def get(self):
        return{
            'succes': True,
            'content': productos,
            'message': None
        }

class ProductoUnico(Resource):
    def get(self, id):
        #devolver producto segun id
        longitud_lista = len(productos)
        if longitud_lista > id:
            return{
                'success': True,
                'content': productos[id],
                'message': None
            }
        else:
            return{
                'success': False,
                'content': None,
                'message': 'Producto con id {} no existe'.format(id)
            }, 400
        pass    
    def put(self, id):
      
        # MEDIANTE EL METODO PARSE_ARGS() RECIEN SE HACE LA VALIDACION DE LOS PARAMETROS SOLICITADOS Y SI TODO ESTA
        # BIEN, DEVOLVERA LOS ARGUMENTOS EN FORMA DE UN DICCIONARIO
        # SI ES VALIDO MODIFICAR ESA POSICIÓN
        # SI ES INVALIDO INDICAR QUE EL ID ES INCORRECTO
        longitud = len(productos)
        data = serializer.parse_args()
        if longitud > id:
            #existe
            productos[id] = data
            return{
                'success':True,
                'contenet': productos[id],
                'message': 'Producto actualizado con exito'
            }, 201
        else:
            #no existe
            return {
                'success': False,
                'contenet': None,
                'message': 'Productocon id {} no existe'.format(id)
            }
    
    def delete(self, id):
        longitud = len(productos)
        if longitud > id:
            #existe
            productos.pop(id)
            return{
                'success':True,
                'contenet': None,
                'message': 'Producto eliminado con exito'
            }, 201
        else:
            #no existe
            return {
                'success': False,
                'contenet': None,
                'message': 'Productocon id {} no existe'.format(id)
            }

api.add_resource(Producto, '/producto', '/otro')
api.add_resource(ProductoUnico, '/producto/<int:id>')

app.run(debug=True, port=5001)