from django.urls import path
from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('plato', PlatosController.as_view()),
    path('plato/<int:id>', PlatoController.as_view()),
    path('registro', RegistroPersonalController.as_view()),
    path('login', TokenObtainPairView.as_view() ),
    path('refresh_token', TokenRefreshView.as_view()),
    path('login_custom', CustomPayloadController.as_view()),
    path('mesa', MesaController.as_view()),
    path('notapedido', NotaPedidoController.as_view()),
    path('mozos/mesas', MostrarMesasMozosController.as_view()),
    path('comprobante/<int:id_comanda>', GenerarComprobantePago.as_view())
]