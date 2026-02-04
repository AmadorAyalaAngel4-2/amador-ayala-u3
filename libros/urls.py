from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

# --- Configuración de la API ---
# Definimos el router aquí para poder importarlo desde el urls.py principal
router = DefaultRouter()
router.register(r'libros', views.LibroViewSet)
router.register(r'autores', views.AutorViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'editoriales', views.EditorialViewSet)
router.register(r'prestamos', views.PrestamoViewSet)

# --- Configuración de Vistas Tradicionales (HTML) ---
urlpatterns = [
    # Nota: Quitamos el router de aquí para manejarlo en el archivo principal
    
    path('index/', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    
    # Corregí las rutas que tenían "//" vacíos agregando el parámetro <int:pk>
    path('libro/<int:pk>/', views.detalle_libro, name='detalle_libro'),
    
    path('busqueda/', views.busqueda, name='busqueda'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
    
    path('solicitar-prestamo/<int:libro_id>/', views.solicitar_prestamo, name='solicitar_prestamo'),
    path('renovar-prestamo/<int:prestamo_id>/', views.renovar_prestamo, name='renovar_prestamo'),
]