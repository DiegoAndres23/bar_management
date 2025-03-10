from django.urls import path
from .views import MesaListView, MesaDetailView, MesaCreateView, MesaUpdateView, MesaDeleteView

urlpatterns = [
    path('', MesaListView.as_view(), name='mesa_list'),
    path('<int:pk>/', MesaDetailView.as_view(), name='mesa_detail'),
    path('crear/', MesaCreateView.as_view(), name='mesa_create'),
    path('<int:pk>/editar/', MesaUpdateView.as_view(), name='mesa_update'),
    path('<int:pk>/eliminar/', MesaDeleteView.as_view(), name='mesa_delete'),
]
