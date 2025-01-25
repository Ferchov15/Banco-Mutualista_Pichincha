from django import  forms
from .models import Catalogo,Usuario, Tarjeta, CuentaBancaria, Transacciones


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'direccion', 'correo', 'cedula', 'telefono']
        widgets = {
            'correo': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}),
            'cedula': forms.TextInput(attrs={'placeholder': 'Cédula'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Número de Teléfono'}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if len(telefono) < 10:
            raise forms.ValidationError("El número de teléfono debe tener al menos 10 dígitos.")
        return telefono

class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ['numero_tarjeta', 'cuenta_perteneciente', 'fecha_emision', 'fecha_caducidad', 'estado_tarjeta', 'pin']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'fecha_caducidad': forms.DateInput(attrs={'type': 'date'}),
            'pin': forms.PasswordInput(),
        }

    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        if len(pin) != 4:
            raise forms.ValidationError("El PIN debe tener exactamente 4 dígitos.")
        return pin

class CuentaBancariaForm(forms.ModelForm):
    class Meta:
        model = CuentaBancaria
        fields = ['numero_cuenta', 'propietario', 'tipo_cuenta', 'saldo']
        widgets = {
            'saldo': forms.NumberInput(attrs={'min': '0'}),
        }

    def clean_numero_cuenta(self):
        numero_cuenta = self.cleaned_data.get('numero_cuenta')
        if not numero_cuenta.isdigit() or len(numero_cuenta) < 20:
            raise forms.ValidationError("El número de cuenta debe tener 20 dígitos.")
        return numero_cuenta
