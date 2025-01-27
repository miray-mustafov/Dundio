from django.urls import path
from apps.products import views

urlpatterns = (
    path('search/', views.products_search_view, name='products_search'),
    path('category/<slug:slug>/', views.products_view, name='products_list'),
    path('details/<slug:slug>/', views.product_details_view, name='product_details'),
)
