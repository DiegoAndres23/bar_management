from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Ventas, Producto, Topping
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.core.serializers import serialize
import pandas as pd
import plotly.express as px
import openpyxl

@csrf_exempt
def registrar_pago(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for pedido in data["pedidos"]:
            producto_nombre = pedido["producto"]
            cantidad = pedido["quantity"]
            toppings_nombres = pedido["toppings"]
            producto = Producto.objects.get(nombre=producto_nombre)
            toppings = Topping.objects.filter(nombre__in=toppings_nombres)
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

class VentasPage(ListView):
    template_name = 'ventas.html'  

    def get_queryset(self):
        return Ventas.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ventas = self.get_queryset()

        # Serializar los datos de ventas a JSON
        ventas_json = serialize('json', ventas)

        # Convertir los datos de ventas a un DataFrame de pandas
        data = {
            'Producto': [venta.producto.nombre for venta in ventas],
            'Cantidad': [venta.cantidad for venta in ventas],
            'Total': [venta.calcular_total() for venta in ventas],
            'Fecha': [venta.fecha.replace(tzinfo=None) for venta in ventas],  # Eliminar la información de zona horaria
        }
        df = pd.DataFrame(data)
        print(df)
        # Agrupar los datos por Producto y sumar las cantidades y totales
        df_grouped = df.groupby('Producto').agg({'Cantidad': 'sum', 'Total': 'sum'}).reset_index()

        # Crear un gráfico de barras con Plotly
        fig = px.bar(df_grouped, x='Producto', y='Total', title='Ventas por Producto')

        # Convertir el gráfico a JSON
        graph_json = fig.to_json()

        context['ventas'] = ventas_json
        context['graph_json'] = graph_json
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(VentasPage, self).dispatch(request, *args, **kwargs)