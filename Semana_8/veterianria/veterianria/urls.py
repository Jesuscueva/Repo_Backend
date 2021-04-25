"""veterianria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
schema_view = get_schema_view(
    openapi.Info(
        title= "API de Gestion de Veterinaria",
        default_version= "1.0",
        description= "API usando DRF para el manejo de las mascotas de una veterianria",
        terms_of_service= "http://www.google.com",
        contact= openapi.Contact(name= "Jesus Cueva", email="jcueva12380@gmail.com"),
        license= openapi.License(
            name="MIT", url="http://es.wikipedia.org/wiki/Licencia_MIT"
        )
    ),
    public=True,
    permission_classes = [permissions.AllowAny]
)
# from django.urls.conf import include

urlpatterns = [
    path('', schema_view.with_ui('swagger')),
    path('redoc', schema_view.with_ui('redoc')),
    path('admin/', admin.site.urls),
    path('' , include('administracion.urls'))
]
