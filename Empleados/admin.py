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
    search_fields=["empleado_id", "empleado_nombre", "empleado_apellido"]
    list_per_page = 20
    list_display_links = ["empleado_nombre"]

    #ordering = ('active',) #ordenar por activo
    #date_hierarchy='fecha de creacion'

    def salario(self, obj):
        return f"Q.{obj.empleado_salario}"
    def aumento(self, obj):
        return f"Q.{obj.empleado_aumento}"

    def foto(self, object):
        return format_html ('<img src={} width="80" height="60" />', object.empleado_foto.url)
    def fecha_format(self, obj):
        return obj.empleado_contratacion.strftime('%d de %B del %Y')
    fecha_format.short_description = 'Fecha de contratacion'

class DepartamentoAdmin(admin.ModelAdmin):
    list_display=("departamento_id", 
                  "departamento_nombre"
                  )

class PuestoAdmin(admin.ModelAdmin):
    list_display=("puesto_departamento_id", 
                  "puesto_nombre", 
                  "puesto_cantidad"
                  )

class AumentoAdmin(admin.ModelAdmin):
    list_display=("aumento_empleado",
                  "fecha_formateada", 
                  "aumento_cantidad",)
    
    def fecha_formateada(self, obj):
        return obj.aumento_fecha.strftime('%d de %B del %Y')
    fecha_formateada.short_description = 'Fecha del Aumento'

    search_fields=["aumento_empleado__empleado_nombre", "aumento_empleado__empleado_id"]

class ExpedienteAdmin(admin.ModelAdmin):
    search_fields=["expediente_empleado_id"]


class AusenciaAdminForm(forms.ModelForm):
    class Meta:
        model = Ausencia
        fields = '__all__'
class AusenciaAdmin(admin.ModelAdmin):
    list_display=("ausencia_fecha", "ausencia_empleado_id", "ausencia_aprovacion", "ausencia_desNomina", "descuento",)
    
    def descuento(self, obj):
        return f"Q.{obj.ausencia_descuento}"

    form = AusenciaAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(AusenciaAdmin, self).get_form(request, obj, **kwargs)
        
        # Ocultar los campos ausencia_desNomina y ausencia_descuento si ausencia_aprovacion es False
        if obj and not obj.ausencia_aprovacion:
            form.base_fields['ausencia_desNomina'].widget = forms.HiddenInput()
            form.base_fields['ausencia_descuento'].widget = forms.HiddenInput()
        
        return form


admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Puesto, PuestoAdmin)
admin.site.register(Aumento, AumentoAdmin)
admin.site.register(Expediente, ExpedienteAdmin)
admin.site.register(Ausencia, AusenciaAdmin)
