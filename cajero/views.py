from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect,render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Catalogo,Usuario, Tarjeta, CuentaBancaria, Transacciones
from cajero.forms import UsuarioForm

# Create your views here.

def index(request):
    usuarios = Usuario.objects.all()
    return render(request, 'index.html', {'usuarios': usuarios})

def login_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        pin = request.POST.get('pin')

        if not nombre or not pin:
            messages.error(request, "Por favor, ingrese el nombre de usuario y el PIN.")
            return render(request, 'login_fail.html')

        try:
            
            usuario = Usuario.objects.get(nombre=nombre)

            tarjeta = Tarjeta.objects.get(cuenta_perteneciente=usuario, pin=pin)

            messages.success(request, f"Bienvenido, {usuario.nombre}!")
            return redirect('index/')  

        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return render(request, 'login_fail.html')  # Redirige al login_fail.html
        except Tarjeta.DoesNotExist:
            messages.error(request, "PIN incorrecto.")
            return render(request, 'login_fail.html')  # Redirige al login_fail.html

    return render(request, 'login.html')