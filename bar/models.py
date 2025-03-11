from django.db import models
from babel.numbers import format_currency

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

    def precio_formateado(self):
        return format_currency(self.precio_base, 'COP', locale='es_CO')

class Topping(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

    def precio_formateado(self):
        return format_currency(self.precio, 'COP', locale='es_CO')

class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='pedidos')
    cantidad = models.IntegerField()
    toppings = models.ManyToManyField(Topping, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido de {self.cantidad} {self.producto.nombre}"

    def calcular_total(self):
        total = self.producto.precio_base * self.cantidad
        for topping in self.toppings.all():
            total += topping.precio * self.cantidad
        return total

    def total_formateado(self):
        return format_currency(self.calcular_total(), 'COP', locale='es_CO')

class Pago(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='pagos')
    total = models.DecimalField(max_digits=10, decimal_places=2)