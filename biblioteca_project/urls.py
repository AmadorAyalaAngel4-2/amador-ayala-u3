from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from libros.soap_services import soap_view
from . import views as project_views # Alias para evitar conflicto si importas views de la app

# Importamos el router desde tu app libros
from libros.urls import router as libros_router

urlpatterns = [
    # 1. Página principal y Ejemplos (Tus views actuales del proyecto)
    path('', project_views.home, name='home'),
    path('ejemplos/rest/', project_views.ejemplos_rest, name='ejemplos_rest'),
    path('ejemplos/soap/', project_views.ejemplos_soap, name='ejemplos_soap'),
    path('ejemplos/admin/', project_views.ejemplos_admin, name='ejemplos_admin'),

    # 2. Admin de Django
    path('admin/', admin.site.urls),

    # 3. Servicio SOAP
    re_path(r'^soap/', soap_view),

    # 4. API REST (Conectado al Router)
    # Esto generará rutas como: /api/libros/, /api/autores/
    path('api/', include(libros_router.urls)),

    # 5. Vistas de la App Libros (Catálogo, Detalles, etc.)
    # Usamos include() sin prefijo para que sean accesibles como /catalogo/
    path('', include('libros.urls')),

    # 6. Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]