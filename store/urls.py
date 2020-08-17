from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="home"),
    path('checkout/', views.checkout, name="checkout"),
    path('cart/', views.cart, name="cart")
]