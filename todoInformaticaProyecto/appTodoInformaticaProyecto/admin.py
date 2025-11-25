# appTodoInformaticaProyecto/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import TipoProducto, Producto, Tienda

admin.site.site_header = "🖥️ Todo Informática - Panel de Administración"
admin.site.site_title = "Todo Informática Admin"
admin.site.index_title = "Bienvenido al panel de gestión"

@admin.register(TipoProducto)
class TipoProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'num_productos'] 
    list_filter = ['nombre']  
    search_fields = ['nombre']  
    readonly_fields = ['num_productos']  

    def num_productos(self, obj):
        return obj.producto_set.count()  # Cuenta productos relacionados
    num_productos.short_description = 'Número de Productos'

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'precio_base', 'imagen']  # Incluye preview de imagen
    list_filter = ['tipo', 'precio_base']  # Filtros
    search_fields = ['nombre', 'descripcion']  

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" />', obj.imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = 'Preview'

@admin.register(Tienda)
class TiendaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'direccion', 'contacto']
    search_fields = ['nombre', 'direccion']
    list_filter = ['nombre'] #