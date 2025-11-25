import os
from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.files import File
from django.conf import settings
from appTodoInformaticaProyecto.models import TipoProducto, Producto, Tienda 

class Command(BaseCommand):
    help = 'Carga masiva automática basada en nombres de archivo'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # 1. DEFINIR RUTA DE ORIGEN
        # Django buscará las fotos en: tu_proyecto/imagenes_origen/
        CARPETA_ORIGEN = os.path.join(settings.BASE_DIR, 'imagenes_origen')

        self.stdout.write(self.style.WARNING(f'Buscando imágenes en: {CARPETA_ORIGEN}'))
        
        # Limpieza inicial
        self.stdout.write(self.style.WARNING('--- BORRANDO BASE DE DATOS ANTIGUA ---'))
        Tienda.objects.all().delete()
        Producto.objects.all().delete()
        TipoProducto.objects.all().delete()

        # 2. CREAR CATEGORÍAS
        cat_laptops = TipoProducto.objects.create(nombre="Portátiles")
        cat_componentes = TipoProducto.objects.create(nombre="Componentes")
        cat_perifericos = TipoProducto.objects.create(nombre="Periféricos")
        cat_almacenamiento = TipoProducto.objects.create(nombre="Almacenamiento")

        # 3. LISTA DE PRODUCTOS 
        # Ya no ponemos el campo 'img'. El script lo adivinará por el 'nombre'.
        productos_data = [
            # Portátiles
            {"nombre": "MacBook Air M2", "precio": 1199.00, "tipo": cat_laptops, "desc": "Ligero y potente."},
            {"nombre": "ASUS ROG Strix", "precio": 1450.50, "tipo": cat_laptops, "desc": "Gaming puro."},
            
            # Componentes
            {"nombre": "NVIDIA RTX 4090", "precio": 1899.99, "tipo": cat_componentes, "desc": "La gráfica más potente."},
            {"nombre": "Intel Core i9", "precio": 580.00, "tipo": cat_componentes, "desc": "Procesador extremo."},
            {"nombre": "RAM Corsair 32GB", "precio": 125.00, "tipo": cat_componentes, "desc": "DDR5 RGB."},

            # Periféricos
            {"nombre": "Teclado Mecánico", "precio": 95.00, "tipo": cat_perifericos, "desc": "Switches azules."},
            {"nombre": "Raton Logitech", "precio": 50.00, "tipo": cat_perifericos, "desc": "Alta precisión."},
            {"nombre": "Monitor 4K Dell", "precio": 400.00, "tipo": cat_perifericos, "desc": "Para diseño gráfico."},

            # Almacenamiento
            {"nombre": "SSD Samsung 1TB", "precio": 110.00, "tipo": cat_almacenamiento, "desc": "Alta velocidad NVMe."},
        ]

        self.stdout.write(self.style.SUCCESS('--- CARGANDO PRODUCTOS ---'))

        for p in productos_data:
            # Creamos el producto en la BD
            producto_obj = Producto.objects.create(
                nombre=p["nombre"],
                descripcion=p["desc"],
                precio_base=p["precio"],
                tipo=p["tipo"]
            )

            # --- LÓGICA AUTOMÁTICA DE IMAGEN ---
            # Construimos el nombre del archivo: "Nombre Producto.jpg"
            nombre_foto = f"{p['nombre']}.jpg"
            ruta_completa = os.path.join(CARPETA_ORIGEN, nombre_foto)

            if os.path.exists(ruta_completa):
                with open(ruta_completa, 'rb') as f:
                    # Guardamos la imagen. 
                    # El primer argumento es el nombre con el que se guardará en Django
                    producto_obj.imagen.save(nombre_foto, File(f), save=True)
                self.stdout.write(f" [OK] Foto cargada para: {p['nombre']}")
            else:
                self.stdout.write(self.style.ERROR(f" [X] NO SE ENCONTRÓ ARCHIVO: {nombre_foto} (Se creó el producto sin foto)"))

        
        # 4. CREAR TIENDAS Y STOCK
        self.stdout.write(self.style.SUCCESS('--- ASIGNANDO STOCK A TIENDAS ---'))
        
        central = Tienda.objects.create(nombre="MegaTech Central", direccion="Centro", contacto="admin@megatech.com")
        central.productos.set(Producto.objects.all())

        gamer = Tienda.objects.create(nombre="Zona Gamer", direccion="Norte", contacto="gamer@megatech.com")
        # Filtro: Solo productos caros o de categorías específicas
        gamer.productos.set(Producto.objects.filter(precio_base__gte=100))

        self.stdout.write(self.style.SUCCESS('¡PROCESO TERMINADO!'))