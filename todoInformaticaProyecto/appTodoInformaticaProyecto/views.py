from django.views.generic import ListView, DetailView
from .models import TipoProducto, Producto, Tienda
from django.views.decorators.http import require_POST
from django.http import JsonResponse


# Devuelve el listado de tipos de productos (usando ListView)
class IndexTipoProductoView(ListView):
    model = TipoProducto
    template_name = 'index_tipoProducto.html'
    context_object_name = 'tipos'
    ordering = ['nombre']  # Ordena por nombre

# Devuelve los datos de un tipo de producto (usando DetailView, incluyendo productos en contexto)
class ShowTipoProductoView(DetailView):
    model = TipoProducto
    template_name = 'show_tipoProducto.html'
    context_object_name = 'tipo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = self.object.producto_set.all()
        return context

# Devuelve los productos de un tipo de producto (similar a ShowTipoProductoView, pero si es solo lista de productos, usa ListView)
# Nota: Esta vista parece redundante con show_tipoProducto, ya que usa la misma plantilla y contexto.
# Si es intencionalmente una lista de productos, la implementamos como ListView filtrada por tipo.
class IndexProductoView(ListView):
    model = Producto
    template_name = 'show_tipoProducto.html'
    context_object_name = 'productos'

    def get_queryset(self):
        tipoproducto_id = self.kwargs['tipoproducto_id']
        return Producto.objects.filter(tipo_id=tipoproducto_id)  # Asumiendo que el campo FK en Producto es 'tipo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipoproducto_id = self.kwargs['tipoproducto_id']
        context['tipo'] = TipoProducto.objects.get(pk=tipoproducto_id)
        return context

# Devuelve los detalles de un producto (usando DetailView)
class ShowProductoView(DetailView):
    model = Producto
    template_name = 'show_producto.html'
    context_object_name = 'producto'

# Devuelve los detalles de una tienda (usando DetailView)
class ShowTiendaView(DetailView):
    model = Tienda
    template_name = 'show_tienda.html'
    context_object_name = 'tienda'


    
# funcion auxiliar para la sesion del carrito
def get_or_create_cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']

# ajax, vista que maneja la peticion POST)
@require_POST  
def add_to_cart_ajax(request):
    product_id = request.POST.get('product_id')
    
    if not product_id:
        return JsonResponse({'status': 'error', 'message': 'ID de producto no proporcionado'}, status=400)

    try:
        cart = get_or_create_cart(request)
        
        # añadir producto carrito
        cart_key = str(product_id)
        cart[cart_key] = cart.get(cart_key, 0) + 1
            
        request.session.modified = True
        
        # calcular total
        new_cart_count = sum(cart.values())

        # Respuesta JSON para cliente
        return JsonResponse({
            'status': 'success', 
            'message': 'Producto añadido al carrito.',
            'cart_count': new_cart_count
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)