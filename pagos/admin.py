##Admin de pagos
from django.contrib import admin
from datetime import datetime
from django.db import transaction

from .models import *
# Register your models here.

#CREAR ESTADO DE CUENTA

class NominaAdmin(admin.ModelAdmin):
    readonly_fields=('nomina_fecha', 'nomina_comision', 'nomina_bonificacion', 
                    'nomina_bono', 'nomina_aguinaldo', 'nomina_igss', 'nomina_tienda', 'nomina_prestamo',
                    'nomina_neto','nomina_sueldo_base','nomina_aumento_total',
                    'nomina_extras_calculada','nomina_dobles_calculada',
                    'nomina_ingreso_total','nomina_descuento_total','nomina_aporte',)

    fields = [('nomina_fecha'),
              ('nomina_empleado_id', 'nomina_sueldo_base', 'nomina_aumento_total'),
              ('nomina_aporte'),
              ('nomina_extras','nomina_extras_calculada'),
              ('nomina_dobles','nomina_dobles_calculada'),
               ('nomina_ventas', 'nomina_comision'),
                ('nomina_piezas','nomina_bonificacion'), 
                ('nomina_igss','nomina_tienda','nomina_prestamo'),
                ('nomina_ingreso_total','nomina_descuento_total', 'nomina_neto')
                ]
    list_display = ('nomina_id', 'nomina_empleado_id','nomina_ingreso_total',)
    list_display_links = ["nomina_empleado_id"]

class PrestamoAdmin(admin.ModelAdmin):
    readonly_fields=('prestamo_saldo','prestamo_mensualidad','prestamo_aporte',)

    list_display = ('prestamo_empleado_id', 'prestamo_saldo','prestamo_mensualidad', 'prestamo_aporte',)

class AporteAdmin(admin.ModelAdmin):
    readonly_fields=('aporte_acumulado',)
    list_display = ('aporte_empleado_id', 'aporte_cantidad', 'aporte_acumulado',)

class IgssAdmin(admin.ModelAdmin):
    readonly_fields=('igss_cantidad',)
    list_display=('igss_empleado_id', 'igss_cantidad')


admin.site.register(Nomina, NominaAdmin)
admin.site.register(Aporte, AporteAdmin)
admin.site.register(Prestamo, PrestamoAdmin)
admin.site.register(Liquidacion)
admin.site.register(Igss, IgssAdmin)