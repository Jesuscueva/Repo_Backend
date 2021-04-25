from enum import unique
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.expression import false
from config.base_datos import bd
from sqlalchemy import Column, types

class ConocimientoModel(bd.Model):
    __tablename__='t_conocimiento'
    conocimientoId = Column(
        name='conocimiento_id',
        type_= types.Integer,
        nullable= False,
        primary_key=True,
        unique=True,
        autoincrement=True
    )
    conocimientoTitulo = Column(
        name='conocimiento_titulo',
        type_= types.String(45),
        nullable=False 
    )
    conocimientoPuntuacion = Column(
        name='conocimiento_puntuacion',
        type_= types.DECIMAL(2,1),
        nullable= False 
    )
    conocimientoImagenTN = Column(
        name='conocimiento_imagen_thumbnail',
        type_= types.TEXT,
        nullable= False
    )
    conocimientoImagenLarge = Column(
        name='conociniemto_imagen_large',
        type_= types.TEXT,
        nullable= false
    )
    conocimientoDescripcion = Column(
        name='conocimiento_descripcion',
        type_= types.String(200),
        nullable= False
    )

    categoria = Column(
        ForeignKey('t_categoria.cat_id'),
        name='cat_id',
        type_=types.Integer,
        nullable=False
    )


    def __init__(self, titulo, puntuacion, imagentn, imagenl, descripcion, categoria):
        self.conocimientoTitulo = titulo
        self.conocimientoPuntuacion = puntuacion
        self.conocimientoImagenTN = imagentn
        self.conocimientoImagenLarge = imagenl,
        self.conocimientoDescripcion = descripcion
        self.categoria = categoria
    
    def save(self):
        bd.session.add(self)
        bd.session.commit()

    def json(self):
        return {
            'conocimiento_id': self.conocimientoId,
            'conocimiento_titulo': self.conocimientoTitulo,
            'conocimiento_puntuacion': str(self.conocimientoPuntuacion),
            'conocimiento_imagen_thumbnail': self.conocimientoImagenTN,
            'conocimiento_imagen_large': self.conocimientoImagenLarge,
            'conocimiento_descripcion': self.conocimientoDescripcion,
            'cat_id': self.categoria,
        }