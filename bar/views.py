from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pedido, Producto
from .forms import PedidoForm
from django.views.decorators.csrf import csrf_exempt
from .models import Pago
import json
from django.http import JsonResponse

@csrf_exempt
def registrar_pago(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mesa_id = data.get('mesa_id')
        total = data.get('total')
        pago = Pago.objects.create(mesa_id=mesa_id, total=total)
        return JsonResponse({'status': 'success', 'pago_id': pago.id})
    return JsonResponse({'status': 'error'}, status=400)


class HomePage(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(HomePage, self).dispatch(request, *args, **kwargs)

class MesasPage(TemplateView):
    template_name = 'mesas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(MesasPage, self).dispatch(request, *args, **kwargs)

