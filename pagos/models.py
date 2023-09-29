from django.db import models
from Empleados.models import Empleado, Departamento

# Create your models here.
class Nomina(models.Model):
    nomina_id = models.AutoField(primary_key=True)
    nomina_fecha = models.DateTimeField(auto_now_add=True)
    nomina_empleado_id = models.ForeignKey(Empleado, null=False, default=None, blank=False, on_delete=models.CASCADE)
    #Ingresos del empleado
    nomina_sueldo_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sueldo Base", default=0)
    nomina_aumento_total= models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aumento", default=0) 
    nomina_extras = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Horas Extras", default=0) #aplica media hora despues del turno
    nomina_extras_calculada = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total horas extras", default=0, editable=False)
    nomina_dobles = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Horas dobles", default=0) #aplica dias festivos y domingos
    nomina_dobles_calculada = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total horas dobles", default=0, editable=False)
    nomina_interes = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Interes mensual", default=0, editable=False)
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


    """def calculos(self):
        salario_hora = ((self.nomina_sueldo_base/30)/9)
        self.nomina_extras_calculada = (salario_hora*1.5)*self.nomina_extras
        self.nomina_dobles_calculada = salario_hora+(salario_hora*nomina_dobles)
        self.nomina_ingreso_total = self.nomina_sueldo_base + self.nomina_aumento_total + self.nomina_extras_calculada + self.nomina_dobles_calculada + self.nomina_comision + self.nomina_bonificacion + self.nomina_interes
        self.nomina_descuento_total = self.nomina_igss + self.nomina_tienda + self.nomina_prestamo
        self.nomina_neto = self.nomina_ingreso_total - self.nomina_descuento_total """

    def save(self, *args, **kwargs):
        # Calcular el salario por hora
        salario_hora = (self.nomina_sueldo_base / 30) / 9

        # Calcular los valores de los atributos
        self.nomina_sueldo_base = self.nomina_empleado_id.empleado_salario
        self.nomina_aumento_total = self.nomina_empleado_id.empleado_aumento or 0
        self.nomina_extras_calculada = (salario_hora * 1.5) * (self.nomina_extras or 0)
        self.nomina_dobles_calculada = salario_hora * (self.nomina_dobles or 0)
        self.nomina_ingreso_total = (
            self.nomina_sueldo_base +
            self.nomina_aumento_total +
            self.nomina_extras_calculada +
            self.nomina_dobles_calculada +
            self.nomina_comision +
            self.nomina_bonificacion +
            self.nomina_interes
        )
        self.nomina_descuento_total = (
            self.nomina_igss +
            self.nomina_tienda +
            self.nomina_prestamo
        )
        self.nomina_neto = self.nomina_ingreso_total - self.nomina_descuento_total

        super(Nomina, self).save(*args, **kwargs)



    def save(self, *args, **kwargs):
        empleado = self.nomina_empleado_id
        #self.nomina_sueldo_base = self.nomina_empleado_id.empleado_salario
        #self.nomina_aumento_total = self.nomina_empleado_id.empleado_aumento or 0

        if empleado.empleado_departamento:
            if empleado.empleado_departamento.departamento_nombre == 'Ventas':
                # Calcula la comisión en función de las ventas
                if 0 <= self.nomina_ventas <= 100000:
                    self.nomina_comision = 0
                elif 100001 <= self.nomina_ventas <= 200000:
                    self.nomina_comision = 2.5
                elif 200001 <= self.nomina_ventas <= 400000:
                    self.nomina_comision = 3.5
                else:
                    self.nomina_comision = 4.5

                # La bonificación en ventas es 0 para el departamento de Ventas
                self.nomina_bonificacion = 0
            elif empleado.empleado_departamento.departamento_nombre == 'Produccion':
                # Calcula la bonificación en función de las piezas elaboradas
                self.nomina_bonificacion = float(self.nomina_piezas) * 0.05
                # La comisión en producción es 0
                self.nomina_comision = 0
            else:
                # Otros departamentos no tienen comisión ni bonificación
                self.nomina_comision = 0
                self.nomina_bonificacion = 0
        else:
            self.nomina_comision = 0
            self.nomina_bonificacion = 0

        super(Nomina, self).save(*args, **kwargs)

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
        return f"{self.nomina_id} {self.nomina_empleado_id}, {self.nomina_sueldo_base}"

class Aporte(models.Model):
    aporte_id = models.AutoField(primary_key=True)
class Prestamo(models.Model):
    prestamo_id = models.AutoField(primary_key=True)

class Liquidacion(models.Model):
    liquidacion_id = models.AutoField(primary_key=True)

#IGSS = sueldo base -bonificacion * 4.83%