from django.shortcuts import render  # 'render' ya estaba importado, ¡perfecto!
from django.http import HttpResponse
from .models import TipoProducto, Producto, Tienda

# devuelve el listado de tipos de productos
def index_tipoProducto(request):
	tipos = TipoProducto.objects.order_by('nombre')
	context = {'tipos': tipos}
	return render(request, 'index_tipoProducto.html', context)

# devuelve los datos de un tipo de producto
def show_tipoProducto(request, tipoproducto_id):
	tipo = TipoProducto.objects.get(pk=tipoproducto_id)
	productos = tipo.producto_set.all()
	context = {
		'tipo': tipo,
		'productos': productos
	}
	return render(request, 'show_tipoProducto.html', context)

# devuelve los productos de un tipo de producto
def index_producto(request, tipoproducto_id):
	tipo = TipoProducto.objects.get(pk=tipoproducto_id)
	productos = tipo.producto_set.all()
	context = {
		'tipo': tipo,
		'productos': productos
	}
	return render(request, 'show_tipoProducto.html', context) 


# devuelve los detalles de un empleado
def show_producto(request, producto_id):
	producto = Producto.objects.get(pk=producto_id)
	context = {'producto': producto}
	return render(request, 'show_producto.html', context) 

# devuelve los detalles de una tienda
def show_tienda(request, tienda_id): 
    tienda = Tienda.objects.get(pk=tienda_id)
    context = {'tienda': tienda}
    return render(request, 'show_tienda.html', context)