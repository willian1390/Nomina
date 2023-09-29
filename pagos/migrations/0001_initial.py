# Generated by Django 4.2.5 on 2023-09-24 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Empleados', '0020_ausencia_ausencia_fecha_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nomina',
            fields=[
                ('nomina_id', models.AutoField(primary_key=True, serialize=False)),
                ('nomina_fecha', models.DateTimeField(auto_now_add=True)),
                ('nomina_extras', models.IntegerField(verbose_name='Horas Extras')),
                ('nomina_dobles', models.IntegerField(verbose_name='Horas dobles')),
                ('nomina_comision', models.IntegerField(verbose_name='Comision')),
                ('nomina_bonificacion', models.IntegerField(verbose_name='Bono')),
                ('nomina_bono', models.IntegerField(verbose_name='Bono')),
                ('nomina_aguinaldo', models.IntegerField(verbose_name='Aguinaldo')),
                ('nomina_empleado_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Empleados.empleado')),
            ],
        ),
    ]
