# Generated by Django 4.2.5 on 2023-09-30 20:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Empleados', '0023_alter_empleado_empleado_puesto'),
        ('pagos', '0007_remove_nomina_nomina_departamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='aporte',
            name='aporte_cantidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Monto'),
        ),
        migrations.AddField(
            model_name='aporte',
            name='aporte_empleado_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Empleados.empleado', verbose_name='Empleado'),
        ),
        migrations.AddField(
            model_name='aporte',
            name='aporte_fecha',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='liquidacion',
            name='liquidacion_empleado_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Empleados.empleado', verbose_name='Empleado'),
        ),
        migrations.AddField(
            model_name='liquidacion',
            name='liquidacion_fecha',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='liquidacion',
            name='liquidacion_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total'),
        ),
        migrations.AddField(
            model_name='prestamo',
            name='prestamo_cantidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Prestamo'),
        ),
        migrations.AddField(
            model_name='prestamo',
            name='prestamo_empleado_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Empleados.empleado', verbose_name='Empleado'),
        ),
        migrations.AddField(
            model_name='prestamo',
            name='prestamo_fecha',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prestamo',
            name='prestamo_interes',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Interes'),
        ),
        migrations.AddField(
            model_name='prestamo',
            name='prestamo_meses',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Tiempo'),
        ),
    ]
