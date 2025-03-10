from django.urls import path
from bar import views
from . import views

urlpatterns = [
    path('', views.MesaListView.as_view(), name='mesa_list'),
    path('registrar_pago/', views.registrar_pago, name='registrar_pago'),
    
]
