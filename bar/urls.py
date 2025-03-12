from django.urls import path
from bar import views
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('registrar_pago/', views.registrar_pago, name='registrar_pago'),
    path('mesas/', views.MesasPage.as_view(), name='mesas'),
    path('ventas/', views.VentasPage.as_view(), name='ventas'),
    
]
