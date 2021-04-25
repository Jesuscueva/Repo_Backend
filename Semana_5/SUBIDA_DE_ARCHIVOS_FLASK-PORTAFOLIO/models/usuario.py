from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import String
import bcrypt
from config.base_datos import bd
from sqlalchemy import Column, types
class UsuarioModel(bd.Model):
    __tablename__= "t_usuario"
    usuarioId = Column(
        name="usuario_id",
        type_=types.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False
    )
    usuarioNombre = Column(
        name='usuario_nombre',
        type_=types.String(25),
        nullable=False
    )
    usuarioApellido= Column(
        name='usuario_apellido',
        type_=types.String(45),
        nullable='False'
    )
    usuarioCorreo= Column(
        name='usuario_correo',
        type_=types.String(45),
        nullable=False
    )
    usuarioPassword= Column(
        name='usuario_password',
        type_=types.TEXT,
        nullable=False
    )
    usuarioFoto= Column(
        name= 'usuario_foto',
        type_=types.TEXT,
        nullable=False
    )
    usuarioTitulo= Column(
        name='usuario_titulo',
        type_=types.String(45),
        nullable=False
    )
    usuarioInfo= Column(
        name='usuario_info',
        type_=types.TEXT,
        nullable=False
    )
    usuarioCV= Column(
        name='usuario_cv',
        type_=types.TEXT,
        nullable=False
    )
    usuarioSuperUser= Column(
        name='usuario_superuser',
        type_=types.Boolean(),
        nullable=False
    )

    def __init__(self, nombre, apellido, correo, password, titulo, información, curriculum, superusuario, foto):
        self.usuarioNombre = nombre
        self.usuarioApellido = apellido
        self.usuarioCorreo = correo
        self.usuarioTitulo = titulo
        self.usuarioInfo = información
        self.usuarioCV = curriculum
        self.usuarioSuperUser = superusuario
        self.usuarioFoto = foto
        # ENCRIPTO LA CONTRASEÑA
        # primero agarro la password y la convierto a bytes mediante el formato de escritura de utf-8
        password = bytes(password, 'utf-8')

        hash = bcrypt.hashpw(password, bcrypt.gensalt())

        self.usuarioPassword = hash.decode('utf-8')
    
    def save(self):
        bd.session.add(self)
        bd.session.commit()
    def json(self):
        return{
            'usuario_nombre': self.usuarioId,
            'usuario_apellido': self.usuarioNombre,
            'usuario_correo': self.usuarioCorreo,
            'usuario_titulo': self.usuarioTitulo,
            'usuario_info': self.usuarioInfo,
            'usuario_cv': self.usuarioCV,
            'usuario_foto': self.usuarioFoto
        }