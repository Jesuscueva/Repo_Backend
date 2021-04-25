# Aca declararemos todas la rutas de la aplicacion

from django.urls import path
from .views import EspeciesController, EspecieController, MascotasController, RazasController, buscar_mascotas, prueba, BusquedaController, contabilizar_sexo, ClienteController

urlpatterns = [
    path('especie', EspeciesController.as_view()),
    path('especie/<int:id>', EspecieController.as_view()),
    path("raza", RazasController.as_view()),
    path("mascota", MascotasController.as_view()),
    path("prueba", prueba),
    path('busquedaFecha', BusquedaController.as_view()),
    path('contabilizarSexo', contabilizar_sexo),
    path('cliente', ClienteController.as_view()),
    path('buscar', buscar_mascotas)
] 