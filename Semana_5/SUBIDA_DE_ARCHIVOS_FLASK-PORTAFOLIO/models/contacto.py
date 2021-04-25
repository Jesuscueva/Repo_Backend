from sqlalchemy.schema import ForeignKey
from config.base_datos import bd
from sqlalchemy import Column, types
from datetime import date, datetime

class ContactoModel(bd.Model):
    __tablename__='t_contacto'
    contactoId= Column(
        name='contacto_id',
        nullable=False,
        type_=types.Integer,
        unique=True,
        autoincrement=True,
        primary_key=True,
    )
    contactoNombre= Column(
        name='contacto_nombre',
        nullable=False,
        type_=types.String(45)
    )
    contactoEmail = Column(
        name='contacto_email',
        nullable=False,
        type_=types.String(45)
    )
    contactoFono=Column(
        name='contacto_fono',
        nullable=False,
        type_=types.String(10)
    )
    contactoMensaje=Column(
        name='conatcto_mensaje',
        nullable=False,
        type_=types.TEXT
    )
    contactoFecha=Column(
        name='contacto_fecha',
        nullable=False,
        type_=types.DateTime,
        default=datetime.now()
    )
    usuario = Column(
        ForeignKey('t_usuario.usuario_id'),
        name='usuario_id',
        nullable=False,
        type_=types.Integer
    )

    def __init__(self, nombre, correo, telefono, mensaje, fecha,usuario):
        self.contactoNombre=nombre
        self.contactoEmail= correo
        self.contactoFono=telefono
        self.contactoMensaje=mensaje
        self.contactoFecha=fecha
        self.usuario =usuario
    def save(self):
        bd.session.add(self)
        bd.session.commit()