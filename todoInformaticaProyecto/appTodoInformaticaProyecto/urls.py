from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_tipoProducto, name='index'),
    path('tipoproducto/<str:nombre>/', views.show_tipoProducto, name='detail'),
    path('tipoproducto/<str:tipoproducto>/producto', views.index_producto, name='producto'),
    path('producto/<str:nombre>', views.show_producto, name='producto'),
    path('tienda/<str:nombre>', views.show_tienda, name='tienda'),
]