from flask import Flask, request, send_file
from flask_restful import Api
from config.base_datos import bd
# INSTAÑAR TODAS LAS LIBRERIAS
# pip install -r requirements.txt 
from controllers.usuario import RegistroController, LoginController
from controllers.redSocial import RedSocialControllers
from controllers.categoria import CategoriaController
from controllers.contacto import ContactoController
# from models.usuario import UsuarioModel
# from models.categoria import CategoriaModel
from models.conocimiento import ConocimientoModel
# from models.contacto import ContactoModel
# from models.redSocial import RedSocialModel
from models.usuarioRedSocial import UsuarioRedSocialModel
# Sirve para que el nombre del archivo que me manda el cliente lo valide antes de guardar y evita que se guarde nombre con caracteres especiales 
#que puedan malograr el funcionamiento de mi api
from werkzeug.utils import secure_filename
import os
from uuid import uuid4
from flask_jwt import JWT, jwt_required, current_identity
from config.seguridad import autenticador, identificador
from config.jwt import manejo_error_jwt
from datetime import timedelta

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:root@localhost:3306/portfolioFlask'
app.config['SQALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']= 'miclavesecreta' # ESTO USA FLASK-JWT PARA ENCRIPTAR LA TOKEN, ESTA SERA LA CONTRASEÑA PARAENCRIPTAR Y DESENCRIPTAR LA TOKEN
app.config['JWT_AUTH_URL_RULE']='/iniciarSesion'
app.config['JWT_AUTH_USERNAME_KEY']= "correo"
app.config['JWT_AUTH_PASSWORD_KEY']= "contraseña"
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
app.config['JWT_EXPIRATION_DELTA']= timedelta(minutes=10)

jsonwebtoken = JWT(app=app, authentication_handler=autenticador, identity_handler=identificador)
jsonwebtoken.jwt_error_callback = manejo_error_jwt

bd.init_app(app)
# bd.drop_all(app=app)
bd.create_all(app=app)

# Sirve para indicar en que parte del proyecto se va a almacenar los archivos subidos
UPLOAD_FOLDER= 'media'
EXTENSIONES_PERMITIDAS_IMEGENES = ['jpg', 'png']

def filtro_extensiones(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[-1].lower() in EXTENSIONES_PERMITIDAS_IMEGENES

@app.route('/uploadFile', methods=['POST'])
def subir_archivo():
    print(request.files)
    # primero validamos que no este pasando en el form-data la llave archivo
    if 'archivo' not in request.files:
        return {
            'success': False,
            'message': 'No hay archivo para subir',
            'content': None
        }, 400
    archivo = request.files['archivo']
    if archivo.filename == '':
        return {
            'success': False,
            'message': 'No hay archivo para subir',
            'content': None
        }, 400
    
    if filtro_extensiones(archivo.filename) is False:
        return {
            'content': None,
            'success':  False,
            'message': "Archivo no permitido" 
        }
    
    formato = archivo.filename.rsplit(".")[-1] 
    nombre_modificado= str(uuid4())+'.'+formato
    print(archivo.filename.rsplit(".")[-1])
    nombre_archivo = secure_filename(nombre_modificado)
    print(nombre_archivo)
    archivo.save(os.path.join(UPLOAD_FOLDER, nombre_archivo))
    
    return {
        'content': nombre_archivo,
        'success': True,
        'message': "se guardo el archivo exitosamente" 
        }, 201

@app.route('/devolverImagen/<string:nombre>', methods=['GET'])
def devolver_archivo(nombre):
    #el metodo send_file sirve para mandar cualquier tipo de archivos, si es un archivo imagen se mostrara caso contrario
    # se descargará
    try:
        return send_file(os.path.join(UPLOAD_FOLDER, nombre))
    except:
        return send_file(os.path.join(UPLOAD_FOLDER, 'default.png'))

@app.route('/eliminarImagen/<string:nombre>', methods=['DELETE'])
def remove_file(nombre):
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, nombre))
        return {
            'success': True,
            'content': 'Imagen eliminada exitosamente'
        }
    except:
        return {
            'success': False,
            'content': 'Imagen no encontrada'
        }

@app.route('/protegida')
@jwt_required()
def mostrar_saludo():
    print(current_identity)
    return {
        'mensaje': 'Hola'
    }

api.add_resource(RedSocialControllers, '/redsocial')
api.add_resource(RegistroController, '/registro')
api.add_resource(LoginController, '/login')
api.add_resource(CategoriaController, '/categoria', '/categoria/<int:id>')
api.add_resource(ContactoController, '/contacto')

if __name__ == '__main__':
    app.run(debug=True)