from django.contrib import admin
from .models import Producto, Topping, Ventas

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_formateado')
    search_fields = ('nombre',)

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_formateado')
    search_fields = ('nombre',)

@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'fecha', 'total_formateado')
    list_filter = ('fecha',)
    search_fields = ('producto__nombre', 'fecha',)
