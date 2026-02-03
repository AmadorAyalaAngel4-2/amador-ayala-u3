from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para API REST
router = DefaultRouter()
router.register(r'libros', views.LibroViewSet)
router.register(r'autores', views.AutorViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'editoriales', views.EditorialViewSet)
router.register(r'prestamos', views.PrestamoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]