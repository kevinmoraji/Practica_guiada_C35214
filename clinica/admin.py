from django.contrib import admin
from .models import Propietario, Mascota, ConsultaVeterinaria

@admin.register(Propietario)
class PropietarioAdmin(admin.ModelAdmin):
    lidst_display = ('identificacion', 'nombre', 'telefono', 'email')


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'fecha_nacimiento', 'peso', 'activo', 'propietario')


@admin.register(ConsultaVeterinaria)
class ConsultaVeterinariaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'fecha', 'motivo', 'diagnostico', 'tratamiento', 'costo')

