from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import Cliente, Venta
from .forms import ClienteForm, VentaForm

def listar_clientes(request):
    clientes = Cliente.objects.all()
    total_clientes = clientes.count()
    clientes_recientes = clientes.filter(fecharegistro__gte=timezone.now()-timedelta(days=30)).count()
    return render(request, 'listar_clientes.html', {
        'clientes': clientes,
        'total_clientes': total_clientes,
        'clientes_recientes': clientes_recientes
    })

def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, clienteid=cliente_id)
    ventas_cliente = cliente.ventas.all()
    total_ventas = ventas_cliente.count()
    total_gastado = ventas_cliente.aggregate(Sum('montototal'))['montototal__sum'] or 0
    promedio_compra = ventas_cliente.aggregate(Avg('montototal'))['montototal__avg'] or 0
    return render(request, 'detalle_cliente.html', {
        'cliente': cliente,
        'ventas_cliente': ventas_cliente,
        'total_ventas': total_ventas,
        'total_gastado': total_gastado,
        'promedio_compra': promedio_compra
    })

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app_libreria:listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'formulario_cliente.html', {'form': form, 'titulo': 'Registrar Nuevo Cliente'})

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, clienteid=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('app_libreria:detalle_cliente', cliente_id=cliente.clienteid)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'formulario_cliente.html', {'form': form, 'titulo': 'Editar Cliente'})

def borrar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, clienteid=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('app_libreria:listar_clientes')
    return render(request, 'confirmar_borrar.html', {'objeto': cliente, 'tipo': 'cliente'})

def listar_ventas(request):
    ventas = Venta.objects.all()
    total_ventas = ventas.count()
    ventas_hoy = ventas.filter(fechaventa__date=timezone.now().date()).count()
    ingresos_totales = sum(venta.monto_final() for venta in ventas)
    return render(request, 'listar_ventas.html', {
        'ventas': ventas,
        'total_ventas': total_ventas,
        'ventas_hoy': ventas_hoy,
        'ingresos_totales': ingresos_totales
    })

def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, ventaid=venta_id)
    return render(request, 'detalle_venta.html', {'venta': venta})

def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app_libreria:listar_ventas')
    else:
        form = VentaForm()
    return render(request, 'formulario_venta.html', {'form': form, 'titulo': 'Registrar Nueva Venta'})

def editar_venta(request, venta_id):
    venta = get_object_or_404(Venta, ventaid=venta_id)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('app_libreria:detalle_venta', venta_id=venta.ventaid)
    else:
        form = VentaForm(instance=venta)
    return render(request, 'formulario_venta.html', {'form': form, 'titulo': 'Editar Venta'})

def borrar_venta(request, venta_id):
    venta = get_object_or_404(Venta, ventaid=venta_id)
    if request.method == 'POST':
        venta.delete()
        return redirect('app_libreria:listar_ventas')
    return render(request, 'confirmar_borrar.html', {'objeto': venta, 'tipo': 'venta'})

def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_ventas = Venta.objects.count()
    ingresos_totales = sum(venta.monto_final() for venta in Venta.objects.all())
    ventas_recientes = Venta.objects.all().order_by('-fechaventa')[:5]
    clientes_recientes = Cliente.objects.all().order_by('-fecharegistro')[:5]
    return render(request, 'dashboard.html', {
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
        'ingresos_totales': ingresos_totales,
        'ventas_recientes': ventas_recientes,
        'clientes_recientes': clientes_recientes
    })