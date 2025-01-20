from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect,render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from .models import Catalogo,Usuario, Tarjeta, CuentaBancaria, Transacciones
from cajero.forms import UsuarioForm

# Create your views here.

def index(request):
    usuarios = Usuario.objects.all()
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'usuarios': usuarios}, request))