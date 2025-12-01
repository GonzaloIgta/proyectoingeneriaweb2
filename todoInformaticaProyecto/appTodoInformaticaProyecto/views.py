from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from .models import TipoProducto, Producto, Tienda


# Devuelve el listado de tipos de productos
class IndexTipoProductoView(ListView):
    model = TipoProducto
    template_name = 'index_tipoProducto.html'
    context_object_name = 'tipos'
    ordering = ['nombre']

# Devuelve los datos de un tipo de producto
class ShowTipoProductoView(DetailView):
    model = TipoProducto
    template_name = 'show_tipoProducto.html'
    context_object_name = 'tipo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = self.object.producto_set.all()
        return context

# Devuelve los productos de un tipo (lista filtrada)
class IndexProductoView(ListView):
    model = Producto
    template_name = 'show_tipoProducto.html'
    context_object_name = 'productos'

    def get_queryset(self):
        tipoproducto_id = self.kwargs['tipoproducto_id']
        return Producto.objects.filter(tipo_id=tipoproducto_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipoproducto_id = self.kwargs['tipoproducto_id']
        context['tipo'] = TipoProducto.objects.get(pk=tipoproducto_id)
        return context

# Devuelve los detalles de un producto
class ShowProductoView(DetailView):
    model = Producto
    template_name = 'show_producto.html'
    context_object_name = 'producto'

# Devuelve los detalles de una tienda
class ShowTiendaView(DetailView):
    model = Tienda
    template_name = 'show_tienda.html'
    context_object_name = 'tienda'



def get_or_create_cart(request):
    """Obtiene el diccionario del carrito o crea uno vacío"""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']

def actualizar_total_carrito(request):
    cart = request.session.get('cart', {})
    total_cantidad = sum(cart.values()) # Suma las cantidades de todos los productos
    request.session['cart_total_items'] = total_cantidad # Variable especial para el header
    request.session.modified = True
    return total_cantidad



def ver_carrito(request):
    """Renderiza la página del carrito con los productos detallados"""
    cart = request.session.get('cart', {})
    items = []
    total_precio = 0

    for product_id, cantidad in cart.items():
        try:
            producto = Producto.objects.get(pk=product_id)
            subtotal = float(producto.precio_base) * cantidad
            total_precio += subtotal
            
            items.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        except Producto.DoesNotExist:
            continue

    # Actualizamos el total al entrar aquí por si acaso
    actualizar_total_carrito(request)

    context = {
        'items': items,
        'total_precio': total_precio
    }
    return render(request, 'carrito.html', context)


# ajax
@require_POST
def add_to_cart_ajax(request):
    product_id = request.POST.get('product_id')
    if not product_id:
        return JsonResponse({'status': 'error', 'message': 'ID faltante'}, status=400)

    cart = get_or_create_cart(request)
    cart_key = str(product_id)
    cart[cart_key] = cart.get(cart_key, 0) + 1
    
    request.session.modified = True
    
    # Calculamos el nuevo total real
    new_total = actualizar_total_carrito(request)

    return JsonResponse({
        'status': 'success', 
        'message': 'Producto añadido',
        'cart_count': new_total # Enviamos la suma total
    })


# ajax, actualizar cantidad
@require_POST
def update_cart_item_ajax(request):
    product_id = request.POST.get('product_id')
    action = request.POST.get('action')
    
    cart = get_or_create_cart(request)
    key = str(product_id)
    
    if key in cart:
        if action == 'increase':
            cart[key] += 1
        elif action == 'decrease':
            cart[key] = max(1, cart[key] - 1)
            
        request.session.modified = True
        
        # Recalculamos el total global
        new_total = actualizar_total_carrito(request)

        return JsonResponse({
            'status': 'success',
            'cantidad': cart[key],
            'cart_total_items': new_total
        })
    
    return JsonResponse({'status': 'error', 'message': 'Producto no encontrado'})


# ajax, eliminar producto
@require_POST
def remove_from_cart_ajax(request):
    product_id = request.POST.get('product_id')
    cart = get_or_create_cart(request)
    key = str(product_id)
    
    if key in cart:
        del cart[key]
        request.session.modified = True
        
        # Recalculamos el total global tras borrar
        new_total = actualizar_total_carrito(request)
        
        return JsonResponse({
            'status': 'success', 
            'cart_total_items': new_total
        })
        
    return JsonResponse({'status': 'error', 'message': 'No se pudo eliminar'})