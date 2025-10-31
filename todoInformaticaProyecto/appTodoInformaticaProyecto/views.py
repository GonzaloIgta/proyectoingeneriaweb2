from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse
from .models import TipoProducto, Producto, Tienda

#devuelve el listado de tipos de productos
def index_tipoProducto(request):
	tipos = TipoProducto.objects.order_by('nombre')
	output = ', '.join([t.nombre for t in tipos])
	return HttpResponse(output)

#devuelve los datos de un tipo de producto
def show_tipoProducto(request, nombre):
	tipo = TipoProducto.objects.get(pk=nombre)
	output = f'Detalles del tipo de producto: {nombre}'
	return HttpResponse(output)

#devuelve los productos de un tipo de producto
def index_producto(request, nombre):
	tipo = TipoProducto.objects.get(pk=nombre)
	output = ', '.join([e.nombre for e in tipo.producto_set.all()])
	return HttpResponse(output)

#devuelve los detalles de un empleado
def show_producto(request, nombre):
	producto = Producto.objects.get(pk=nombre)
	output = f'Detalles del producto: {producto.nombre}, {producto.descripcion}, {str(producto.tipo)}, , {producto.precio_base} € tiendas: {[t.nombre for t in producto.tienda_set.all()]}'
	return HttpResponse(output)

#devuelve los detalles de una habilidad
def show_tienda(request, nombre):
	tienda = Tienda.objects.get(pk=nombre)
	output = f'Detalles de la tienda: {tienda.id}, {tienda.nombre}. producto: {[p.nombre for p in tienda.productos_set.all()]}'
	return HttpResponse(output)