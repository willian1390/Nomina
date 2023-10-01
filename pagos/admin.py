##Admin de pagos
from django.contrib import admin

from .models import *
# Register your models here.

#CREAR ESTADO DE CUENTA

class NominaAdmin(admin.ModelAdmin):
    readonly_fields=('nomina_fecha', 'nomina_interes', 'nomina_comision', 'nomina_bonificacion', 
                    'nomina_bono', 'nomina_aguinaldo', 'nomina_igss', 'nomina_tienda', 'nomina_prestamo',
                      'nomina_interes', 'nomina_neto','nomina_sueldo_base','nomina_aumento_total',
                        'nomina_extras_calculada','nomina_dobles_calculada',
                        'nomina_ingreso_total','nomina_descuento_total',)

    fields = [('nomina_fecha'),
              ('nomina_empleado_id', 'nomina_sueldo_base', 'nomina_aumento_total','nomina_interes'),
              ('nomina_extras','nomina_extras_calculada'),
              ('nomina_dobles','nomina_dobles_calculada'),
               ('nomina_ventas', 'nomina_comision'),
                ('nomina_piezas','nomina_bonificacion'), 
                ('nomina_igss','nomina_tienda','nomina_prestamo'),
                ('nomina_ingreso_total','nomina_descuento_total', 'nomina_neto')
                ]
    list_display = ('nomina_id', 'nomina_empleado_id','nomina_ingreso_total',)

admin.site.register(Nomina, NominaAdmin)
admin.site.register(Aporte)
admin.site.register(Prestamo)
admin.site.register(Liquidacion)