from django.contrib import admin
from .models import Producto, Topping, Pedido, Pago

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_formateado')
    search_fields = ('nombre',)

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_formateado')
    search_fields = ('nombre',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'fecha', 'total_formateado')
    list_filter = ('fecha',)
    search_fields = ('producto__nombre', 'fecha',)

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'total_formateado', 'fecha')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'total', 'fecha')
    list_filter = ('fecha',)
    search_fields = ('pedido__producto__nombre',)