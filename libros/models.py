from django.db import models
from django.contrib.auth.models import User

class Autor(models.Model):
    """Modelo para autores de libros"""
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

class Categoria(models.Model):
    """Modelo para categorías de libros"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Editorial(models.Model):
    """Modelo para editoriales"""
    nombre = models.CharField(max_length=200, unique=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Editorial"
        verbose_name_plural = "Editoriales"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Libro(models.Model):
    """Modelo principal para libros"""
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('mantenimiento', 'En Mantenimiento'),
    ]
    
    titulo = models.CharField(max_length=300)
    isbn = models.CharField(max_length=13, unique=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='libros')
    editorial = models.ForeignKey(Editorial, on_delete=models.SET_NULL, null=True, related_name='libros')
    fecha_publicacion = models.DateField()
    numero_paginas = models.PositiveIntegerField()
    idioma = models.CharField(max_length=50, default='Español')
    descripcion = models.TextField(blank=True, null=True)
    stock_total = models.PositiveIntegerField(default=1)
    stock_disponible = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    """Modelo para gestión de préstamos"""
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
        ('renovado', 'Renovado'),
    ]
    
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos')
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion_esperada = models.DateField()
    fecha_devolucion_real = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ['-fecha_prestamo']
    
    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario.username}"