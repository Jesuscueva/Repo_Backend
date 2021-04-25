import re
import requests
from requests import api
from rest_framework.decorators import api_view
from datetime import date
from rest_framework import response
from .serializers import (ClienteMascotaSerializar, ClienteSerializar, EspecieSerializers,
                          RazaEscrituraSerializers, RazaVistaSerializar, MascotaSerializar, RegistroClienteSerializar)
from .models import ClienteModel, EspecieModel, MascotaModel, RazaModel
from rest_framework import serializers, status
from django.db.models import Count

from .utils import consultarDNI

# Las vistass genericas sirven para ya no hacer mucho codigo pero no estamos estandarizando las respuestas de nuestra api (si da error lanzará m status 500 sin ningun mensaje), si hay info retornara una lista o un objeto, si no mandamos la data correctamente  solamente nos mostrará el mensaje de error
# obviamente estas vistas genericas se pueden modificar y se pueden alterar segun nuestros requerimientos
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
# Sirve para devolver una respuesta mejor elaborada al usuario
from rest_framework.response import Response
from rest_framework.views import APIView

# Las APIViews sirven para darnos ya los metodos que pueden ser accedidos a esta clase, en el sigueiente casp sera el metodo GET, POST


class EspeciesController(ListCreateAPIView):
    # queryset es la consulta que se realizará a la bd en todo el controlador
    queryset = EspecieModel.objects.all()  # SELECT * FROM t_especie
    serializer_class = EspecieSerializers

    def get(self, request):
        # en el request se almacena todos los datos del front (headers, bodu, cookies, etc)
        print(self.queryset)
        respuesta = self.serializer_class(
            instance=self.get_queryset(), many=True)
        print(respuesta)
        return Response(data={
            "success": True,
            "content": respuesta.data,
            "message": None
        }, status=200)

    def post(self, request):
        # La forma de capturar lo que me esta mandando el lient es mediante el request
        # request.data
        # print(request.data)
        data = self.serializer_class(data=request.data)
        # el metodo is_valid() se encarga de validar si la data que se da es la indicada para usarse en el modelo
        # NOTA:  solo se puede usar ese metodo cuando le pasamos el parametro data
        # Si indicamos el parametro raise_exceptiom = True este detendrá el procedimiento habitual  y para todo para responder lose errores que esten en el servidor
        print(data.is_valid())
        # Si queremos manejar los errores tendremos que usar el atribot errors del serializar y ahi nos detallara todos los errores del porq la data no es valida
        # el atributo erros se genera despues de haber llamado al metodo is_valid() y si su resultado es false
        print(data.errors)
        if (data.is_valid()):
            # serializer_class al ser un serializador de tipo SerializerModel ya trae un metodo predeterminado llamado save()
            # el cual se encargara de guardar el nuevo registro en la bd
            data.save()
            # si queremos la data de ese nuevo registro usaremos su atributo .data que nos devolvera un diccioranrio con la nueva informacion guardada en la bd
            return Response(data={
                "success": True,
                "content": None,
                "message": None
            }, status=200)
        else:
            print(data.errors.get("especieNombre")[0])
            texto = "{} ya se encuentra registrado!".format(
                request.data.get("especieNombre")
            )
            data.errors.get("especieNombre")[0] = texto
            return Response(data={
                "success": False,
                "content": data.errors,
                "message": "Hubo un error al guardar la especie"
            }, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request):
    #     return Response("ok")


class EspecieController(RetrieveUpdateDestroyAPIView):
    queryset = EspecieModel.objects.all()
    serializer_class = EspecieSerializers

    def get_queryset(self, id):
        return EspecieModel.objects.filter(especieId=id).first()

    def get(self, request, id):
        especie = self.get_queryset(id)
        print(especie.especiesRaza.all())
        respuesta = self.serializer_class(instance=especie)
        # FORMA #1:
        # respuest.data.get("especieId")
        # Forma #2:
        # respuesta.instance
        # Forma #3:
        if especie:
            return Response(data={
                "success": True,
                "content": respuesta.data,
                "message": None
            })
        return Response(data={
            "success": True,
            "content": None,
            "message": "No se encuentra la especie con D {}".format(id)
        })

    def put(self, request, id):
        especie = self.get_queryset(id)
        respuesta = self.serializer_class(instance=especie, data=request.data)
        if respuesta.is_valid():
            resultado = respuesta.update()
            print(resultado)
            return Response(data={
                "success": True,
                "content": resultado,
                "message": "Se actualizo correctamente la data"
            })
        else:
            return Response(data={
                "success": False,
                "content": respuesta.errors,
                "message": "Data incorrecta"
            })

    def delete(self, request, id):
        # 1. Agregar una columna en la tabla especie que sea "especieEstado" que sea boolean y que x defecto sea true y no puede ser vacio
        # 2. Modificar el metodo update para que admita el estado
        # 3. al momento de hacer delete NO ELIMINAR la especie sino cambiar su estado a False (inhabilitado)
        # 4. Indicar al usuario que se inhabilito correctamente la especie
        consulta = self.get_queryset(id)
        if consulta:
            respuesta = self.serializer_class(instance=consulta)
            respuesta.delete()
            return Response(data={
                "success": True,
                "content": None,
                "message": "se inhabilito la especie exitosamente"
            })
        else:
            return Response(data={
                "success": False,
                "content": None,
                "message": "Especie no existe"
            })


class RazasController(ListCreateAPIView):
    queryset = RazaModel.objects.all()
    serializer_class = RazaEscrituraSerializers

    def post(self, request):
        print(request.data)
        respuesta = self.serializer_class(data=request.data)
        if respuesta.is_valid(raise_exception=True):
            respuesta.save()
            return Response(data={
                "success": True,
                "content": respuesta.data,
                "message": "Raza creada exitosamente"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                "success": False,
                "content": respuesta.errors,
                "message": "Data incorrecta"
            }, status=status.HTTP_400_BAD_REQUEST)

    def filtrar_razas(self):
        razas = RazaModel.objects.all()
        resultado = []
        for raza in razas:
            if (raza.especie.especieEstado is True):
                resultado.append(raza)
        return resultado

    def get(self, request):
        respuesta = RazaVistaSerializar(
            instance=self.filtrar_razas(), many=True)
        return Response(data={
            "success": True,
            "content": respuesta.data,
            "message": None
        })


class MascotasController(ListCreateAPIView):
    queryset = MascotaModel.objects.all()
    serializers_class = MascotaSerializar

    def post(self, request):
        resultado = self.serializers_class(data=request.data)
        if resultado.is_valid():
            resultado.save()
            return Response({
                "success": True,
                "content": resultado.data,
                "message": "Mascota registrada exitosamente"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "content": resultado.errors,
                "message": "Hubo un error al registrar ña mascota"
            }, status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        resultado = self.serializers_class(
            instance=self.get_queryset(), many=True)

        return Response({
            "success": True,
            "content": resultado.data,
            "message": None
        })


# Luego de usar las vistas genericas podemos tambien utilizar algunas vistas con total control de nuestros metodos, se puede realizar en forma de una clase o en forma de una funcion

# Al usar Apiviews no tenemos que indicar a que modelo corresponde ni a que serializador van a cumplir ordenes ya que en cada metodo podemos acceder a diferentes modelos

# class CustomController(APIView):
#     #el api view se puede utilizar para trabajar con varios modelos dentro de la misma clase
#     def get(self):
#         pass
#     def post(self):
#         pass

# tambien


@api_view(['GET', 'POST'])
def prueba(request):  # /usuario/id
    print(request.method)
    return Response({
        "message": "Esto es un controlodor de prueba"
    })

# Hacer un controlador para contabilizar la cantidad de perros nacidos en determinado año
# SELECT * FROM t_mascota where macota_fecnac BETWEEN "2018-01-01" and "2018-12-31"

# EN el orm seria => MascotaModel.objects.filter(masccotaFechaNacimiento__range = ("2018-01-01", "2018-12-31"))


class BusquedaController(ListAPIView):
    queryset = MascotaModel.objects.all()
    serializer_class = MascotaSerializar

    def get(self, request):
        print(request.query_params.get('fecha'))
        if request.query_params.get('fecha'):
            anios = request.query_params.get('fecha')
            # mascotas = MascotaModel.objects.filter        (mascotaFechaNacimiento__range = (anios + "-01-01", anios + "-12-31"))
            # Para ver todas las combinaciones posibles entre las columnas y sus opciones => https://docs.djangoproject.com/en/3.1/ref/models/querysets/#gt
            mascotas = MascotaModel.objects.filter(
                mascotaFechaNacimiento__year=anios
            ).all()
            resultado = self.serializer_class(mascotas, many=True)
            return Response({
                "success": True,
                "content": resultado.data,
                "message": None
            })
        else:
            return Response({
                "success": False,
                "content": None,
                "message": None
            })

# controlador para contabilizar cuantas mascotas son machos y cuantos son hembras


@api_view(['GET'])
def contabilizar_sexo(request):

    # Seleccionar que values vamos a utilizar para esta consulta
    # el metodo values sirve para indicar que columnas vamos a utilizar de la tabla
    # Luego el count sirve para hacer clausulas de agrupamiento
    # Order by es una clausula de ordenamiento en el cual su valor por defecto as ASCENDENTE, si queremos ordenar de manera descente simplemente ponemos  un "-" antes de la columna
    resultado = MascotaModel.objects.values('mascotaSexo').annotate(
        Count('mascotaSexo')).order_by('mascotaSexo')
    # Si queremos hacer un ordenamiento usando alguna relacion con una columna de un padre
    pruebas = MascotaModel.objects.order_by('raza_id__razaNombre').all()
    # Busqueda de todas las mascotas ciando su razanombre sea doberman
    pruebas3 = MascotaModel.objects.filter(
        raza__especie__especieNombre="Perro"
    ).all()
    pruebas4 = EspecieModel.objects.filter(especiesRaza__razaId=1).all()

    pruebas5 = EspecieModel.objects.filter(
        especiesRaza__mascotaRaza__mascotaNombre="Flu"
    ).all()
    # print(pruebas)
    # print(pruebas3)
    # print(pruebas4)
    # print(pruebas5)

    # print(pruebas3)
    # print(resultado)
    # hembra = 0
    # macho = 0
    # for i in resultado:
    #     print(i["mascotaSexo"])
    #     if(i["mascotaSexo"] is "H"):
    #         hembra += 1
    #     elif i["mascotaSexo"] is "M":
    #         macho += 1
    # print(hembra)
    # print(macho)
    return Response({
        "success": resultado
    })


class ClienteController(ListCreateAPIView):
    queryset = ClienteModel.objects.all()
    serializer_class = ClienteSerializar

    def post(self, request):
        resultado = RegistroClienteSerializar(data=request.data)
        if resultado.is_valid():
            # Validar si el dni ya esta registrado
            validacion = ClienteModel.objects.filter(clienteDni = resultado.validated_data.get('dni')).first()
            if validacion is None:
                resultado.validated_data
                personaEncontrada = consultarDNI(
                    resultado.validated_data['dni'])
                print(personaEncontrada)
                nuevoCliente = ClienteModel(clienteDni = resultado.validated_data.get('dni'),
                            clienteNombre = personaEncontrada.get('data').get('nombres'),
                            clienteApellido = personaEncontrada.get('data').get('apellido_paterno')+' '+ personaEncontrada.get('data').get('apellido_materno'),
                            clienteEmail = resultado.validated_data.get('email'),
                            clienteFono = resultado.validated_data.get('telefono')
                )
                nuevoCliente.save()
                # resultado.date
                # resultado.save()
                return Response({
                    "success": True,
                    "content": self.serializer_class(nuevoCliente).data,
                    "message": None
                }, status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "content": resultado.errors,
            "message": "Hubo error al guardar el cliente"
        }, status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        resultado = self.serializer_class(self.get_queryset(), many=True)
        return Response({
            "success": True,
            "content": resultado.data,
            "message": None
        })

# Ejercicio 1 ver todas las mascotas de un usuario segun su dni, Pista: usar el related_name ubicado en la fk del usuario de mascota
# Ejercicio bonus luego mostrar la raza de esa mascota

# 127.0.0.1:8000/buscar?dni=77777
from django.shortcuts import get_object_or_404
@api_view(['GET'])
def buscar_mascotas(request):
    # llamarian al serializar
        print(request.query_params.get('dni'))
        dni = request.query_params.get('dni')
        try:
            cliente = get_object_or_404(ClienteModel, pk= dni)
            print(cliente)
            resultado = ClienteMascotaSerializar(instance=cliente)
            return Response({
                "success": True,
                "content": resultado.data,
                "message": "Encontrado" 
            })
        except:
            return Response({
                "success": False
            })
