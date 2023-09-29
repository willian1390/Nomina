##Admin de pagos
from django.contrib import admin

from .models import Nomina
# Register your models here.

#CREAR ESTADO DE CUENTA

class NominaAdmin(admin.ModelAdmin):
    """readonly_fields=('nomina_fecha', 'nomina_interes', 'nomina_comision', 'nomina_bonificacion', 
                    'nomina_bono', 'nomina_aguinaldo', 'nomina_igss', 'nomina_tienda', 'nomina_interes', 'nomina_neto',) """
    list_display = ('nomina_id', 'nomina_empleado_id','nomina_ingreso_total', 'nomina_descuento_total' , 'nomina_neto',)

admin.site.register(Nomina, NominaAdmin)