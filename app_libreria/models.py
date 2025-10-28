from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Cliente(models.Model):
    GENERO_PREFERENCIAS = [
        ('ficcion', 'Ficción'),
        ('ciencia_ficcion', 'Ciencia Ficción'),
        ('fantasia', 'Fantasía'),
        ('misterio', 'Misterio'),
        ('romance', 'Romance'),
        ('terror', 'Terror'),
        ('biografia', 'Biografía'),
        ('historia', 'Historia'),
        ('ciencia', 'Ciencia'),
        ('infantil', 'Infantil'),
    ]
    
    clienteid = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    fecharegistro = models.DateTimeField(default=timezone.now)
    preferenciasgenero = models.CharField(
        max_length=50, 
        choices=GENERO_PREFERENCIAS, 
        default='ficcion'
    )
    # ¡ESTE CAMPO DEBE ESTAR PRESENTE!
    foto_cliente = models.ImageField(upload_to='clientes_fotos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-fecharegistro']

class Venta(models.Model):
    ESTADOS_VENTA = [
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('reembolsada', 'Reembolsada'),
    ]
    
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('tarjeta_debito', 'Tarjeta de Débito'),
        ('transferencia', 'Transferencia'),
        ('paypal', 'PayPal'),
    ]
    
    ventaid = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ventas')
    fechaventa = models.DateTimeField(default=timezone.now)
    montototal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    metodopago = models.CharField(max_length=50, choices=METODOS_PAGO, default='efectivo')
    estadoVenta = models.CharField(max_length=50, choices=ESTADOS_VENTA, default='pendiente')
    descuentoAplicado = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f"Venta #{self.ventaid} - {self.cliente.nombre_completo()}"

    def monto_final(self):
        descuento = self.montototal * (self.descuentoAplicado / 100)
        return self.montototal - descuento

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fechaventa']