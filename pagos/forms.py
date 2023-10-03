from .models import Aporte, Empleado

def sumar_aporte(empleado_id, aporte_cantidad):
    # Obtener el objeto Aporte del empleado
    aporte = Aporte.objects.get(aporte_empleado_id=empleado_id)
    
    # Sumar el aporte mensual al acumulado
    aporte.aporte_acumulado += aporte_cantidad
    
    # Guardar los cambios en la base de datos
    aporte.save()