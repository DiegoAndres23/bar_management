from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Ventas, Producto, Topping
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.core.serializers import serialize

@csrf_exempt
def registrar_pago(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data["pedidos"])
        for pedido in data["pedidos"]:
            producto_nombre = pedido["producto"]
            cantidad = pedido["quantity"]
            toppings_nombres = pedido["toppings"]

            # Obtener la instancia de Producto
            producto = Producto.objects.get(nombre=producto_nombre)

            # Obtener las instancias de Topping
            toppings = Topping.objects.filter(nombre__in=toppings_nombres)

            # Crear la instancia de Ventas
            pago = Ventas.objects.create(producto=producto, cantidad=cantidad)
            pago.toppings.set(toppings)
            pago.save()
        return JsonResponse({'status': 'success'})
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
        context['productos'] = Producto.objects.all()
        context['productos'] = serialize('json', context['productos'])
        context['toppings'] = Topping.objects.all()
        context['toppings'] = serialize('json', context['toppings'])
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(MesasPage, self).dispatch(request, *args, **kwargs)

