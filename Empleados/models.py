from django.db import models
#libreria para calcular suma de aumento
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, date
from django.core.exceptions import ValidationError

# Create your models here.
class Departamento(models.Model):
    departamento_id = models.AutoField(primary_key=True, verbose_name="ID",)
    departamento_nombre = models.CharField(max_length=50, verbose_name="Nombre")
    class Meta:
        unique_together = ('departamento_id','departamento_nombre')

    def __str__(self):
        return self.departamento_nombre

class Puesto(models.Model):
    puesto_id = models.AutoField(primary_key=True)
    puesto_departamento_id = models.ForeignKey(Departamento, verbose_name="Departamento", null=True, blank=True, on_delete=models.CASCADE, default=None)
    puesto_nombre = models.CharField(max_length=50, verbose_name="Nombre de puesto")
    puesto_cantidad = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Salario", default=0)

    class Meta:
        unique_together = ('puesto_id','puesto_nombre')
        verbose_name='Puesto'
        verbose_name_plural='Puestos'
    
    def __str__(self):
        return f"{self.puesto_nombre} ({self.puesto_departamento_id})"

class Empleado(models.Model):
    empleado_id = models.AutoField(primary_key=True, verbose_name="ID",)
    empleado_estado = models.BooleanField(default=True, verbose_name="O")
    empleado_contratacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de contratacion")
    empleado_dpi = models.CharField(max_length=50, verbose_name="DPI")
    empleado_foto = models.ImageField(upload_to='empleados')
    empleado_nombre = models.CharField(max_length=50, verbose_name="Nombres")
    empleado_apellido = models.CharField(max_length=50, verbose_name="Apellidos")
    empleado_direccion = models.CharField(max_length=50, verbose_name="Direccion")
    empleado_telefono = models.CharField(max_length=50, verbose_name="Telefono")
    empleado_correo = models.EmailField(max_length=50, verbose_name="Correo")
    empleado_esposa = models.CharField(max_length=50, verbose_name="Esposa", null=True, blank=True,default='')
    empleado_hijos = models.TextField(verbose_name="Hijos", null=True, blank=True, default='')
    
    #llaves foraneas
    empleado_departamento = models.ForeignKey(Departamento, null=True, blank=True, on_delete=models.CASCADE, default=None)
    empleado_puesto  = models.ForeignKey(Puesto, null=False, default=None, blank=False, on_delete=models.CASCADE, verbose_name="Puesto")
    empleado_salario = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Salario", default=0, editable=False) #Depende del puesto que tenga
    empleado_aumento = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aumento total", default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.empleado_id} - {self.empleado_nombre} {self.empleado_apellido}, {self.empleado_puesto}"

    def save(self, *args, **kwargs):
        puesto = self.empleado_puesto
        self.empleado_salario = puesto.puesto_cantidad
        super().save(*args, **kwargs)

class Aumento(models.Model):
    aumento_id = models.AutoField(primary_key=True)
    aumento_empleado = models.ForeignKey(Empleado, verbose_name="Nombre de empleado y Puesto", on_delete=models.CASCADE)
    aumento_fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de aumento")
    aumento_cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad de aumento")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        empleado = self.aumento_empleado # Obtener el empleado asociado al aumento        
        total_aumentos = empleado.empleado_aumento or 0 # Obtener el total de aumentos acumulados hasta ahora
        total_aumentos += self.aumento_cantidad # Sumar el aumento actual al total acumulado
        empleado.empleado_aumento = total_aumentos # Actualizar el atributo empleado_aumento del empleado
        empleado.save()
        
    def __str__(self):
        return f"{self.aumento_empleado} {self.get_fecha_formateada()}, {self.aumento_cantidad}"
    
    def get_fecha_formateada(self):
        return self.aumento_fecha.strftime('%d de %B del %Y')

class Ausencia(models.Model):
    ausencia_id = models.AutoField(primary_key=True)
    ausencia_fecha = models.DateTimeField(verbose_name="Fecha de ausencia", default=timezone.now)
    ausencia_empleado_id = models.ForeignKey(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE, verbose_name="Empleado")
    ausencia_detalle = models.CharField(max_length=500, verbose_name="Detalle de ausencia")
    ausencia_aprovacion = models.BooleanField(default=False, verbose_name="Aprovar Ausencia")
    ausencia_desNomina = models.BooleanField(default=False, verbose_name="Descuento en nomina?", editable=False)
    ausencia_descuento = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Descuento", default=0)

    def clean(self):
        if self.ausencia_aprovacion:
            self.ausencia_desNomina.editable = True
            self.ausencia_descuento.editable = True
        else:
            self.ausencia_desNomina.editable = False
            self.ausencia_descuento.editable = False
        if self.ausencia_desNomina and not self.ausencia_descuento:
            raise ValidationError({'ausencia_descuento': ' Debe rellenar este campo por haber marcado "Descuento en nomina" '})
        elif not self.ausencia_desNomina and self.ausencia_descuento:
            self.ausencia_descuento = None

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Expediente(models.Model):
    expediente_id = models.AutoField(primary_key=True, verbose_name="Expediente de Empleado")
    expediente_empleado_id = models.ForeignKey(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE)
    expediente_titulo = models.TextField(max_length=500, verbose_name="Titulo Principal")
    expediente_otros_titulos = models.TextField(max_length=500, verbose_name="Otros Titulos", null=True, blank=True)
    expediente_titulo_foto = models.ImageField(upload_to='expediente', verbose_name="Foto de titulo principal")
    expediente_ant_penal = models.ImageField(upload_to='expediente', verbose_name="Antecedentes Penales")
    expediente_ant_policiaco = models.ImageField(upload_to='expediente', verbose_name="Antecedente Policiaco")

    def __str__(self):
        return f"{self.expediente_empleado_id.empleado_puesto}, {self.expediente_empleado_id.empleado_nombre} {self.expediente_empleado_id.empleado_apellido}, {self.expediente_titulo}"









 





