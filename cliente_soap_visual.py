#!/usr/bin/env python3
"""
Cliente SOAP Visual - Sistema de Biblioteca
Ejecuta operaciones y muestra XML en navegador
"""

from zeep import Client, Settings
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
import sys
import webbrowser
import os
import tempfile
from datetime import datetime
from lxml import etree

WSDL_URL = 'http://127.0.0.1:8000/soap/?wsdl'

# Plugin para capturar mensajes SOAP
history = HistoryPlugin()

def crear_cliente():
    """Crea cliente SOAP con configuración optimizada"""
    try:
        settings = Settings(strict=False, xml_huge_tree=True, xsd_ignore_sequence_order=True)
        client = Client(WSDL_URL, settings=settings, plugins=[history])
        return client
    except Exception as e:
        print(f"❌ Error al conectar con el servidor SOAP: {e}")
        print("\n💡 Asegúrate de que el servidor Django esté corriendo:")
        print("   python manage.py runserver")
        sys.exit(1)

def formatear_xml(xml_string):
    """Formatea XML para mejor visualización"""
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(xml_string, parser)
        return etree.tostring(root, pretty_print=True, encoding='unicode')
    except:
        return xml_string

def mostrar_xml_en_navegador(request_xml, response_xml, operacion):
    """Genera HTML con XML SOAP y lo abre en navegador"""
    import html
    
    request_formatted = formatear_xml(request_xml)
    response_formatted = formatear_xml(response_xml)
    
    request_escaped = html.escape(request_formatted)
    response_escaped = html.escape(response_formatted)
    
    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>🔍 XML SOAP - {operacion}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }}
        .container {{ max-width: 1600px; margin: 0 auto; background: white; border-radius: 15px; overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 40px; text-align: center; }}
        .section-title {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 25px; border-radius: 10px; }}
        .xml-container {{ background: #1e1e1e; border-radius: 10px; padding: 25px; overflow: auto; max-height: 600px; }}
        pre {{ margin: 0; color: #d4d4d4; font-family: 'Consolas', 'Monaco', monospace; white-space: pre-wrap; }}
        .copy-btn {{ background: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Visualizador de XML SOAP</h1>
            <div>Operación: {operacion}</div>
            <div>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        <div style="padding: 40px;">
            <div style="margin-bottom: 40px;">
                <div class="section-title">📤 SOAP Request</div>
                <div class="xml-container">
                    <pre id="request-xml">{request_escaped}</pre>
                </div>
                <button class="copy-btn" onclick="copyToClipboard('request-xml')">📋 Copiar Request</button>
            </div>
            <div>
                <div class="section-title">📥 SOAP Response</div>
                <div class="xml-container">
                    <pre id="response-xml">{response_escaped}</pre>
                </div>
                <button class="copy-btn" onclick="copyToClipboard('response-xml')">📋 Copiar Response</button>
            </div>
        </div>
    </div>
    <script>
        function copyToClipboard(elementId) {{
            const text = document.getElementById(elementId).textContent;
            navigator.clipboard.writeText(text).then(() => {{
                const btn = event.target;
                btn.textContent = '✅ Copiado!';
                setTimeout(() => btn.textContent = btn.textContent.includes('Request') ? '📋 Copiar Request' : '📋 Copiar Response', 2000);
            }});
        }}
    </script>
</body>
</html>
"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as f:
        f.write(html_content)
        temp_file = f.name
    
    print(f"\n🌐 Abriendo visualizador XML en el navegador...")
    webbrowser.open('file://' + os.path.abspath(temp_file))

def preguntar_ver_xml():
    """Pregunta si desea ver el XML"""
    print("\n" + "="*80)
    respuesta = input("¿Desea ver el XML SOAP en el navegador? (s/n): ").strip().lower()
    return respuesta in ['s', 'si', 'sí', 'y', 'yes']

def listar_libros(client):
    """Lista todos los libros"""
    print("\n" + "="*80)
    print("📚 LISTANDO TODOS LOS LIBROS")
    print("="*80)
    
    try:
        result = client.service.listar_libros()
        
        if not result:
            print("\n⚠️  No hay libros registrados")
            return
        
        print(f"\n✅ Se encontraron {len(result)} libros:\n")
        
        for i, libro in enumerate(result, 1):
            print(f"{i}. 📖 {libro.titulo} (ID: {libro.id})")
            print(f"   ✍️  Autor: {libro.autor_nombre}")
            print(f"   📦 Disponibles: {libro.stock_disponible}")
        
        if preguntar_ver_xml():
            request_xml = etree.tostring(history.last_sent['envelope'], encoding='unicode', pretty_print=True)
            response_xml = etree.tostring(history.last_received['envelope'], encoding='unicode', pretty_print=True)
            mostrar_xml_en_navegador(request_xml, response_xml, "listar_libros")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

def obtener_libro(client):
    """Obtiene detalles de un libro por ID"""
    print("\n" + "="*80)
    print("🔍 OBTENER LIBRO POR ID")
    print("="*80)
    
    try:
        libro_id = int(input("\nIngrese el ID del libro: "))
        result = client.service.obtener_libro(libro_id)
        
        if not result:
            print(f"\n⚠️  No se encontró libro con ID {libro_id}")
            return
        
        print(f"\n✅ Libro encontrado:")
        print(f"📖 {result.titulo}")
        print(f"✍️  Autor: {result.autor.nombre} {result.autor.apellido}")
        print(f"📄 Páginas: {result.numero_paginas} | Idioma: {result.idioma}")
        print(f"📦 Stock: {result.stock_disponible}")
        
        if preguntar_ver_xml():
            request_xml = etree.tostring(history.last_sent['envelope'], encoding='unicode', pretty_print=True)
            response_xml = etree.tostring(history.last_received['envelope'], encoding='unicode', pretty_print=True)
            mostrar_xml_en_navegador(request_xml, response_xml, f"obtener_libro (ID: {libro_id})")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

def crear_prestamo(client):
    """Crea un nuevo préstamo"""
    print("\n" + "="*80)
    print("➕ CREAR NUEVO PRÉSTAMO")
    print("="*80)
    
    try:
        libro_id = int(input("\nID del libro: "))
        usuario_id = int(input("ID del usuario: "))
        dias = int(input("Días de préstamo: "))
        
        result = client.service.crear_prestamo(libro_id, usuario_id, dias)
        
        if result.exito:
            print(f"\n✅ {result.mensaje}")
            print(f"   ID del préstamo: {result.id}")
        else:
            print(f"\n❌ {result.mensaje}")
        
        if preguntar_ver_xml():
            request_xml = etree.tostring(history.last_sent['envelope'], encoding='unicode', pretty_print=True)
            response_xml = etree.tostring(history.last_received['envelope'], encoding='unicode', pretty_print=True)
            mostrar_xml_en_navegador(request_xml, response_xml, "crear_prestamo")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*80)
    print("🏛️  SISTEMA DE BIBLIOTECA - CLIENTE SOAP VISUAL")
    print("="*80)
    print("\n📚 OPERACIONES:")
    print("  1. Listar todos los libros")
    print("  2. Obtener libro por ID")
    print("  3. Crear préstamo")
    print("\n  0. Salir")
    print("="*80)

def main():
    """Función principal"""
    print("\n🔌 Conectando al servidor SOAP...")
    client = crear_cliente()
    print("✅ Conexión establecida")
    
    operaciones = {
        '1': listar_libros,
        '2': obtener_libro,
        '3': crear_prestamo,
    }
    
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == '0':
            print("\n👋 ¡Hasta luego!")
            break
        
        if opcion in operaciones:
            operaciones[opcion](client)
        else:
            print("\n❌ Opción inválida")
        
        input("\n⏎ Presione Enter para continuar...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
        sys.exit(0)