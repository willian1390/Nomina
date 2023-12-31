# Generated by Django 4.2.5 on 2023-10-08 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Empleados', '0026_alter_empleado_empleado_esposa_and_more'),
        ('pagos', '0017_alter_nomina_nomina_piezas_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bono14',
            fields=[
                ('bono_id', models.AutoField(primary_key=True, serialize=False)),
                ('bono_fecha', models.DateField(auto_now_add=True)),
                ('bono_monto', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Bono 14')),
                ('bono_empleado_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empleados.empleado', verbose_name='Empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Aguinaldo',
            fields=[
                ('aguinaldo_id', models.AutoField(primary_key=True, serialize=False)),
                ('aguinaldo_fecha', models.DateField(auto_now_add=True)),
                ('aguinaldo_monto', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Aguinaldo')),
                ('aguinaldo_empleado_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empleados.empleado', verbose_name='Empleado')),
            ],
        ),
    ]
