from django.urls import path
from apps.common import views

urlpatterns = (
    path('', views.index_view, name='index'),
    path('subscribe-newsletter/', views.subscribe_newsletter_view, name='subscribe_newsletter'),
)
