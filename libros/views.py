from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .models import Libro, Autor, Categoria, Editorial, Prestamo
from .serializers import (
    LibroSerializer, AutorSerializer, CategoriaSerializer,
    EditorialSerializer, PrestamoSerializer
)

class LibroViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de libros via API REST"""
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'autor', 'editorial', 'estado']
    search_fields = ['titulo', 'isbn', 'autor__nombre', 'autor__apellido']
    ordering_fields = ['titulo', 'fecha_publicacion', 'stock_disponible']
    ordering = ['titulo']

class AutorViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de autores"""
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'apellido', 'nacionalidad']
    ordering_fields = ['nombre', 'apellido']
    ordering = ['apellido']

class CategoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de categorías"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class EditorialViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de editoriales"""
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PrestamoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de préstamos"""
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['estado', 'usuario', 'libro']
    ordering_fields = ['fecha_prestamo', 'fecha_devolucion_esperada']
    ordering = ['-fecha_prestamo']