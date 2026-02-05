# Sistema de Gestión de Biblioteca (Django U3)

Este proyecto es una aplicación web integral para la gestión de una biblioteca, desarrollada como parte del curso de Servicios Web (Unidad 3). La plataforma permite administrar libros, autores, categorías y editoriales, además de gestionar el ciclo de vida de los préstamos de libros.

## 🚀 Características Principales

- **Dashboard de Usuario**: Resumen de actividades y acceso rápido a funciones.
- **Gestión de Catálogo**: CRUD completo de Libros, Autores, Categorías y Editoriales.
- **Sistema de Préstamos**: 
  - Solicitar préstamos de libros disponibles.
  - Renovar préstamos activos.
  - Control de estados (Activo, Devuelto, Vencido).
- **Estadísticas Visuales**: Gráficos dinámicos sobre la distribución de libros y préstamos.
- **Integraciones de Servicios**:
  - **API REST**: Implementada con Django REST Framework para facilitar la interoperabilidad.
  - **Servicio SOAP**: Implementado con Spyne para servicios web tradicionales.
- **Admin Customizado**: Interfaz administrativa optimizada para la gestión de datos.
- **Dockerizado**: Configuración lista para despliegue con Docker, MySQL y Nginx.

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3.11.9
- **Framework Web**: Django 5.x
- **APIs**: Django REST Framework
- **SOAP**: Spyne
- **Base de Datos**: MySQL
- **Contenedores**: Docker & Docker Compose
- **Servidor Web/Proxy**: Nginx
- **Estilos**: HTML5, CSS3, JavaScript (integración con gráficos)

## 📦 Instalación y Configuración

### 1. Requisitos Previos
- Python 3.11.9
- Docker y Docker Compose (recomendado)
- MySQL (si se ejecuta localmente sin Docker)

### 2. Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto (usar como guía `settings.py`):
```env
DJANGO_SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOST=localhost
DB_NAME=biblioteca_db
DB_USER=root
DB_PASSWORD=root_password
DB_HOST=db
DB_PORT=3306
```

### 3. Ejecución con Docker (Recomendado)
```bash
# Construir e iniciar contenedores
docker-compose up --build -d

# Poblar la base de datos con datos de prueba
docker cp populate.py biblioteca_web:/app/populate_manual.py
docker-compose exec web python /app/populate_manual.py
```

### 4. Ejecución Local (Opcional)
```bash
# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Ejecutar servidor de desarrollo
python manage.py runserver
```

## 🛣️ Rutas y Endpoints

- **Web App**: `http://localhost:8000/`
- **Catálogo**: `http://localhost:8000/catalogo/`
- **Estadísticas**: `http://localhost:8000/estadisticas/`
- **API REST**: `http://localhost:8000/api/` (Soporta GET, POST, PUT, DELETE)
- **Servicio SOAP**: `http://localhost:8000/soap/`
- **Admin**: `http://localhost:8000/admin/`

## 📝 Notas de Versión (Observaciones)
- Se debe asegurar el uso de Python 3.11.9 para evitar conflictos de librerías.
- La configuración de seguridad utiliza `django-environ`.
- El servicio SOAP está optimizado para su visualización y consumo mediante scripts cliente incluidos (`cliente_soap_visual.py`).

---
**Desarrollado por:** Amador Ayala Angel
**Proyecto:** Unidad 3 - Servicios Web
