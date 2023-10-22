from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta, date, datetime
from decimal import Decimal
from Empleados.models import Empleado, Departamento, Ausencia
from tienda.models import CompraProducto

# Create your models here.
class Nomina(models.Model):
    nomina_id = models.AutoField(primary_key=True)
    nomina_fecha = models.DateTimeField(default=datetime.now())
    nomina_empleado_id = models.ForeignKey(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE, verbose_name="Empleado")
    #Ingresos del empleado
    nomina_sueldo_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sueldo Base", default=0)
    nomina_aumento_total= models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aumento", default=0) 
    nomina_extras = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Horas Extras", default=0) #aplica media hora despues del turno
    nomina_extras_calculada = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total horas extras", default=0, )
    nomina_dobles = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Horas dobles", default=0) #aplica dias festivos y domingos
    nomina_dobles_calculada = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total horas dobles", default=0, )
    #Aporte solidario
    nomina_aporte = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aporte Solidario", default=0)
    #Departamento de ventas
    nomina_ventas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Venta realizada (Depto. Ventas)", default=0, null=True, blank=True) #aplica solo a ventas
    nomina_comision = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Comision", default=0, null=True, blank=True)
    #Departamento de Produccion
    nomina_piezas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Piezas hechas (Depto. Produccion)", default=0, null=True, blank=True) #aplica solo a produccion 
    nomina_bonificacion = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Bonificacion", default=0, null=True, blank=True)
    #aplicar solo si es el mes correcto
    nomina_bono = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Bono 14", default=0, editable=False) #aplica solo si es julio
    nomina_aguinaldo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aguinaldo", default=0, editable=False) #aplica solo si es noviembre
    
    #Descuentos del empleado del empleado
    nomina_igss  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="IGSS", default=0)
    nomina_tienda = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Compras en tienda", default=0)
    nomina_prestamo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prestamo", default=0)
    nomina_ausencia = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ausencia", default=0)

    #Ingresos y descuentos totales
    nomina_ingreso_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ingreso total", default=0)
    nomina_descuento_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Descuento total", default=0)
    nomina_neto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sueldo Neto", default=0)

    def save(self, *args, **kwargs):
        #obtener el salario y aumentos del empleado        
        self.nomina_sueldo_base = self.nomina_empleado_id.empleado_salario
        self.nomina_aumento_total = self.nomina_empleado_id.empleado_aumento or 0
        #Calculo de horas extras
        sueldo_base = self.nomina_sueldo_base
        horas_extras = self.nomina_extras
        salario_hora = ((sueldo_base / 30) / 9) # sueldo base/ mes / 9 horas de trabajo
        salario_hora_decimal = Decimal(salario_hora)
        extra = (salario_hora_decimal*Decimal('1.5'))*horas_extras #salario por hora * 1.5 * horas realizadas por el empleado
        self.nomina_extras_calculada = extra
        #calculo de horas dobles
        horas_dobles = self.nomina_dobles
        if horas_dobles > 0:
            dobles = salario_hora * (1 + horas_dobles)
            self.nomina_dobles_calculada = dobles
        else:
            self.nomina_dobles_calculada = 0
        # Calcular el total de ausencia para el mismo mes y empleado
        nomina_mes = self.nomina_fecha.month
        nomina_anio = self.nomina_fecha.year
        ausencia_total = Ausencia.objects.filter(
            ausencia_empleado_id=self.nomina_empleado_id,
            ausencia_fecha__month=nomina_mes,
            ausencia_fecha__year=nomina_anio
        ).aggregate(total_ausencia=models.Sum('ausencia_descuento'))['total_ausencia']

        if ausencia_total is not None:
            self.nomina_ausencia = ausencia_total
        else:
            self.nomina_ausencia = 0
        #Guardar
        super(Nomina, self).save(*args, **kwargs)
    #cadena
    def __str__(self):
        return f"{self.nomina_empleado_id.empleado_nombre} { self.nomina_empleado_id.empleado_apellido}, {self.nomina_empleado_id.empleado_puesto}"
    
class Aporte(models.Model):
    aporte_id = models.AutoField(primary_key=True)
    aporte_fecha = models.DateTimeField(auto_now_add=True)
    aporte_empleado_id = models.ForeignKey(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE, verbose_name="Empleado")
    aporte_cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto", default=0)
    aporte_acumulado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Acumulado", default=0)
    #cadena
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
    prestamo_aporte = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aporte", default=0)
    #calcular la mensualidad
    def save(self, *args, **kwargs):
        prestamo = self.prestamo_cantidad
        meses = self.prestamo_meses
        interes = Decimal('0.00417')   #con un interes anual de 5% siendo 0.417% mensual
        mensualidad = (interes * prestamo) / (1-(1+interes)**(-meses)) #calcular la mensualidad
        self.prestamo_mensualidad = mensualidad
        super(Prestamo, self).save(*args, **kwargs)

class Igss(models.Model):
    igss_id = models.AutoField(primary_key=True)
    igss_fecha = models.DateTimeField(auto_now_add=True)
    igss_empleado_id = models.OneToOneField(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE, verbose_name="Empleado")
    igss_nac = models.DateField(verbose_name='Fecha de nacimiento', default=timezone.now)
    igss_sexo = models.CharField(max_length=50, verbose_name="Sexo", default='')
    igss_civil = models.CharField(max_length=50, verbose_name="Estado civil", default='Soltero')
    igss_nacion = models.CharField(max_length=50, verbose_name="Nacionalidad", default='Guatemalteca')
    igss_departamento = models.CharField(max_length=50, verbose_name="Departamento", default='')
    igss_municipio = models.CharField(max_length=50, verbose_name="Municipio", default='')
    igss_ncp = models.CharField(max_length=50, verbose_name="Nombre completo de Padre", default='')
    igss_ncm = models.CharField(max_length=50, verbose_name="Nombre completo de Madre", default='')
    igss_cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto", default=0)
    #cadena
    def __str__(self):
        return f"{self.igss_empleado_id.empleado_nombre} { self.igss_empleado_id.empleado_apellido}"
    #Definicion de nombre en singular y plural
    class Meta:
        verbose_name='IGSS'
        verbose_name_plural='IGSS'
    
class Bono14(models.Model):
    bono_id = models.AutoField(primary_key=True)
    bono_empleado_id = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Empleado")
    bono_fecha = models.DateField(auto_now_add=True)
    bono_monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Bono 14", default=0)
    #cadena
    def __str__(self):
        return f"{self.bono_empleado_id.empleado_nombre} { self.bono_empleado_id.empleado_apellido}"
    #Definicion de nombre en singular y plural
    class Meta:
        verbose_name='Bono 14'
        verbose_name_plural='Bono 14'

class Aguinaldo(models.Model):
    aguinaldo_id = models.AutoField(primary_key=True)
    aguinaldo_empleado_id = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Empleado")
    aguinaldo_fecha = models.DateField(auto_now_add=True)
    aguinaldo_monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aguinaldo", default=0)
    #cadena
    def __str__(self):
        return f"{self.aguinaldo_empleado_id.empleado_nombre} { self.aguinaldo_empleado_id.empleado_apellido}"

class Liquidacion(models.Model):
    liquidacion_id = models.AutoField(primary_key=True)
    liquidacion_fecha = models.DateTimeField(auto_now_add=True)
    liquidacion_empleado_id = models.ForeignKey(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE, verbose_name="Empleado")
    liquidacion_sm = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Promedio Sueldo Mensual", default=0)
    liquidacion_sc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Promedio Sueldo Correspondiente", default=0)
    liquidacion_ind = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Indemnizacion", default=0)
    liquidacion_ag = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aguinaldo pendiente", default=0)
    liquidacion_bn = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Bono 14 pendiente", default=0)
    liquidacion_vc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Vacaciones pendientes", default=0)
    liquidacion_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", default=0)

    def save(self, *args, **kwargs):
        empleado = self.liquidacion_empleado_id
        #sueldo mensual
        mensualidad_sm = self.liquidacion_empleado_id.empleado_salario + self.liquidacion_empleado_id.empleado_aumento
        #montos de bono y aguinaldo
        ultimo_bono = Bono14.objects.filter(bono_empleado_id=empleado).order_by('-bono_fecha').first()
        monto_bono = ultimo_bono.bono_monto if ultimo_bono else 0
        ultimo_aguinaldo = Aguinaldo.objects.filter(aguinaldo_empleado_id=empleado).order_by('-aguinaldo_fecha').first()
        monto_aguinaldo = ultimo_aguinaldo.aguinaldo_monto if ultimo_aguinaldo else 0
        #sueldo correspondiente
        mensualidad_sc = mensualidad_sm + monto_bono + monto_aguinaldo
        # Calcular días trabajados
        fecha_actual = date.today()
        dias_laborados = (fecha_actual - empleado.empleado_contratacion.date()).days
        #indemnizacion
        indemnizacion = (dias_laborados * mensualidad_sm) / 365
        #aguinaldo pendiente
        fecha_pasada_a = date(date.today().year - 1, 12, 1)
        dias_aguinaldo = (fecha_actual - fecha_pasada_a).days
        aguinaldo = (dias_aguinaldo * mensualidad_sm) / 365
        #bono pendiente
        fecha_pasada_b = date(date.today().year - 1, 7, 1)
        dias_bono = (fecha_actual - fecha_pasada_b).days
        bono = (dias_bono * mensualidad_sm) / 365
        #vacaciones
        fecha_contratacion = empleado.empleado_contratacion
        dias_vacaciones = (fecha_actual - fecha_contratacion.date()).days
        vacaciones_pendientes = (dias_vacaciones * 17) / 365
        sueldo_diario = mensualidad_sm / 30
        vacaciones = sueldo_diario * Decimal(vacaciones_pendientes)
        #total liquidacion
        total_liq = indemnizacion + aguinaldo + bono + vacaciones

        self.liquidacion_sm = mensualidad_sm
        self.liquidacion_sc = mensualidad_sc
        self.liquidacion_ind = indemnizacion
        self.liquidacion_bn = bono
        self.liquidacion_ag = aguinaldo
        self.liquidacion_vc = vacaciones
        self.liquidacion_total = total_liq

        super(Liquidacion, self).save(*args, **kwargs)
        #descativar estado del emplead
        if self.liquidacion_empleado_id:
            empleado = self.liquidacion_empleado_id
            empleado.empleado_estado = False  # Cambiar el estado a False
            empleado.save()
    #cadena
    def __str__(self):
        return f"{self.liquidacion_empleado_id.empleado_nombre} { self.liquidacion_empleado_id.empleado_apellido}, {self.liquidacion_empleado_id.empleado_puesto}"
    #Definicion de nombre en singular y plural
    class Meta:
        verbose_name='Liquidacion'
        verbose_name_plural='Liquidaciones'

@receiver(pre_save, sender=Bono14)
def calcular_bono_14(sender, instance, **kwargs):
    empleado = instance.bono_empleado_id
    salario_ordinario = empleado.empleado_salario + empleado.empleado_aumento
    # Calcular el bono 14 según las condiciones
    if empleado.empleado_contratacion + timedelta(days=365) <= timezone.now(): #timezone.now().month == 7 and
        # Más de un año trabajando
        instance.bono_monto = salario_ordinario
    else:
        # Menos de un año trabajando
        dias_laborados = (timezone.now() - empleado.empleado_contratacion).days
        monto = (salario_ordinario * dias_laborados) / 365
        instance.bono_monto = monto

@receiver(pre_save, sender=Aguinaldo)
def calcular_aguinaldo(sender, instance, **kwargs):
    empleado = instance.aguinaldo_empleado_id
    salario_ordinario = empleado.empleado_salario + empleado.empleado_aumento
    # Calcular el bono 14 según las condiciones
    if empleado.empleado_contratacion + timedelta(days=365) <= timezone.now(): #timezone.now().month == 11 and
        # Más de un año trabajando
        instance.aguinaldo_monto = salario_ordinario
    else:
        # Menos de un año trabajando
        dias_laborados = (timezone.now() - empleado.empleado_contratacion).days
        monto = (salario_ordinario * dias_laborados) / 365
        instance.aguinaldo_monto = monto

@receiver(post_save, sender=Nomina)
def actualizar_aporte(sender, instance, created, **kwargs):
    # Verificar si se creó una nueva instancia de Nomina
    if created:
        empleado = instance.nomina_empleado_id
        # Verificar si el empleado tiene un aporte
        try:
            aporte = Aporte.objects.get(aporte_empleado_id=empleado)
        except Aporte.DoesNotExist:
            aporte = None

        if aporte:
            # Actualizar el campo nomina_aporte de la instancia de Nomina
            instance.nomina_aporte = aporte.aporte_cantidad
            # Sumar el aporte del empleado 
            aumento_porcentaje = aporte.aporte_cantidad * Decimal('0.05')
            aporte.aporte_acumulado += aporte.aporte_cantidad + aumento_porcentaje
            # Guarda los cambios en el modelo Aporte
            aporte.save()
            # Guarda la instancia de Nomina actualizada
            instance.save()

@receiver(post_save, sender=Nomina)
def actualizar_prestamo(sender, instance, created, **kwargs):
    # Verificar si se creó una nueva instancia de Nomina
    if created:
        empleado = instance.nomina_empleado_id
        # Verificar si el empleado tiene un préstamo
        try:
            prestamo = Prestamo.objects.get(prestamo_empleado_id=empleado)
        except Prestamo.DoesNotExist:
            prestamo = None

        if prestamo:
            # Actualizar el campo nomina_prestamo de la instancia de Nomina
            instance.nomina_prestamo = prestamo.prestamo_mensualidad
            # Restar al prestamo del empleado
            prestamo.prestamo_aporte += prestamo.prestamo_mensualidad
            saldo = prestamo.prestamo_cantidad - prestamo.prestamo_aporte
            prestamo.prestamo_saldo = saldo
            # Guarda los cambios en el modelo Prestamo
            prestamo.save()
            # Guarda la instancia de Nomina actualizada
            instance.save()

@receiver(pre_save, sender=Igss)
def calcular_igss_cantidad(sender, instance, **kwargs):
    empleado = instance.igss_empleado_id
    salario = empleado.empleado_salario
    #calcular igss con el 4.83%
    igss_cantidad = salario * Decimal(0.0483)
    instance.igss_cantidad = igss_cantidad

@receiver(pre_save, sender=Nomina)
def actualizar_nomina_igss(sender, instance, **kwargs):
    empleado = instance.nomina_empleado_id
    #ingresar el a la nomina el igss correspondiente del empleado
    igss_registro = Igss.objects.filter(
        igss_empleado_id=empleado,
    ).first()
    if igss_registro:
        instance.nomina_igss = igss_registro.igss_cantidad
    
@receiver(post_save, sender=Nomina)
def calcular_bonificacion(sender, instance, created, **kwargs):
    # Verificar si el empleado pertenece al departamento de producción y si se creó una nueva instancia de Nomina
    if instance.nomina_empleado_id.empleado_departamento.departamento_nombre == 'Produccion' and created:
        # Realizar el cálculo de la bonificación
        piezas_realizadas = instance.nomina_piezas
        bonificacion = piezas_realizadas * Decimal('0.05')
        instance.nomina_bonificacion = bonificacion
        #instance.nomina_comision = 0
        instance.save()

@receiver(post_save, sender=Nomina)
def calcular_comision(sender, instance, created, **kwargs):
    # Verificar si el empleado pertenece al departamento de ventas y si se creó una nueva instancia de Nomina
    if instance.nomina_empleado_id.empleado_departamento.departamento_nombre == 'Ventas' and created:
        # Realizar el cálculo de la comisión
        ventas = instance.nomina_ventas
        if ventas <= Decimal('100000'):
            comision = ventas * Decimal('0.0')
        elif ventas <= Decimal('200000'):
            comision = ventas * Decimal('0.025')
        elif ventas <= Decimal('400000'):
            comision = ventas * Decimal('0.035')
        else:
            comision = ventas * Decimal('0.045')
        instance.nomina_comision = comision
        #instance.nomina_bonificacion = 0
        instance.save()

@receiver(post_save, sender=Nomina)
def actualizar_nomina_tienda(sender, instance, created, **kwargs):
    if created:
        empleado = instance.nomina_empleado_id
        # Verificar si el empleado posee compras en la tienda
        if empleado:
            # Filtrar las compras del empleado en el mes de la nómina
            compras_empleado = CompraProducto.objects.filter(
                compra__compra_empleado_id=empleado,
                compra__compra_fecha__month=instance.nomina_fecha.month,
                compra__compra_fecha__year=instance.nomina_fecha.year,
            )
            # Calcular el total de las compras del empleado en el mes
            total_compras = sum(compra.compra_total for compra in compras_empleado)

            # Ingresar en la nomina el total de compra
            instance.nomina_tienda = total_compras
            instance.save()

@receiver(post_save, sender=Nomina)
def calcular_ingreso_total(sender, instance, created, **kwargs):
    if created:
        # Realizar el cálculo del total de ingresos
        sueldo_base = instance.nomina_sueldo_base
        aumento = instance.nomina_aumento_total
        horas_extras = instance.nomina_extras_calculada
        horas_dobles = instance.nomina_dobles_calculada
        comision = instance.nomina_comision
        bonificacion = instance.nomina_bonificacion

        ingreso_total = (
            sueldo_base + aumento + horas_extras + horas_dobles + comision + bonificacion
        )

        #ingresar en la nomina el total de ingresos
        instance.nomina_ingreso_total = ingreso_total
        instance.save()

@receiver(post_save, sender=Nomina)
def calcular_descuento_total(sender, instance, created, **kwargs):
    if created:
        # Realizar el cálculo de descuentos
        igss = instance.nomina_igss
        prestamo = instance.nomina_prestamo
        tienda = instance.nomina_tienda
        aporte = instance.nomina_aporte

        descuento_total = igss + prestamo + tienda + aporte

        # Ingresar en la nomina el total de descuentos
        instance.nomina_descuento_total = descuento_total
        instance.save()

@receiver(post_save, sender=Nomina)
def calcular_neto(sender, instance, created, **kwargs):
    if created:
        # Realizar el cálculo de sueldo neto
        ingreso_total = instance.nomina_ingreso_total
        descuento_total = instance.nomina_descuento_total

        neto = ingreso_total - descuento_total

        # Ingrear en la nomina el sueldo neto
        instance.nomina_neto = neto
        instance.save()

