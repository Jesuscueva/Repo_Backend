from django import db
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.expressions import F
from .authmanager import UsuarioManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.
class PersonalModel(AbstractBaseUser, PermissionsMixin):
    """ Modelo de la base de datos del personal del sistema"""
    TIPO_PERSONAL = [
        (1, 'ADMINISTRADOR'),
        (2, 'CAJERO'),
        (3, 'MOZO')
    ]
    # si no definimos una PK django creara una automaticamente y le pondra de nombre de columna od
    personalId = models.AutoField(
        primary_key=True,
        unique=True,
        db_column='personal_id'
    )
    personalCorreo = models.EmailField(
        unique=True,
        max_length=30,
        db_column='personal_correo',
        verbose_name='Correo del usuario'
    )
    personalTipo = models.IntegerField(
        db_column='personal_tipo',
        choices=TIPO_PERSONAL,
        verbose_name='Tipo del usuario'
    )
    personalNombre = models.CharField(
        max_length=45,
        null=False,
        db_column='personal_nombre'
    )
    personalApellido = models.CharField(
        max_length=45,
        null=False,
        db_column='personal_apellido'
    )
    password = models.TextField(
        db_column='personal_password',
        verbose_name='Contraseña del personal'
    )

    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )

    # aca asignamos el comportamiento con el modelo
    objects = UsuarioManager()
    # ahora indico que columna va ser la encargada del login
    # hace esa columna unica y null=False
    USERNAME_FIELD = 'personalCorreo'
    # sirve para solicitar los campos al momento de crear el supersusuario por consola
    # EXCLUSIVAMENTE
    REQUIRED_FIELDS = [ 'personalNombre','personalTipo', 'personalApellido']

    class Meta:
        db_table = 't_personal'
        verbose_name = 'personal'
        verbose_name_plural = 'personales'

class MesaModel(models.Model):
    mesaId = models.AutoField(
        primary_key=True,
        db_column='mesa_id',
        null=False
    )
    mesaNumero = models.CharField(
        db_column="mesa_numero",
        max_length=10,
        null=False,
        verbose_name="Numero de mesa"
    )
    mesaCapacidad = models.IntegerField(
        db_column='mesa_capacidad',
        null=False,

    )
    mesaEstado = models.BooleanField(
        db_column='mesa_estado',
        null=False,
        verbose_name='estado de la mes',
        default=True
    )
    class Meta:
        db_table= "t_mesa"
        verbose_name = "Mesa"

class PlatoModel(models.Model):
    platoId = models.AutoField(
        primary_key=True,
        db_column="plato_id",
        null=False
    )
    platoDescripcion = models.CharField(
        db_column="plato_descripcion",
        null= False,
        verbose_name="Nombre del plato",
        max_length=50
    )
    platoCantidad = models.IntegerField(
        db_column="plato_cantidad",
        verbose_name="Cantidad de los platos",
        null=False
    )
    platoFoto = models.ImageField(
        upload_to='platos/',
        db_column="plato_foto",
        verbose_name="Foto del plato",
        null= False
    )
    platoPrecio = models.DecimalField(
        db_column="plato_precio",
        max_digits=5,
        decimal_places=2,
        null=False,
        verbose_name="Precio del plato"
    )
    #campos de auditoria
    # sirve para que cuando se registre un nuevo plato se sobreescriba automaticamente la fecha y  hora del servidor
    createdAt = models.DateTimeField(
        auto_now_add=True,
        db_column= "create_at"
    )
    # sirve para que cuando se actualice un plato se sobreescriba automaticamente la fecha y hora del servidor
    updatedAt = models.DateTimeField(
        auto_now= True,
        db_column= "updated_at"
    )
    class Meta: 
        db_table = "t_plato"
        verbose_name= "Plato"


# class PersonalMesaModel(models.Model):
#     personalId = models.ForeignKey(
#         to=PersonalModel,
#         on_delete=models.CASCADE,
#         related_name='personalMesas',
#         db_column='personal_id'
#     )
#     mesaId = models.ForeignKey(
#         to=MesaModel,
#         on_delete=models.CASCADE,
#         related_name='mesaPersonales',
#         db_column='mesa_id'
#     )
#     class Meta:
#         db_table = 't_personal_mesa'
#         verbose_name = 'personal mesa'

class ComprobanteModel(models.Model):
    TIPO_COMPROBANTE = [
        (1, "BOLETA"),
        (2, "FACTURA")
    ]
    comprobanteId = models.AutoField(
        primary_key=True,
        unique=True,
        db_column="comprobante_id"
    )
    comprobanteSerie = models.CharField(
        max_length= 4,
        db_column="comprobante_serie"
    )
    comprobanteTipo = models.IntegerField(
        choices= TIPO_COMPROBANTE,
        db_column= "comprobante_tipo",
        null= False
    )
    comprobanteNumero = models.IntegerField(
        db_column="comprobante_numero"
    )
    comprobantePdf = models.URLField(
        db_column= "comprobante_pdf"
    )
    comprobanteCdr = models.URLField(
        db_column="comprobante_cdr",
        null=True
    )
    comprobanteXml = models.URLField(
        db_column="comprobante_xml"
    )
    comprobanteRuc = models.URLField(
        db_column="comprobante_ruc",
        max_length= 11
    )
    class Meta:
        db_table = "t_comprobante"
        verbose_name = "comprobante"

class CabeceraComandaModel(models.Model):
    cabeceraId = models.AutoField(
        primary_key=True,
        unique= True,
        db_column='cabecera_id'
    )
    cabeceraFecha = models.DateField(
        db_column='cabecera_fecha',
        null=False
    )
    cabeceraTotal = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        db_column='cabecera_total',
        null= False
    )
    cabeceraCliente = models.TextField(
        db_column="cabecera_cliente",
        null=False
    )
    mozo = models.ForeignKey(
        to=PersonalModel,
        on_delete=models.PROTECT,
        db_column="mozo_id",
        related_name="mozoCabecera",
        null=False
    )
    mesa = models.ForeignKey(
        to= MesaModel,
        on_delete=models.PROTECT,
        db_column="mesa_id",
        related_name="mesaCabeceras",
        null=False
    )
    comprobante = models.ForeignKey(
        to=ComprobanteModel,
        db_column="comprobante_id",
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "t_comanda_cabecera"
        verbose_name = "comanda cabecera"

class DetalleComandaModel(models.Model):
    detalleId = models.AutoField(
        db_column= "detalle_id",
        unique=True,
        null=False,
        primary_key=True
    )
    detalleCantidad = models.IntegerField(
        db_column= "detalle_cantidad"
    )
    detalleSubtotal = models.DecimalField(
        db_column= "detalle_subtotal",
        decimal_places=2,
        max_digits=5
    )
    plato = models.ForeignKey(
        to=PlatoModel,
        db_column="plato_id",
        on_delete= models.PROTECT,
        related_name= "PlatoDetalles",
        null=False
    )
    cabecera = models.ForeignKey(
        to=CabeceraComandaModel,
        db_column= "cabecera_id",
        on_delete=models.PROTECT,
        related_name= "cabeceraDetalles",
        null=False
    )
    class Meta: 
        db_table = "t_comanda_detalle"
        verbose_name = "detalle comanda"