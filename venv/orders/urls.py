from django.urls import path
from . import views
urlpatterns = [
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart,name='cart'),
    path('remove_from_cart<int:orderdetail_id>',views.remove_from_cart,name='remove_from_cart'),
    path('add_qty/<int:orderdetail_id>',views.add_qty,name='add_qty'),
    path('sub_qty/<int:orderdetail_id>',views.sub_qty,name='sub_qty'),
    path('payment',views.payment,name='payment'),
    path('show_orders',views.show_orders,name='show_orders'),
]
