from django.contrib import admin
from .models import Cliente, Venta

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['clienteid', 'nombre', 'apellido', 'email', 'telefono', 'fecharegistro', 'preferenciasgenero']
    list_filter = ['preferenciasgenero', 'fecharegistro']
    search_fields = ['nombre', 'apellido', 'email']
    readonly_fields = ['fecharegistro']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['ventaid', 'cliente', 'fechaventa', 'montototal', 'monto_final', 'metodopago', 'estadoVenta']
    list_filter = ['estadoVenta', 'metodopago', 'fechaventa']
    search_fields = ['cliente__nombre', 'cliente__apellido']
    readonly_fields = ['fechaventa']
    
    def monto_final(self, obj):
        return obj.monto_final()
    monto_final.short_description = 'Monto Final'