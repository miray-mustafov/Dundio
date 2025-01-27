from django.urls import path
from apps.users import views

urlpatterns = (
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    path('confirm/', views.check_token_match_view, name='confirm_registration'),
    path('forgotten-pass/', views.forgotten_password_view, name='forgotten_pass'),
    path('reset-pass/', views.reset_pass_view, name='reset_pass'),

    path('my-profile/', views.my_profile_view, name='my-profile'),
    path('logout/', views.logout_view, name='logout'),
)
