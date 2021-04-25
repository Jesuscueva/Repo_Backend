from sqlalchemy.sql.expression import null
from config.base_datos import bd
from sqlalchemy import Column, types

class RedSocialModel(bd.Model):
    __tablename__='t_red_social'
    redSocialId= Column(
        name='rs_id',
        type_=types.Integer,
        nullable=False,
        primary_key= True,
        unique=True,
        autoincrement=True
    )
    redSocialNombre= Column(
        name='rs_nombre',
        type_=types.String(45),
        nullable=False
    )
    redSocialImagen= Column(
        name='rs_imagen',
        type_=types.TEXT,
        nullable=False
    )
    def __init__(self, nombre, imagen):
        self.redSocialNombre = nombre
        self.redSocialImagen = imagen
    def json(self):
        return{
            'rs_id' :self.redSocialId,
            'rs_nombre': self.redSocialNombre,
            'rs_imagen' : self.redSocialImagen
        }
    def save(self):
        bd.session.add(self)
        bd.session.commit()