from django.urls import path
from apps.contacts import views

urlpatterns = (
    path('list/', views.contacts_list_view, name='contacts_list'),
)
