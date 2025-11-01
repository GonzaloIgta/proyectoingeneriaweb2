from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_tipoProducto, name='index'),
    path('tipoproducto/<int:tipoproducto_id>/', views.show_tipoProducto, name='detail'),
    path('tipoproducto/<int:tipoproducto_id>/producto', views.index_producto, name='producto'),
    path('producto/<int:producto_id>', views.show_producto, name='producto'),
    path('tienda/<int:tienda_id>', views.show_tienda, name='tienda'),
]