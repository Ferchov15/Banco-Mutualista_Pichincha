from django.contrib import admin
from .models import Usuario,Tarjeta,CuentaBancaria,Transacciones
# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin (admin.ModelAdmin):
        pass


@admin.register(Tarjeta)
class TarjetaAdmin (admin.ModelAdmin):
        pass

@admin.register(CuentaBancaria)
class CuentaBancariaAdmin (admin.ModelAdmin):
        pass

@admin.register(Transacciones)
class TransaccionesAdmin (admin.ModelAdmin):
        pass