import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_project.settings')
django.setup()

from libros.models import Autor, Categoria, Editorial, Libro, Prestamo
from django.contrib.auth.models import User

print("🗑️  Limpiando base de datos...")
Prestamo.objects.all().delete()
Libro.objects.all().delete()
Autor.objects.all().delete()
Categoria.objects.all().delete()
Editorial.objects.all().delete()

print("📚 Creando categorías...")
categorias = [
    Categoria.objects.create(nombre="Ficción", descripcion="Novelas y cuentos de ficción"),
    Categoria.objects.create(nombre="Ciencia Ficción", descripcion="Literatura de ciencia ficción"),
    Categoria.objects.create(nombre="Historia", descripcion="Libros de historia"),
    Categoria.objects.create(nombre="Biografía", descripcion="Biografías y autobiografías"),
    Categoria.objects.create(nombre="Tecnología", descripcion="Libros sobre tecnología"),
]

print("✍️  Creando autores...")
autores = [
    Autor.objects.create(nombre="Gabriel", apellido="García Márquez", nacionalidad="Colombiano", fecha_nacimiento=date(1927, 3, 6)),
    Autor.objects.create(nombre="Isabel", apellido="Allende", nacionalidad="Chilena", fecha_nacimiento=date(1942, 8, 2)),
    Autor.objects.create(nombre="Jorge", apellido="Luis Borges", nacionalidad="Argentino", fecha_nacimiento=date(1899, 8, 24)),
    Autor.objects.create(nombre="Julio", apellido="Cortázar", nacionalidad="Argentino", fecha_nacimiento=date(1914, 8, 26)),
    Autor.objects.create(nombre="Mario", apellido="Vargas Llosa", nacionalidad="Peruano", fecha_nacimiento=date(1936, 3, 28)),
]

print("🏢 Creando editoriales...")
editoriales = [
    Editorial.objects.create(nombre="Penguin Random House", pais="Estados Unidos"),
    Editorial.objects.create(nombre="Planeta", pais="España"),
    Editorial.objects.create(nombre="Alfaguara", pais="España"),
    Editorial.objects.create(nombre="Anagrama", pais="España"),
]

print("📖 Creando libros...")
libros_data = [
    {"titulo": "Cien años de soledad", "autor": 0, "categoria": 0, "editorial": 0, "isbn": "9780307474728", "paginas": 432},
    {"titulo": "El amor en los tiempos del cólera", "autor": 0, "categoria": 0, "editorial": 0, "isbn": "9780307387738", "paginas": 368},
    {"titulo": "La casa de los espíritus", "autor": 1, "categoria": 0, "editorial": 1, "isbn": "9788497592208", "paginas": 448},
    {"titulo": "El Aleph", "autor": 2, "categoria": 0, "editorial": 2, "isbn": "9788420633114", "paginas": 176},
    {"titulo": "Rayuela", "autor": 3, "categoria": 0, "editorial": 2, "isbn": "9788437604572", "paginas": 736},
    {"titulo": "La ciudad y los perros", "autor": 4, "categoria": 0, "editorial": 2, "isbn": "9788420482729", "paginas": 408},
]

for libro_data in libros_data:
    Libro.objects.create(
        titulo=libro_data["titulo"],
        isbn=libro_data["isbn"],
        autor=autores[libro_data["autor"]],
        categoria=categorias[libro_data["categoria"]],
        editorial=editoriales[libro_data["editorial"]],
        fecha_publicacion=date(2000, 1, 1),
        numero_paginas=libro_data["paginas"],
        stock_total=5,
        stock_disponible=5,
        estado='disponible'
    )

print("👤 Creando usuario de prueba...")
user, created = User.objects.get_or_create(
    username='usuario',
    defaults={'email': 'usuario@biblioteca.com'}
)
if created:
    user.set_password('usuario123')
    user.save()

print("\n✅ ¡Base de datos poblada exitosamente!")
print(f"   📚 Libros: {Libro.objects.count()}")
print(f"   ✍️  Autores: {Autor.objects.count()}")
print(f"   📑 Categorías: {Categoria.objects.count()}")
print(f"   🏢 Editoriales: {Editorial.objects.count()}")
print("\n🔐 Credenciales:")
print("   Admin: admin / admin123")
print("   Usuario: usuario / usuario123")