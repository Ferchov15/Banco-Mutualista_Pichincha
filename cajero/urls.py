from django.urls import path
from . import views

app_name = 'cajero'

urlpatterns = [
    
    path("", views.login_view, name="login"), 
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/login/index/", views.index, name="index"),
]