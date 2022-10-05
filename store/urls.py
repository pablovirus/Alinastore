"""Store app URL configuration"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('productos/', views.productos, name='productos'),
    path('detalle/<slug>', views.detalle, name='detalle'),
    path('productos/<slug>', views.categoria, name='categoria'),
    path('about/', views.about, name='about'),
    path('contacto/', views.contacto, name='contacto'),
    path('consultaok', views.consultaok, name='consulta'),
    path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', views.remove_from_cart, name='remove-from-cart'),
    path('add_to_cart_from_product_list/<slug>', views.add_to_cart_from_product_list,
        name='add_to_cart_from_product_list'),
    path('carrito/', views.carrito, name='carrito'),
    path('decrease/<slug>', views.decrease_quantity, name='decrease'),
    path('increase/<slug>', views.increase_quantity, name='increase'),
    path('pedidook/', views.pedido_ok, name='pedidook'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos/<int:pk>', views.pedido_detalle, name='pedido-detalle'),
    # path('search/') #TODO
]
