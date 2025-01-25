from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal

from .models import Usuario, Tarjeta, CuentaBancaria


# Create your views here.

def index(request):
    usuarios = Usuario.objects.all()
    return render(request, 'index.html', {'usuarios': usuarios})

def login_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        pin = request.POST.get('pin')

        if not nombre or not pin:
            return render(request, 'login_fail.html')
        try:
            usuario = Usuario.objects.get(nombre=nombre)
            tarjeta = Tarjeta.objects.get(cuenta_perteneciente=usuario)

            if tarjeta.pin == pin:
                messages.success(request, f"Bienvenido, {usuario.nombre}!")
                request.session['usuario_id'] = usuario.id_usuario
                return render(request, 'index.html', {'usuario': usuario})
            else:
                messages.error(request, "PIN incorrecto.")
                return render(request, 'login_fail.html')

        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return render(request, 'login_fail.html')
        except Tarjeta.DoesNotExist:
            messages.error(request, "No se encontró una tarjeta asociada a este usuario.")
            return render(request, 'login_fail.html')

    return render(request, 'login.html')

@login_required
def consultar_saldo(request):
    try:
        usuario_id = request.session.get('usuario_id')

        if not usuario_id:
            return render(request, 'error.html', {'mensaje': 'Usuario no autenticado.'})

        usuario = Usuario.objects.get(id_usuario=usuario_id)

        cuenta = CuentaBancaria.objects.get(propietario=usuario)
        saldo = cuenta.saldo

    except Usuario.DoesNotExist:
        return render(request, 'error.html', {'mensaje': 'Usuario no encontrado.'})
    except CuentaBancaria.DoesNotExist:
        return render(request, 'error.html', {'mensaje': 'Cuenta bancaria no encontrada.'})
    except Exception as e:
        return render(request, 'error.html', {'mensaje': f'Ocurrió un error: {e}'})

    return render(request, 'consultar_saldo.html', {'saldo': saldo})

@login_required
def realizar_retiro(request):
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')

        if not usuario_id:
            return render(request, 'saldo_insuficiente.html', {'mensaje': 'Usuario no autenticado.'})

        try:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
            cuenta = CuentaBancaria.objects.get(propietario=usuario)

            monto_retirar_str = request.POST.get('monto')

            if not monto_retirar_str:
                return render(request, 'saldo_insuficiente.html', {'mensaje': 'El monto no puede estar vacío.'})

            monto_retirar_str = monto_retirar_str.replace(',', '.')

            try:
                monto_retirar = Decimal(monto_retirar_str)

                if monto_retirar <= 0:
                    return render(request, 'saldo_insuficiente.html', {'mensaje': 'El monto debe ser mayor que 0.'})

            except ValueError:
                return render(request, 'saldo_insuficiente.html', {'mensaje': 'El monto ingresado no es válido.'})

            if monto_retirar > cuenta.saldo:
                return render(request, 'saldo_insuficiente.html', {'mensaje': 'El monto a retirar es mayor al saldo disponible.'})

            cuenta.saldo -= monto_retirar
            cuenta.save()

            return render(request, 'retiro_exito.html', {'nuevo_saldo': cuenta.saldo})

        except Usuario.DoesNotExist:
            return render(request, 'saldo_insuficiente.html', {'mensaje': 'Usuario no encontrado.'})
        except CuentaBancaria.DoesNotExist:
            return render(request, 'saldo_insuficiente.html', {'mensaje': 'Cuenta bancaria no encontrada.'})

    return render(request, 'retirar_saldo.html')