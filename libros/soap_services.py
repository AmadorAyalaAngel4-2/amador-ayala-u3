from django.views.decorators.csrf import csrf_exempt
from spyne import Application, rpc, ServiceBase, Integer, Unicode, String, Boolean, Array
from spyne.model.complex import ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from .models import Libro
from django.http import HttpResponse

# --- 1. MODELOS SOAP ---

class SoapAutor(ComplexModel):
    nombre = String
    apellido = String

class SoapLibro(ComplexModel):
    id = Integer
    titulo = String
    autor_nombre = String
    autor = SoapAutor
    stock_disponible = Integer
    numero_paginas = Integer
    idioma = String

class SoapResponse(ComplexModel):
    exito = Boolean
    mensaje = String
    id = Integer(min_occurs=0, nillable=True)

# --- 2. SERVICIO ---

class BibliotecaService(ServiceBase):
    
    @rpc(_returns=Array(SoapLibro))
    def listar_libros(ctx):
        libros = Libro.objects.all().select_related('autor')
        resultado = []
        for libro in libros:
            s_libro = SoapLibro()
            s_libro.id = libro.id
            s_libro.titulo = libro.titulo
            s_libro.stock_disponible = getattr(libro, 'stock', 1)
            
            # Nombre del autor (manejo de errores)
            try:
                if hasattr(libro.autor, 'nombre_completo'):
                    s_libro.autor_nombre = libro.autor.nombre_completo
                else:
                    s_libro.autor_nombre = f"{libro.autor.nombre} {libro.autor.apellido}"
            except:
                s_libro.autor_nombre = "Autor Desconocido"

            # Objeto autor anidado
            s_autor = SoapAutor()
            try:
                s_autor.nombre = libro.autor.nombre
                s_autor.apellido = libro.autor.apellido
            except:
                s_autor.nombre = "Desconocido"
                s_autor.apellido = ""
            
            s_libro.autor = s_autor
            resultado.append(s_libro)
        return resultado

    @rpc(Integer, _returns=SoapLibro)
    def obtener_libro(ctx, pk):
        try:
            libro = Libro.objects.get(pk=pk)
            s_libro = SoapLibro()
            s_libro.id = libro.id
            s_libro.titulo = libro.titulo
            s_libro.stock_disponible = getattr(libro, 'stock', 1)
            s_libro.numero_paginas = getattr(libro, 'paginas', 0)
            s_libro.idioma = getattr(libro, 'idioma', 'Español')
            
            # Manejo de nombre simple
            try:
                s_libro.autor_nombre = f"{libro.autor.nombre} {libro.autor.apellido}"
            except:
                s_libro.autor_nombre = "Desconocido"

            s_autor = SoapAutor()
            try:
                s_autor.nombre = libro.autor.nombre
                s_autor.apellido = libro.autor.apellido
            except:
                s_autor.nombre = "Desconocido"
            
            s_libro.autor = s_autor
            return s_libro
        except Libro.DoesNotExist:
            return None

    @rpc(Integer, Integer, Integer, _returns=SoapResponse)
    def crear_prestamo(ctx, libro_id, usuario_id, dias):
        # Lógica simulada para evitar errores si no existen los modelos
        resp = SoapResponse()
        resp.exito = True
        resp.mensaje = f"Préstamo registrado (Simulado): Libro {libro_id} a Usuario {usuario_id}"
        resp.id = 999
        return resp

# --- 3. CONFIGURACIÓN Y VISTA SEGURA ---

application = Application(
    [BibliotecaService],
    tns='biblioteca.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# Instancia pura de Spyne
_django_app = DjangoApplication(application)

@csrf_exempt
def soap_view(request):
    """
    Vista puente que desactiva CSRF y pasa la petición a Spyne.
    """
    return _django_app(request)