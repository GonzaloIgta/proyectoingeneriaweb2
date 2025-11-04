from django.db import models

class TipoProducto(models.Model):
   
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    def __str__(self):
        return self.nombre

    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    

class Tienda(models.Model):
    def __str__(self):
        return self.nombre

    nombre = models.CharField(max_length=40)
    direccion = models.CharField(max_length=100)
    contacto = models.CharField(max_length=50)
    productos = models.ManyToManyField(Producto)

