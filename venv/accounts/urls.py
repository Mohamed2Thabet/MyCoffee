from django.urls import path
from . import views

urlpatterns = [
    path('signin',views.singnin,name="signin"),
    path('logout',views.logout,name="logout"),
    path('signup',views.signup,name="signup"),
    path('profile',views.profile,name="profile"),
    path('product_favorites/<int:pro_id>',views.product_favorites,name="product_favorites"),
    path('show_product_favorites',views.show_product_favorites,name="show_product_favorites"),
]
