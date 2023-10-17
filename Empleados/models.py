from django.db import models
#libreria para calcular suma de aumento
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, date
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
class Departamento(models.Model):
    departamento_id = models.AutoField(primary_key=True, verbose_name="ID",)
    departamento_nombre = models.CharField(max_length=50, verbose_name="Nombre")
    #restriccion de registros
    class Meta:
        unique_together = ('departamento_id','departamento_nombre')
    #cadena
    def __str__(self):
        return self.departamento_nombre

class Puesto(models.Model):
    puesto_id = models.AutoField(primary_key=True)
    puesto_departamento_id = models.ForeignKey(Departamento, verbose_name="Departamento", null=True, blank=True, on_delete=models.CASCADE, default=None)
    puesto_nombre = models.CharField(max_length=50, verbose_name="Nombre de puesto")
    puesto_cantidad = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Salario", default=0)
    #restriccion de registros
    class Meta:
        unique_together = ('puesto_id','puesto_nombre')
    #cadena
    def __str__(self):
        return f"{self.puesto_nombre} ({self.puesto_departamento_id})"

class Empleado(models.Model):
    empleado_id = models.AutoField(primary_key=True, verbose_name="ID",)
    empleado_estado = models.BooleanField(default=True, verbose_name="Activo")
    empleado_contratacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de contratacion")
    empleado_dpi = models.CharField(max_length=50, verbose_name="DPI")
    empleado_foto = models.ImageField(upload_to='empleados')
    empleado_nombre = models.CharField(max_length=50, verbose_name="Nombres")
    empleado_apellido = models.CharField(max_length=50, verbose_name="Apellidos")
    empleado_direccion = models.CharField(max_length=50, verbose_name="Direccion")
    empleado_telefono = models.CharField(max_length=50, verbose_name="Telefono")
    empleado_correo = models.EmailField(max_length=50, verbose_name="Correo")
    empleado_esposa = models.CharField(max_length=50, verbose_name="Esposo/a", null=True, blank=True,default='')
    empleado_hijos = models.TextField(verbose_name="Hijos", null=True, blank=True, default='')
    
    #llaves foraneas
    empleado_departamento = models.ForeignKey(Departamento, null=True, blank=True, on_delete=models.CASCADE, default=None)
    empleado_puesto  = models.ForeignKey(Puesto, null=False, default=None, blank=False, on_delete=models.CASCADE, verbose_name="Puesto")
    empleado_salario = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Salario", default=0, editable=False) #Depende del puesto que tenga
    empleado_aumento = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aumento total", default=0, null=True, blank=True)
    #cadena
    def __str__(self):
        return f"{self.empleado_nombre} {self.empleado_apellido}, {self.empleado_puesto}"
    #metodo para obtener el salario del puesto correspondiente
    def save(self, *args, **kwargs):
        puesto = self.empleado_puesto
        self.empleado_salario = puesto.puesto_cantidad
        super().save(*args, **kwargs)

class Aumento(models.Model):
    aumento_id = models.AutoField(primary_key=True)
    aumento_empleado = models.ForeignKey(Empleado, verbose_name="Empleado", on_delete=models.CASCADE)
    aumento_fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de aumento")
    aumento_cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    aumento_desc = models.CharField(max_length=50, verbose_name="Descripcion", default='')

    #agregar y sumar los aumentos al empleado
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        empleado = self.aumento_empleado        
        total_aumentos = empleado.empleado_aumento or 0 
        total_aumentos += self.aumento_cantidad 
        empleado.empleado_aumento = total_aumentos 
        empleado.save()
    #cadena
    def __str__(self):
        return f"{self.aumento_empleado} {self.get_fecha_formateada()}, {self.aumento_cantidad}"
    #formato de fecha sin hora
    def get_fecha_formateada(self):
        return self.aumento_fecha.strftime('%d de %B del %Y')

class Ausencia(models.Model):
    ausencia_id = models.AutoField(primary_key=True)
    ausencia_fecha = models.DateField(verbose_name="Fecha de ausencia", default=timezone.now)
    ausencia_empleado_id = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Empleado")
    ausencia_detalle = models.CharField(max_length=500, verbose_name="Detalle de ausencia")
    ausencia_aprovacion = models.BooleanField(default=False, verbose_name="Aprobar Ausencia")
    ausencia_descuento = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Descuento", default=0)
    #cadena
    def __str__(self):
        return f"{self.ausencia_empleado_id}"
    
class Expediente(models.Model):
    expediente_id = models.AutoField(primary_key=True, verbose_name="Expediente de Empleado")
    expediente_empleado_id = models.ForeignKey(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE, verbose_name='Empleado')
    expediente_titulo = models.TextField(max_length=150, verbose_name="Titulo")
    expediente_otitulo = models.TextField(max_length=500, verbose_name="Otros Titulos", null=True, blank=True)
    #pdf de expedientes
    expediente_pdf_dpi = models.FileField(
        upload_to='expediente',
        verbose_name="DPI",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        default=None
    )
    expediente_pdf_cv = models.FileField(
        upload_to='expediente',
        verbose_name="Curriculum",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        default=None
    )
    expediente_pdf_titulo = models.FileField(
        upload_to='expediente',
        verbose_name="Foto de titulo principal",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        default=None
    )
    expediente_pdf_penal = models.FileField(
        upload_to='expediente',
        verbose_name="Antecedentes Penales",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        default=None
    )
    expediente_pdf_polic = models.FileField(
        upload_to='expediente',
        verbose_name="Antecedente Policiaco",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        default=None
    )
    #cadena
    def __str__(self):
        return f"Expediente de Empleado: {self.expediente_empleado_id}"

#metodo que valida que el documento sea de formato pdf
def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Solo se permiten archivos PDF.')
    
#metodo para restar de un aumento el aumento ingresado    
@receiver(post_delete, sender=Aumento)
def eliminar_aumento(sender, instance, **kwargs):
    empleado = instance.aumento_empleado  
    if empleado:
        empleado.empleado_aumento -= instance.aumento_cantidad 
        empleado.save()