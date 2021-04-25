from re import L
from flask import Flask, request
from flask_restful import Api
from config.base_datos import bd
from controllers.autor import AutoresController, AutorController
from controllers.categoria import CategoriaController
from controllers.libro import LibrosController, LibroModel, RegistroLibroController
from controllers.sede import SedeController, LibroSedeController, LibroCategoriaSedeController

# from models.autor import AutorModel
# from models.libro import LibroModel
# from models.sede import SedeModel
# from models.categoria import CategoriaModel
# from models.sedeLibro import SedeLibroModel
from flask_cors import CORS
# para la documentacion 
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '' # esta variable se usa para indicar en que endpoint se encontrará la documentación
API_URL = '/static/swagger.json'
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config= {
        'app_name' : "Libreria Flask - Swagger Documentacion"
    }
)
app = Flask(__name__)
app.register_blueprint(swagger_blueprint)
#formato://useername:password@host:port/databasename
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/flasklibreria'
api = Api(app)
print(app.config)
CORS(app) # PERMITIENDO TODOS LOS METODOS, DOMINIOS Y HEADERS

#para evitar el warning de la funcionalidad de sqlalchemy de track modificacion:
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#inicio a la aplicación proveyendo las credenciales indicadas en el app.config pero aun no se ha conectado a la bd
bd.init_app(app)
# bd.drop_all(app=app)
#recien se conecta a ua base de datos en mysql deberemos instslar : pip install mysqlclient
bd.create_all(app=app)


@app.route('/buscar')
def buscarLibro():
    print(request.args.get('palabra'))
    palabra = request.args.get('palabra')
    if palabra:
        resultadoBusqueda = LibroModel.query.filter(LibroModel.libroNombre.like('%' + palabra + '%')).all()
        if resultadoBusqueda:
            resultado =[]
            for libro in resultadoBusqueda:
                resultado.append(libro.json())
            return{
                'success': True,
                'contenet': resultado,
                'message': None
            }
    return{
        'success': False,
        'contenet': None,
        'message': "No se encontro nada para buscar o la busqueda no tuvo exito"
    }, 400

#RUTAS DE MI API 
api.add_resource(AutoresController, '/autores')
api.add_resource(AutorController, '/autor/<int:id>')

api.add_resource(CategoriaController, '/categorias', '/categoria')

api.add_resource(LibrosController, '/libro', '/libros')

api.add_resource(SedeController, '/sedes', '/sede')
api.add_resource(LibroSedeController, '/sedeLibros/<int:id_sede>')
api.add_resource(LibroCategoriaSedeController, '/busquedaLibroSedeCat')
api.add_resource(RegistroLibroController, '/registrarSedesLibro')



if __name__ == '__main__':
    app.run(debug=True)