from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from datetime import date
from django.core.exceptions import ValidationError

class Catalogo(models.Model):
    id_catalogo = models.AutoField(primary_key=True)
    CATEGORIA_CHOICES = [
        ('TIPO_CUENTA', 'Tipo de Cuenta'),
        ('TIPO_TRANSACCION', 'Tipo de Transacción'),
        ('ESTADO_TARJETA', 'Estado de Tarjeta'),
    ]

    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIA_CHOICES,
        verbose_name="Categoría"
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Catálogo"
        verbose_name_plural = "Catálogos"

    def __str__(self):
        return f"{self.get_categoria_display()}: {self.nombre}"

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False, verbose_name="Nombre")
    apellido = models.CharField(max_length=50, null=False, verbose_name="Apellido")
    direccion = models.CharField(max_length=100, null=False, verbose_name="Dirección")
    correo = models.EmailField(max_length=100, null=False, unique=True, verbose_name="Correo Electrónico")
    cedula = models.CharField(
        max_length=20,  # Ajusta según el formato de tu país
        validators=[
            MinLengthValidator(10, message="La cédula debe tener al menos 10 dígitos."),
            RegexValidator(r'^\d+$', message="La cédula debe contener solo números.")
        ],
        unique=True,  # Asegura que no haya duplicados
        verbose_name="Cédula"
    )
    telefono = models.CharField(
        max_length=15,  # Ajusta según el formato de tu país
        validators=[
            MinLengthValidator(10, message="El número de teléfono debe tener al menos 10 dígitos."),
            RegexValidator(r'^\d+$', message="El número de teléfono debe contener solo números.")
        ],
        verbose_name="Teléfono"
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.correo}"
    class Meta:
        indexes = [
            models.Index(fields=['cedula']),
        ]

class Tarjeta(models.Model):
    id_tarjeta = models.AutoField(primary_key=True)
    numero_tarjeta = models.CharField(
        max_length=16,  
        validators=[
            MinLengthValidator(16, message="El número de la tarjeta debe tener exactamente 16 dígitos."),
            RegexValidator(r'^\d+$', message="El número de la tarjeta debe contener solo números.")
        ],
        unique=True,
        verbose_name="Número de Tarjeta"
    )
    cuenta_perteneciente = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,  
        related_name="tarjetas",  
        verbose_name="Cuenta Perteneciente"
    )
    fecha_emision = models.DateField(
        default=date.today,  
        verbose_name="Fecha de Emisión"
    )
    fecha_caducidad = models.DateField(
        verbose_name="Fecha de Caducidad"
    )
    estado_tarjeta = models.ForeignKey(
        Catalogo,
        on_delete=models.CASCADE,
        limit_choices_to={'categoria': 'ESTADO_TARJETA'},
        verbose_name="Estado de Tarjeta"
    )

    pin = models.CharField(
        max_length=4,  
        validators=[
            MinLengthValidator(4, message="El PIN debe tener 4 dígitos."),
            RegexValidator(r'^\d+$', message="El PIN debe contener solo números.")
        ],
        verbose_name="PIN"
    )

    def __str__(self):
        return f"Tarjeta {self.numero_tarjeta} - Estado: {self.estado_tarjeta}"
    class Meta:
        indexes = [
            models.Index(fields=['numero_tarjeta']),
        ]
    
class CuentaBancaria(models.Model):
    id_cuenta = models.AutoField(primary_key=True)
    numero_cuenta = models.CharField(max_length=20, unique=True, verbose_name="Número de Cuenta")
    propietario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True,verbose_name="Nombre del Propietario")   
    tipo_cuenta = models.ForeignKey(
        Catalogo,  
        on_delete=models.CASCADE,
        limit_choices_to={'categoria': 'TIPO_CUENTA'},
        verbose_name="Tipo de Cuenta"
    )
    
    saldo = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Saldo Disponible"
    )

    def __str__(self):
        return f"{self.numero_cuenta} - {self.propietario}"

    class Meta:
        verbose_name = "Cuenta Bancaria"
        verbose_name_plural = "Cuentas Bancarias"

    class Meta:
        indexes = [
            models.Index(fields=['numero_cuenta']),
        ]    
        

class Transacciones(models.Model):
    id_transacciones = models.AutoField(primary_key=True)
    tipo_transaccion = models.ForeignKey(
        Catalogo,
        on_delete=models.CASCADE,
        limit_choices_to={'categoria': 'TIPO_TRANSACCION'},
        verbose_name="Tipo de transaccion"
    )
    monto = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Monto de la Transacción"
    )

    fecha_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y Hora de la Transacción"
    )

    cuenta_emision = models.ForeignKey(
        CuentaBancaria,
        on_delete=models.CASCADE,
        related_name='transacciones_emision',
        verbose_name="Cuenta de Emisión"
    )

    cuenta_destino = models.ForeignKey(
        CuentaBancaria,
        on_delete=models.CASCADE,
        related_name='transacciones_destino',
        verbose_name="Cuenta de Destino"
    )

    descripcion = models.TextField(
        blank=True, null=True, verbose_name="Descripción de la Transacción"
    )

    def __str__(self):
        return f"Transacción {self.id_transacciones} - {self.tipo_transaccion}"
    
    def clean(self):
        if self.monto <= 0:
            raise ValidationError("El monto debe ser mayor a 0.")
        if self.cuenta_emision.saldo < self.monto:
            raise ValidationError(f"La cuenta de emisión no tiene suficiente saldo. Saldo disponible: {self.cuenta_emision.saldo}")
        
    def save(self, *args, **kwargs):
        self.clean()

        self.cuenta_emision.saldo -= self.monto
        self.cuenta_emision.save()

        self.cuenta_destino.saldo += self.monto
        self.cuenta_destino.save()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        ordering = ['-fecha_hora']
    class Meta:
        indexes = [
            models.Index(fields=['id_transacciones']),
        ] 