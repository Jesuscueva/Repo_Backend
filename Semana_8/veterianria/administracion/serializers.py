from re import search
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from .models import ClienteModel, EspecieModel, MascotaModel, RazaModel

class MostrarRazaSerializers(serializers.ModelSerializer):
    class Meta: 
        model = RazaModel
        fields = "__all__"


class EspecieSerializers(serializers.ModelSerializer):
    raza = MostrarRazaSerializers(
        source="especiesRaza", many=True, read_only=True
    )
    def update(self):
        # el atributo instance es la instancia de la clase y me da acceso a todos los atributos de la clase 
        print(self.instance)
        # es la data mandada por el front pero que ya paso un filtro de validacion (que cumple con las condiciones definidas por el modelo ) y se genera cuando se llama al metodo is_valid()
        print(self.validated_data)
        self.instance.especieNombre = self.validated_data.get("especieNombre")
        #el metodo save() es  el metodo de los modelos que se encarga de hacer el guardado en la bd
        self.instance.especieEstado = self.validated_data.get("especieEstado")
        self.instance.save()
        return self.data
    def delete(self):
        self.instance.especieEstado = False
        self.instance.save()
        return self.instance
        # Forma 2
        """
            if(self.instance):
                self.instace.especieEstado = False
                self.instance.save()
                return self.instance
            return None
        """
    class Meta: 
        #Para que haga matvh von el model y oueda jalar las columnas con ssus propiedades{ <}
        model = EspecieModel
        fields =  "__all__"

        # si queremos usar la mayoria de campos y evitar una minoria => exclude = ["campos3", "campos4"]
        #NOTA: no se purfr  usar las dos a la vex


class RazaEscrituraSerializers(serializers.ModelSerializer):
    # especiePadre = EspecieSerializers(source="especie", read_only=True)
    # especie = serializers.IntegerField(write_only=True)
    # def save(self):
    #     print(self.validated.data)
    #     especieEncontrada = EspecieModel.objects.filter(especieId=self.validated.get("especie"))
    #     nuevaRaza = RazaModel(razaNombre=self.validated_data.get(
    #         "razaNombre"
    #     ), especie= especieEncontrada)
    #     nuevaRaza.save()
    #     return nuevaRaza
    class Meta:
        model = RazaModel
        fields = "__all__"
class EspecieVistaSerializar(serializers.ModelSerializer):
    class Meta:
        model = EspecieModel
        fields = "__all__"

class RazaVistaSerializar(serializers.ModelSerializer):
    especie = EspecieSerializers()
    class Meta :
        model = RazaModel
        fields = "__all__"
        
class MascotaSerializar(serializers.ModelSerializer):
    class Meta:
        model = MascotaModel
        fields = "__all__"

class ClienteSerializar(serializers.ModelSerializer):
    class Meta: 
        model = ClienteModel
        fields = "__all__"

class RegistroClienteSerializar(serializers.Serializer):
    # el valor del required x default es True
    # trim_whitespace lo que hace es remueve los espacios
    dni = serializers.CharField(max_length = 9, required= True, min_length= 8)
    email = serializers.EmailField(max_length= 45, trim_whitespace= True)
    telefono = serializers.CharField(max_length= 10, min_length= 4)
    direccion = serializers.CharField(max_length= 50)

class RazaSerializar(serializers.ModelSerializer):
    class Meta:
        model = RazaModel
        fields = '__all__'

class  MascotaRazaSerializar(serializers.ModelSerializer):
    raza = RazaSerializar()
    class Meta:
        model = MascotaModel
        fields = '__all__'

class  ClienteMascotaSerializar(serializers.ModelSerializer):
    mascotas  = MascotaRazaSerializar(source= 'mascotasCliente', many=True)
    class Meta:
        model = ClienteModel
        fields = '__all__'


