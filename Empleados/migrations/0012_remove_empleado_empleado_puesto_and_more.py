# Generated by Django 4.2.5 on 2023-09-23 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Empleados', '0011_remove_empleado_empleado_departamento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empleado',
            name='empleado_puesto',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='empleado_salario',
        ),
    ]