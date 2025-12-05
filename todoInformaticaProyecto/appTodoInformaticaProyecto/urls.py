from django.urls import path
from .views import (
    IndexTipoProductoView, 
    ShowTipoProductoView, 
    IndexProductoView, 
    ShowProductoView, 
    ShowTiendaView,
    ShowCarritoView,
    add_to_cart_ajax,
    update_cart_item_ajax, 
    remove_from_cart_ajax,
    AllProductsView,
    IndexTiendaView,
    SearchView
)

urlpatterns = [
    path('', IndexTipoProductoView.as_view(), name='index'),
    path('tipos/', IndexTipoProductoView.as_view(), name='index_tipoProducto'),
    path('tipos/<int:pk>/', ShowTipoProductoView.as_view(), name='detail'),  
    path('tipos/<int:tipoproducto_id>/productos/', IndexProductoView.as_view(), name='index_producto'),
    path('productos/<int:pk>/', ShowProductoView.as_view(), name='producto'),  
    path('tiendas/<int:pk>/', ShowTiendaView.as_view(), name='tienda'),
    path('productos/', AllProductsView.as_view(), name='all_products'), # Para el boton "Productos"
    path('tiendas/', IndexTiendaView.as_view(), name='index_tiendas'), # Para el boton "Tiendas"
    path('buscar/', SearchView.as_view(), name='search'),              # Para el boton "Buscar"
    path('api/add-to-cart/', add_to_cart_ajax, name='add_to_cart_ajax'),
    path('carrito/', ShowCarritoView.as_view(), name='carrito'),
    path("api/update-cart-item/", update_cart_item_ajax, name="update_cart_item_ajax"),
    path("api/remove-from-cart/", remove_from_cart_ajax, name="remove_from_cart_ajax"),
]