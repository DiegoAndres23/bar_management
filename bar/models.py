from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField()
    estado = models.CharField(max_length=20, choices=[('disponible', 'Disponible'), ('ocupada', 'Ocupada')])

    def __str__(self):
        return f"Mesa {self.numero} - {self.estado}"

class Pedido(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name='pedidos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"Pedido de {self.cantidad} {self.producto.nombre} en {self.mesa}"

class Pago(models.Model):
    mesa_id = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mesa {self.mesa_id} - Total: {self.total}'