from django.urls import path
from . import views

app_name = 'cajero'

urlpatterns = [
    
    path("", views.login_view, name="login"), 
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/login/index/", views.index, name="index"),
    path('consultar_saldo/', views.consultar_saldo, name='consultar_saldo'),
    path('realizar_retiro/', views.realizar_retiro, name='realizar_retiro'),
]