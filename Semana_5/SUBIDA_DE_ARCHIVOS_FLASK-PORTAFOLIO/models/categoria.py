from config.base_datos import bd
from sqlalchemy import Column, types
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

class CategoriaModel(bd.Model):
    __tablename__='t_categoria'
    categoriaId= Column(
        name='cat_id',
        type_=types.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False
    )
    categoriaNombre= Column(
        name='cat_nombre',
        type_=types.String(45),
        nullable=False
    )
    categoriaOrden= Column(
        name='cat_orden',
        type_=types.Integer,
        nullable=False
    )
    categoriaEstado= Column(
        name='cat_estado',
        type_=types.Boolean(),
        nullable=False, #Valor por defecto por si no se ingresa uno
        default=True,
    )
    usuario = Column(
    ForeignKey('t_usuario.usuario_id'),
    name='usuario_id',
    type_=types.Integer,
    nullable=False
    )
    conocimientos = relationship('ConocimientoModel', backref='categoriaConocimientos', cascade='all , delete')

    def __init__(self, nombre, orden, estado, usuario):
        self.categoriaNombre= nombre
        self.categoriaOrden= orden
        self.usuario = usuario
        if estado:
            self.categoriaEstado = estado
    def save(self):
        bd.session.add(self)
        bd.session.commit()

    def delete(self):
        bd.session.delete(self)
        bd.session.commit()
    
    def json(self):
        return {
            'cat_id': self.categoriaId,
            'cat_nombre': self.categoriaNombre,
            'cat_orden': self.categoriaOrden,
            'cat_estado': self.categoriaEstado
        }