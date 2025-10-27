from django.db import models

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=50)

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)

class Tienda(models.Model):
    nombre = models.CharField(max_length=40)
    direccion = models.CharField(max_length=100)
    contacto = models.CharField(max_length=50)
