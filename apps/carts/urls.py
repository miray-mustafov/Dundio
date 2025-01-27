from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail_view, name='cart_details'),
    path('add/<int:product_id>/', views.cart_add_view, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove_view, name='cart_remove'),
]
