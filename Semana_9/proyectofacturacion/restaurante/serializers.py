from django.db.models import fields
from django.db.models.fields import files
from .models import *
from rest_framework import serializers

class PlatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatoModel
        fields = '__all__'

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True)

    def save(self):
        personalCorreo = self.validated_data.get('personalCorreo')
        personalTipo = self.validated_data.get('personalTipo')
        personalNombre = self.validated_data.get('personalNombre')
        personalApellido = self.validated_data.get('personalApellido')
        password= self.validated_data.get('password')
        is_staff = False
        nuevoPersonal = PersonalModel(
            personalCorreo = personalCorreo,
            personalTipo = personalTipo,
            personalNombre = personalNombre,
            personalApellido = personalApellido,
            is_staff = is_staff
        )
        # encriptamos la contraseña
        nuevoPersonal.set_password(password)
        nuevoPersonal.save()
        return nuevoPersonal

    class Meta: 
        model = PersonalModel
            #excluimos grupos porque no va a tener acceso al panel administrativo al igual que user_permissions (ambos sirven para indicar que puede hacer en el panel administrativo)
        exclude = ['groups', 'user_permissions']

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomPayloadSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(CustomPayloadSerializer, cls).get_token(user)
        # ya tenemos la token que se suele devolver de manera automatica
        token["personalTipo"]  = user.personalTipo
        return token

class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MesaModel
        fields = "__all__"

class DetallePedidoCreacionSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField(min_value=1)
    subtotal = serializers.DecimalField(max_digits=5, decimal_places=2)
    plato = serializers.IntegerField()

class NotaPedidoCreacionSerializer(serializers.Serializer):
    cliente = serializers.CharField(max_length = 50, min_length= 1)
    mesa = serializers.IntegerField()
    detalle = DetallePedidoCreacionSerializer(many=True)


class MostrarPlatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatoModel
        fields = ['platoDescripcion','platoFoto' ]

class MostrarDetallePedidoSerializer(serializers.ModelSerializer):
    plato = MostrarPlatoSerializer()
    class Meta:
        model = DetalleComandaModel
        fields = '__all__'

class MostrarPedidoSerializer(serializers.ModelSerializer):
    detalle = MostrarDetallePedidoSerializer(source= 'cabeceraDetalles', many=True)
    class Meta:
        model = CabeceraComandaModel
        fields = '__all__'

# Devolver todas las mesas de un mozo,
# Quitar el modelo persona_mesa y hacerlo mediante los comprobantes
# mandar el token del moxo y debera retornar todas sus mesas que ha atendido
# no importa si se repiten las mesas
# indicar el numero de mesa
# /mozo/mesas

class CabeceraNotaSerializer(serializers.ModelSerializer):
    mesa= MesaSerializer()
    class Meta:
        model = CabeceraComandaModel
        fields = ['mesa']

class MostrarMesasMozoSerializer(serializers.ModelSerializer):
    #ingresar a todos sus comandas cabecera y luego a sus mesas
    pedidos = CabeceraNotaSerializer(source='mozoCabecera', many=True)
    class Meta: 
        model = PersonalModel
        fields = '__all__'

class GenerarComprobanteSerializer(serializers.Serializer):
    tipo_comprobante = serializers.ChoiceField(choices=['BOLETA', 'FACTURA'])
    cliente_tipo_documento = serializers.ChoiceField(choices=['DNI', 'RUC'])
    cliente_documento = serializers.CharField(max_length=11, min_length=8)
    cliente_email = serializers.EmailField()
    observaciones =serializers.CharField(max_length=50)

class ComprobanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComprobanteModel
        fields = "__all__"