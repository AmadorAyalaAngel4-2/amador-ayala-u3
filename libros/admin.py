from django.contrib import admin
from .models import Autor, Categoria, Editorial, Libro, Prestamo

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'nacionalidad', 'fecha_nacimiento']
    search_fields = ['nombre', 'apellido', 'nacionalidad']
    list_filter = ['nacionalidad']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais', 'sitio_web']
    search_fields = ['nombre', 'pais']
    list_filter = ['pais']

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'categoria', 'stock_disponible', 'estado']
    search_fields = ['titulo', 'isbn', 'autor__nombre', 'autor__apellido']
    list_filter = ['categoria', 'editorial', 'estado', 'idioma']
    readonly_fields = ['fecha_creacion']

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['libro', 'usuario', 'fecha_prestamo', 
                    'fecha_devolucion_esperada', 'estado']
    search_fields = ['libro__titulo', 'usuario__username']
    list_filter = ['estado', 'fecha_prestamo']
    readonly_fields = ['fecha_prestamo']