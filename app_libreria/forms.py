from django import forms
from .models import Cliente, Venta

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'telefono', 'direccion', 'preferenciasgenero', 'foto_cliente']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ingrese la dirección completa'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej: +34 612 345 678'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'}),
        }
        labels = {
            'preferenciasgenero': 'Género Literario Preferido',
            'foto_cliente': 'Foto del Cliente'
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'montototal', 'metodopago', 'estadoVenta', 'descuentoAplicado']
        widgets = {
            'montototal': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'descuentoAplicado': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'}),
        }
        labels = {
            'montototal': 'Monto Total (€)',
            'descuentoAplicado': 'Descuento Aplicado (%)',
            'estadoVenta': 'Estado de la Venta'
        }