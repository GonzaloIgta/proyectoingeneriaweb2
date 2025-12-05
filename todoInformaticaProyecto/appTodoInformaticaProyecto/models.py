from django.db import models

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

   # En models.py, dentro de la clase TipoProducto:

    def get_icon(self):
        """Devuelve el nombre del icono de Bootstrap según el nombre de la categoría"""
        n = self.nombre.lower() # Convertimos a minúsculas para comparar fácil

        # 1. Equipos principales
        if 'portátil' in n or 'laptop' in n: return 'bi-laptop'
        if 'sobremesa' in n or 'pc' in n or 'ordenador' in n: return 'bi-pc-display'
        
        # 2. Componentes Internos
        if 'gráfica' in n or 'video' in n or 'gpu' in n: return 'bi-gpu-card'
        if 'procesador' in n or 'cpu' in n: return 'bi-cpu'
        if 'placa' in n or 'motherboard' in n: return 'bi-motherboard'
        if 'ram' in n or 'memoria' in n: return 'bi-memory'
        if 'disco' in n or 'ssd' in n or 'hdd' in n or 'almacenamiento' in n: return 'bi-device-hdd'
        if 'refrigeración' in n or 'ventilador' in n: return 'bi-fan'
        if 'fuente' in n or 'alimentación' in n: return 'bi-plug'
        
        if 'componentes' in n: return 'bi-motherboard' 

        if 'monitor' in n or 'pantalla' in n: return 'bi-display'
        if 'ratón' in n or 'mouse' in n: return 'bi-mouse3'
        if 'teclado' in n or 'keyboard' in n: return 'bi-keyboard'
        if 'audio' in n or 'auricular' in n or 'sonido' in n or 'altavoz' in n: return 'bi-headphones'
        if 'impresora' in n or 'escáner' in n: return 'bi-printer'
        if 'red' in n or 'wifi' in n or 'router' in n: return 'bi-router'
        if 'cable' in n or 'adaptador' in n or 'usb' in n: return 'bi-usb-plug'
        
        # Si la categoría se llama genéricamente "Periféricos"
        if 'periféricos' in n or 'accesorio' in n: return 'bi-keyboard' 
        
        # Icono por defecto si no encuentra coincidencia
        return 'bi-box-seam-fill'

# ... (El resto de tus modelos Producto y Tienda siguen igual) ...
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