from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from decimal import Decimal
from Empleados.models import Empleado, Departamento

# Create your models here.
class Nomina(models.Model):
    nomina_id = models.AutoField(primary_key=True)
    nomina_fecha = models.DateTimeField(auto_now_add=True)
    nomina_empleado_id = models.ForeignKey(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE, verbose_name="Empleado")
    #Ingresos del empleado
    nomina_sueldo_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sueldo Base", default=0)
    nomina_aumento_total= models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aumento", default=0) 
    nomina_extras = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Horas Extras", default=0) #aplica media hora despues del turno
    nomina_extras_calculada = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total horas extras", default=0, )
    nomina_dobles = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Horas dobles", default=0) #aplica dias festivos y domingos
    nomina_dobles_calculada = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total horas dobles", default=0, )
    #Aporte solidarrio
    nomina_aporte = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aporte total", default=0)
    nomina_interes = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Interes mensual", default=0)
    #Departamento de ventas
    nomina_ventas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Venta realizada (Depto. Ventas)", default=0) #aplica solo a ventas
    nomina_comision = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Comision", default=0)
    #Departamento de Produccion
    nomina_piezas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Piezas hechas (Depto. Produccion)", default=0) #aplica solo a produccion 
    nomina_bonificacion = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Bonificacion", default=0)
    #aplicar solo si es el mes correcto
    nomina_bono = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Bono 14", default=0, editable=False) #aplica solo si es julio
    nomina_aguinaldo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aguinaldo", default=0, editable=False) #aplica solo si es noviembre
    
    #Descuentos del empleado del empleado
    nomina_igss  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="IGSS", default=0)
    nomina_tienda = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Compras en tienda", default=0)
    nomina_prestamo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prestamo", default=0)

    #Ingresos y descuentos totales
    nomina_ingreso_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ingreso total", default=0)
    nomina_descuento_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Descuento total", default=0)
    nomina_neto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sueldo Neto", default=0)

    def save(self, *args, **kwargs):
        
        self.nomina_sueldo_base = self.nomina_empleado_id.empleado_salario
        self.nomina_aumento_total = self.nomina_empleado_id.empleado_aumento or 0
        #Calculo de horas extras
        sueldo_base = self.nomina_sueldo_base
        horas_extras = self.nomina_extras
        salario_hora = ((sueldo_base / 30) / 9)
        salario_hora_decimal = Decimal(salario_hora)
        extra = (salario_hora_decimal*Decimal('1.5'))*horas_extras
        self.nomina_extras_calculada = extra
        #calculo de horas dobles
        horas_dobles = self.nomina_dobles
        if horas_dobles > 0:
            dobles = salario_hora * (1 + horas_dobles)
            self.nomina_dobles_calculada = dobles
        else:
            self.nomina_dobles_calculada = 0
        
        #calculo de ingresos
        sueldo = self.nomina_empleado_id.empleado_salario + self.nomina_empleado_id.empleado_aumento + self.nomina_extras_calculada + self.nomina_dobles_calculada
        self.nomina_ingreso_total = sueldo
        #calculo de descuentos
        
        #calculo pago neto
        super(Nomina, self).save(*args, **kwargs)

    def calcular_ingresos_totales(self):
            ingresos = self.nomina_sueldo_base + self.nomina_aumento_total + self.nomina_extras_calculada + self.nomina_dobles_calculada + self.nomina_comision + self.nomina_bonificacion
            self.nomina_ingreso_total = ingresos
            self.save()
            return ingresos

    def calcular_bono_14(self, empleado):
        if empleado.empleado_contratacion and empleado.empleado_contratacion <= date(date.today().year, 7, 15):
            # El empleado ha trabajado en la empresa durante más de un año
            self.nomina_bono = empleado.empleado_salario
        else:
            # El empleado ha trabajado en la empresa menos de un año
            if empleado.empleado_contratacion:
                dias_laborados = (date(date.today().year, 7, 15) - empleado.empleado_contratacion).days
                self.nomina_bono = (empleado.empleado_salario * dias_laborados) / 365
            else:
                self.nomina_bono = 0  # No hay fecha de contratación
        self.calcular_bono_14(empleado)

    def calcular_aguinaldo(self, empleado):
        if empleado.empleado_contratacion:
            if empleado.empleado_contratacion.year == date.today().year:
                # El empleado fue contratado durante el mismo año
                dias_laborados = (date.today() - empleado.empleado_contratacion).days
            else:
                # El empleado fue contratado en años anteriores
                dias_laborados = (date(date.today().year, 11, 15) - empleado.empleado_contratacion).days

            promedio_sueldo_base_anual = empleado.empleado_salario * 12  # Sueldo base mensual multiplicado por 12 meses
            if dias_laborados < 365:
                # El empleado lleva menos de un año en la empresa
                self.nomina_aguinaldo = (dias_laborados * promedio_sueldo_base_anual) / 365
            else:
                # El empleado lleva más de un año en la empresa
                self.nomina_aguinaldo = (365 * promedio_sueldo_base_anual) / 365
        else:
            self.nomina_aguinaldo = 0  # No hay fecha de contratación
        self.calcular_aguinaldo(empleado)

    def __str__(self):
        return f"{self.nomina_empleado_id.empleado_nombre} { self.nomina_empleado_id.empleado_apellido}, {self.nomina_empleado_id.empleado_puesto}"
    

class Aporte(models.Model):
    aporte_id = models.AutoField(primary_key=True)
    aporte_fecha = models.DateTimeField(auto_now_add=True)
    aporte_empleado_id = models.ForeignKey(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE, verbose_name="Empleado")
    aporte_cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto", default=0)
    aporte_acumulado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Acumulado", default=0)
    
    def __str__(self):
        return f"{self.aporte_empleado_id.empleado_nombre} { self.aporte_empleado_id.empleado_apellido}, {self.aporte_acumulado}"

class Prestamo(models.Model):
    prestamo_id = models.AutoField(primary_key=True)
    prestamo_fecha = models.DateTimeField(auto_now_add=True)
    prestamo_empleado_id = models.ForeignKey(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE, verbose_name="Empleado")
    prestamo_cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prestamo", default=0)
    prestamo_meses = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tiempo (6, 12 y 18 M)")
    prestamo_mensualidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Mensualidades", default=0)
    prestamo_saldo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Saldo", default=0)

    def save(self, *args, **kwargs):
        self.prestamo_saldo = self.prestamo_cantidad
        prestamo = self.prestamo_cantidad
        meses = self.prestamo_meses
        interes = Decimal('0.00417')
        mensualidad = (interes * prestamo) / (1-(1+interes)**(-meses))
        self.prestamo_mensualidad = mensualidad
        super(Prestamo, self).save(*args, **kwargs)

class Liquidacion(models.Model):
    liquidacion_id = models.AutoField(primary_key=True)
    liquidacion_fecha = models.DateTimeField(auto_now_add=True)
    liquidacion_empleado_id = models.ForeignKey(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE, verbose_name="Empleado")
    liquidacion_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", default=0)

class Igss(models.Model):
    igss_id = models.AutoField(primary_key=True)
    igss_fecha = models.DateTimeField(auto_now_add=True)
    igss_empleado_id = models.OneToOneField(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE, verbose_name="Empleado")
    igss_cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto", default=0)

@receiver(post_save, sender=Nomina)
def actualizar_prestamo(sender, instance, created, **kwargs):
    # Verifica si se creó una nueva instancia de Nomina
    if created:
        empleado = instance.nomina_empleado_id
        # Verifica si el empleado tiene un préstamo
        try:
            prestamo = Prestamo.objects.get(prestamo_empleado_id=empleado)
        except Prestamo.DoesNotExist:
            prestamo = None

        if prestamo:
            # Resta la mensualidad del préstamo al saldo actual
            prestamo_mensualidad = prestamo.prestamo_mensualidad
            prestamo.prestamo_saldo -= prestamo_mensualidad
            prestamo.save()
            # Actualiza el campo nomina_prestamo de la instancia de Nomina
            instance.nomina_prestamo = prestamo_mensualidad
            instance.save()


@receiver(pre_save, sender=Igss)
def calcular_igss_cantidad(sender, instance, **kwargs):
    empleado = instance.igss_empleado_id
    salario = empleado.empleado_salario
    igss_cantidad = salario * Decimal(0.0483)
    instance.igss_cantidad = igss_cantidad

@receiver(pre_save, sender=Nomina)
def actualizar_nomina_igss(sender, instance, **kwargs):
    empleado = instance.nomina_empleado_id
    igss_registro = Igss.objects.filter(
        igss_empleado_id=empleado,
    ).first()
    if igss_registro:
        instance.nomina_igss = igss_registro.igss_cantidad
    
@receiver(post_save, sender=Nomina)
def calcular_bonificacion(sender, instance, created, **kwargs):
    # Verifica si el empleado pertenece al departamento de producción y si se creó una nueva instancia de Nomina
    if instance.nomina_empleado_id.empleado_departamento.departamento_nombre == 'Produccion' and created:
        # Realizar el cálculo de la bonificación
        piezas_realizadas = instance.nomina_piezas
        bonificacion = piezas_realizadas * Decimal('0.05')
        instance.nomina_bonificacion = bonificacion
        instance.save()

@receiver(post_save, sender=Nomina)
def calcular_comision(sender, instance, created, **kwargs):
    # Verifica si el empleado pertenece al departamento de ventas y si se creó una nueva instancia de Nomina
    if instance.nomina_empleado_id.empleado_departamento.departamento_nombre == 'Ventas' and created:
        # Realizar el cálculo de la comisión
        ventas = instance.nomina_ventas
        comision = ventas * Decimal('0.05')
        instance.nomina_comision = comision
        instance.save()

