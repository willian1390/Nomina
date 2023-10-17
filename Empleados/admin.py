#admin de Empleados
from django.contrib import admin
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.html import format_html
from django import forms
from .models import *

# Register your models here.
class EmpleadoAdmin(admin.ModelAdmin):
    readonly_fields=('empleado_contratacion','empleado_aumento',)
    list_display=("empleado_id",
                  "empleado_nombre",
                  "empleado_apellido",
                  "empleado_puesto", 
                  "fecha_format", 
                  "salario",
                  "aumento",
                  "foto",
                  "empleado_estado"
                  )
    search_fields=["empleado_id", "empleado_nombre", "empleado_apellido",]
    list_per_page = 20
    list_display_links = ["empleado_nombre"]
    ordering = ['-empleado_estado'] 
    list_filter = ('empleado_departamento',)
    #mostrar salario y aumento con 'Q' al inicio
    def salario(self, obj):
        return f"Q.{obj.empleado_salario}"
    def aumento(self, obj):
        return f"Q.{obj.empleado_aumento}"
    #mostrar la foto del empleado
    def foto(self, object):
        return format_html ('<img src={} width="80" height="60" />', object.empleado_foto.url)
    #mostrar formato de fecha sin hora
    def fecha_format(self, obj):
        return obj.empleado_contratacion.strftime('%d de %B del %Y')
    fecha_format.short_description = 'Fecha de contratacion'

class DepartamentoAdmin(admin.ModelAdmin):
    list_display=("departamento_id", 
                  "departamento_nombre"
                  )
    list_display_links = ["departamento_nombre"]
    
class PuestoAdmin(admin.ModelAdmin):
    list_display=("puesto_nombre", 
                  "puesto_departamento_id", 
                  "puesto_cantidad"
                  )

class AumentoAdmin(admin.ModelAdmin):
    list_display=("aumento_empleado",
                  "fecha_formateada", 
                  "aumento_cantidad",)
    search_fields=["aumento_empleado__empleado_nombre", "aumento_empleado__empleado_id"]
    list_per_page = 20
    #mostrar formato de fecha sin hora
    def fecha_formateada(self, obj):
        return obj.aumento_fecha.strftime('%d de %B del %Y')
    fecha_formateada.short_description = 'Fecha del Aumento'

class ExpedienteAdmin(admin.ModelAdmin):
    list_display =('__str__','foto')
    search_fields=["expediente_empleado_id__empleado_nombre"]
    list_filter = ('expediente_empleado_id__empleado_departamento',)
    list_per_page = 20
    #mostrar la foto del empleado
    def foto(self, object):
        return format_html ('<img src={} width="80" height="60" />', object.expediente_empleado_id.empleado_foto.url)

class AusenciaAdmin(admin.ModelAdmin):
    list_display = ('ausencia_empleado_id', 'ausencia_fecha', 'ausencia_aprovacion', 'descuento')
    readonly_fields = ( 'ausencia_descuento',)
    list_per_page = 20
    #mostrar  con 'Q' al inicio
    def descuento(self, obj):
        return f"Q.{obj.ausencia_descuento}"
    #metodo - si se aprueba la ausencia entonces se puede ingresar un descuento o se deja en cero
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj and obj.ausencia_aprovacion:
            readonly_fields.remove('ausencia_descuento')
        return readonly_fields





admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Puesto, PuestoAdmin)
admin.site.register(Aumento, AumentoAdmin)
admin.site.register(Expediente, ExpedienteAdmin)
admin.site.register(Ausencia, AusenciaAdmin)
