import re
from rest_framework.permissions import BasePermission, SAFE_METHODS

class soloAdministrador(BasePermission):
    def has_permission(self, request, view):
        # el request nos dara los mismos atributos que nos da el request de las vistas genericas
        print(SAFE_METHODS)
        print(view)
        print(request.user.personalTipo)

        if request.user.personalTipo == 1:
            return True
        else:
            return False
        # if request.method in SAFE_METHODS:
        #     return True
        # else:
        #     return False

        # en los customs permissions tenemos que retornar siempre un booleano (true o false) porque si es verdadero procedera con el siguiente permiso o con el controlador final

class administradorPost(BasePermission):
    def has_permission(self, request, view):
        print(request.method)
        if request.method == "POST":
            if request.user.personalTipo == 1:
                return True
            else:
                return False
        else:
            return True

class soloMozos(BasePermission):
    def has_permission(self, request, view):
        # Solamente pueden ser mozos
        if request.user.personalTipo == 3:
            return True 
        return False