from django.shortcuts import render
from rest_framework import permissions
from .models import PlatoModel
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import *
from uuid import uuid4
# Create your views here.
from .permissions import administradorPost, soloAdministrador, soloMozos
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
#Libreria que me permite eliminar 
import os 
# nos trae todas la variables que estamos usando en el settings
from django.conf import settings

from datetime import datetime, date

from .combrobantes import emitirComprobante

class PlatosController(generics.ListCreateAPIView):
    queryset = PlatoModel.objects.all()
    serializer_class = PlatoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,administradorPost]    
    def get(self, request):
        respuesta = self.serializer_class(instance=self.get_queryset() , many=True)
        return Response({
            "success": True,
            "content": respuesta.data,
            "message": None
        })

    def post(self, request):
        archivo = request.FILES['platoFoto']
        print(archivo.name)
        # separador = "."
        # imagen_separada = archivo.name.split(separador)
        # imagen_separada.pop(0)
        # print(imagen_separada[0])

        request.FILES['platoFoto'].name =str( uuid4())+request.FILES['platoFoto'].name
        respuesta = self.serializer_class(data=request.data)
        if respuesta.is_valid():
            respuesta.save()
            print(respuesta.data)
            return Response({
                "success": True,
                "message": "Se registro el plato exitosamente",
                "content": respuesta.data
            })
        else:
            return Response({
                "success": False,
                "message": "Error al registrar el plato",
                "content": respuesta.errors
            }, status.HTTP_400_BAD_REQUEST)

class PlatoController(generics.RetrieveDestroyAPIView): 
    queryset = PlatoModel.objects.all()
    serializer_class = PlatoSerializer
    def get_queryset(self, id):
        return PlatoModel.objects.get(platoId = id)
    
    def get(self, request, id):
        resultado = self.serializer_class(instance=self.get_queryset(id))
        return Response({
            "success": True,
            "content": resultado.data,
            "message": None
        })
    def put(self, request, id):
        pass

    def delete(self, request, id):
        plato = self.get_queryset(id)
        foto = str(plato.platoFoto)
        try: 
            ruta_img = settings.MEDIA_ROOT /  foto
            os.remove(ruta_img)
        except:
            print('Fotografia del plato no existe')
        plato.delete()
        return Response({
            "success": True,
            "content": None,
            "message": "Eliminado exitosamente"
        })
        

class RegistroPersonalController(generics.CreateAPIView):
    serializer_class = RegistroSerializer

    def post(self, request):
        nuevoPersonal = self.serializer_class(data = request.data)
        if nuevoPersonal.is_valid():
            nuevoPersonal.save()
            return Response({
                "success": True,
                "content": nuevoPersonal.data,
                "message": "Personal creado exitosamente"
            })
        else:
            return Response({
                "success": False,
                "content": nuevoPersonal.erros,
                "message": "Error al crear el nuevo Personal"
            })

from rest_framework_simplejwt.views import TokenObtainPairView


class CustomPayloadController(TokenObtainPairView):
    """Sirve para modificar el claim de nuestra token de acceso"""
    # los permissions_classes sirve para indicar que tipo de usuario puede acceder a este controller
    permission_classes = [AllowAny]
    serializer_class = CustomPayloadSerializer

# IsAuthenticatedOrReadOnly = Solamente pedira la token en el caso que no sea un metodo de lectura(get)
# IsAdminUser = valida que el usuario que esta tratando de acceder a cualquiera de los metodos sea is_staff
# IsAuthenticated = valida que la consulta sea dada por una token valida y correcto


class MesaController(generics.ListCreateAPIView):
    queryset = MesaModel.objects.all()
    serializer_class = MesaSerializer
    permission_classes = [soloAdministrador]

    def get(self, request):
        print(request.user)
        print(request.auth)
        resultado = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response( {
            "success": True,
            "content": resultado.data,
            "message": None
        })

    def post(self, request):
        resultado = self.serializer_class(data=request.data)
        if resultado.is_valid():
            resultado.save()
            return Response({
                "success": True,
                "content": resultado.data,
                "message": "Mesa creada exitosamente" 
            }, status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "content": resultado.errors,
                "message": "Hubo un error al crear la mesa"
            }, status.HTTP_400_BAD_REQUEST)

class VentasController(generics.ListCreateAPIView):
    def get(self, request):
        pass

class NotaPedidoController(generics.CreateAPIView):
    serializer_class = NotaPedidoCreacionSerializer
    permission_classes = [IsAuthenticated, soloMozos]
    def post(self, request):
        #  crear la cabecera
        data = self.serializer_class(data = request.data)
        data.is_valid(raise_exception=True)
        print(request.user)
        numeroMesa = data.validated_data['mesa']
        objMesa = MesaModel.objects.filter(mesaId =  numeroMesa).first()
        print(objMesa)
        print(request.auth)
        nuevaCabecera = CabeceraComandaModel(
            # si en la columna de la bd es tipo date, al momento de guardar datos con hh:mm y si usamos ese registr recien creado nos dara error ya que indicara que no puede mostrar la hh:mm  entonces debemos guardar solamente la fecha (YYYY-MM-DD) sin horas con date.today()
            cabeceraFecha = date.today(), 
            cabeceraTotal = 0, 
            cabeceraCliente = data.validated_data['cliente'],
            mozo= request.user,
            mesa= objMesa)
        # crear el detalle de la nota
        detalle = data.validated_data['detalle']
        nuevaCabecera.save()
        print(detalle)
        for detallecomanda in detalle:
            objPlato = PlatoModel.objects.filter(platoId= detallecomanda['plato']).first()
            DetalleComandaModel(
                detalleCantidad = detallecomanda['cantidad'],
                detalleSubtotal = detallecomanda['subtotal'],
                # instancia del modelo plato
                plato = objPlato , 
                cabecera = nuevaCabecera,
            ).save()
            # restar la cantidad vendida de los platos  
            objPlato.platoCantidad = objPlato.platoCantidad -  detallecomanda['cantidad']
            # guardamos ese plato con su antidad modificada en la bd
            objPlato.save()
            print(objPlato)
            nuevaCabecera.cabeceraTotal = nuevaCabecera.cabeceraTotal + (detallecomanda['cantidad'] * detallecomanda['subtotal'])
            nuevaCabecera.save()
            
        # al momento de crear el detalle validar si existe el plato
        resultado = MostrarPedidoSerializer(instance=nuevaCabecera)
        return Response({
            "success": True,
            "content": resultado.data,
            "message": "Venta Creada"
        })

# modificar una nota de pedido para agregar mas productos


class MostrarMesasMozosController(generics.ListAPIView):
    queryset = PersonalModel.objects.all()
    serializer_class = MostrarMesasMozoSerializer
    permission_classes = [IsAuthenticated, soloMozos]

    def get(self, request):
        # print(request)
        respuesta = self.serializer_class(instance= request.user)
        # print(respuesta)
        return Response({
            "success": True,
            "content": respuesta.data
        })

class GenerarComprobantePago(generics.CreateAPIView):
    serializer_class = GenerarComprobanteSerializer
    queryset = CabeceraComandaModel.objects.all()

    def get_queryset(self, id):
        return self.queryset.filter(cabeceraId=id).first()

    def post(self, request, id_comanda):
        respuesta = self.serializer_class(data= request.data)
        if respuesta.is_valid():
            pedido = self.get_queryset(id_comanda)
            if pedido.comprobante:
                return Response({
                "success": True,
                "content": ComprobanteSerializer(instance=pedido.comprobante).data,
                "message": "Ya existe un comprobante relacionado con esa comanda"
            })

            resultadoComprobante = emitirComprobante(respuesta.validated_data, id_comanda)
            return Response({
                "success": True,
                "content": resultadoComprobante
            })
        else:
            return Response({
                "success": False,
                "content": respuesta.errors
            })
