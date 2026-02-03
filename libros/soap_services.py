from spyne import Application, rpc, ServiceBase, Unicode, Integer
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from .models import Libro, Autor

class BibliotecaService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def buscar_libro(ctx, titulo):
        """Buscar libro por título"""
        try:
            libro = Libro.objects.get(titulo__icontains=titulo)
            return f"Libro: {libro.titulo}, Autor: {libro.autor.nombre_completo}, ISBN: {libro.isbn}"
        except Libro.DoesNotExist:
            return "Libro no encontrado"
    
    @rpc(_returns=Unicode)
    def listar_libros(ctx):
        """Listar todos los libros"""
        libros = Libro.objects.all()[:10]
        resultado = "Libros disponibles:\n"
        for libro in libros:
            resultado += f"- {libro.titulo} ({libro.autor.nombre_completo})\n"
        return resultado

application = Application(
    [BibliotecaService],
    tns='biblioteca.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

django_soap_application = DjangoApplication(application)