# Módulo esencial para interactuar con el sistema operativo (archivos, directorios).
import os
# Módulo de utilidades de shell, necesario para mover archivos.
import shutil
# Para tipado.
from typing import Dict, List, Tuple, Any


# --- CONSTANTES GLOBALES ---

# Diccionario que mapea extensiones (claves en minúsculas) a los nombres de las carpetas de destino, se puede modificar o expandir fácilmente.
TIPOS_ARCHIVOS: Dict[str, str] = {

    # IMÁGENES
    "jpg": "Imágenes", "jpeg": "Imágenes", "png": "Imágenes", "gif": "Imágenes",
    "webp": "Imágenes", "svg": "Imágenes", "ico": "Imágenes",

    # DOCUMENTOS
    "pdf": "Documentos", "docx": "Documentos", "doc": "Documentos", "txt": "Documentos",
    "xlsx": "Documentos", "xls": "Documentos", "pptx": "Documentos", "ppt": "Documentos",

    # CÓDIGO Y DESARROLLO
    "py": "Código", "js": "Código", "html": "Código", "css": "Código",
    "json": "Código", "md": "Documentos",  # Markdown como Documento

    # MÚSICA Y VÍDEOS
    "mp3": "Música", "wav": "Música", "flac": "Música",
    "mp4": "Vídeos", "mov": "Vídeos", "avi": "Vídeos", "mkv": "Vídeos",

    # COMPRIMIDOS
    "zip": "Comprimidos", "rar": "Comprimidos", "7z": "Comprimidos",
    "tar": "Comprimidos", "gz": "Comprimidos",
}

# Nombre de la carpeta por defecto si la extensión no está en el diccionario.
OTRAS_CARPETAS: str = "Otros"


# Clasifica los archivos por extensión, crea las carpetas y mueve los archivos, retorna un diccionario con estadísticas de la operación.
def clasificar_y_mover_archivos(directorio: str, archivos_mover: List[str]) -> Dict[str, Any]:

    # Inicializar estadísticas
    estadisticas: Dict[str, Any] = {
        "movidos": 0,
        "ignorados": 0,
        "errores": 0,
        "carpetas_creadas": set()
    }

    print(f"\n🚀 Iniciando clasificación de {len(archivos_mover)} archivos...")

    # Itera sobre la lista de nombres de archivo que deben ser movidos.
    for archivo in archivos_mover:

        # 1. Extracción de la extensión y normalización
        _, extension = os.path.splitext(archivo)
        extension_limpia = extension[1:].lower()

        # 2. Determinar la carpeta de destino
        nombre_carpeta = TIPOS_ARCHIVOS.get(extension_limpia, OTRAS_CARPETAS)

        # 3. Construir rutas de Origen y Destino
        ruta_origen = os.path.join(directorio, archivo)
        ruta_destino = os.path.join(directorio, nombre_carpeta)
        ruta_destino_final = os.path.join(ruta_destino, archivo)

        # 4. Asegurar la existencia de la carpeta de destino.
        try:
            # Crea la carpeta, exist_ok=True evita el error si la carpeta ya existe.
            if not os.path.exists(ruta_destino):
                os.makedirs(ruta_destino)
                estadisticas["carpetas_creadas"].add(nombre_carpeta)
                print(f"   -> Carpeta '{nombre_carpeta}' creada.")

        # Manejo de errores si, por ejemplo, los permisos fallan.
        except Exception as e:
            print(
                f"❌ Error al crear la carpeta '{nombre_carpeta}': {e}, saltando archivo.")
            estadisticas["errores"] += 1
            continue

        # 5. Mover el archivo
        try:
            # shutil.move(origen, destino) mueve el archivo.
            shutil.move(ruta_origen, ruta_destino_final)
            estadisticas["movidos"] += 1
            print(f"   ✅ Movido: '{archivo}' -> '{nombre_carpeta}'")

        # Maneja el caso común de que el archivo ya exista en el destino (shutil.Error).
        except shutil.Error as e:
            # Podría ser un error de "mismo archivo", lo ignoramos y contamos como ignorado.
            print(
                f"   ⚠️ Archivo ya existe o no se pudo mover: '{archivo}'. Ignorado.")
            estadisticas["ignorados"] += 1
        except Exception as e:
            print(f"   ❌ Error desconocido al mover '{archivo}': {e}")
            estadisticas["errores"] += 1

    return estadisticas


# Función principal que escanea el directorio y prepara la lista de archivos.
def organizar_archivos(directorio: str):

    # Convierte la ruta a un formato absoluto para evitar ambigüedades.
    directorio = os.path.abspath(directorio)

    print(f"\n--- 🗂️ ORGANIZADOR DE ARCHIVOS ---")
    print(f"📁 Escaneando directorio: {directorio}")

    try:
        # Obtiene una lista de todos los elementos (archivos y carpetas) del directorio.
        elementos: List[str] = os.listdir(directorio)
    except FileNotFoundError:
        print(
            f"❌ Error: El directorio '{directorio}' no existe, por favor, revísalo.")
        return
    except Exception as e:
        print(f"❌ Error al acceder al directorio: {e}")
        return

    archivos_mover: List[str] = []

    for elemento in elementos:

        # Filtro adicional: Ignorar archivos ocultos (los que empiezan con '.')
        if elemento.startswith('.'):
            continue

        # Genera la ruta completa para verificar si es un archivo.
        ruta_completa = os.path.join(directorio, elemento)

        # Filtra: solo queremos los que son archivos (no carpetas).
        if os.path.isfile(ruta_completa):
            # Filtro adicional: Ignorar el script de Python si está en la carpeta
            if elemento != os.path.basename(__file__):
                archivos_mover.append(elemento)

    if not archivos_mover:
        print("ℹ️ No se encontraron archivos para mover en este directorio.")
        return

    # Llama a la función que ejecuta la clasificación y el movimiento con los archivos filtrados.
    stats = clasificar_y_mover_archivos(directorio, archivos_mover)

    # --- Reporte Final ---
    print("\n------------------------------")
    print("🎉 ¡Organización completada! 🎉")
    print("------------------------------")
    print(f"Total de archivos procesados: {len(archivos_mover)}")
    print(f"Archivos movidos con éxito: {stats['movidos']}")
    print(f"Archivos ignorados (ya existían): {stats['ignorados']}")
    print(f"Errores encontrados (permisos, etc.): {stats['errores']}")
    if stats["carpetas_creadas"]:
        print("Nuevas carpetas creadas:")
        for carpeta in sorted(list(stats["carpetas_creadas"])):
            print(f"  - {carpeta}")
    print("------------------------------")


def main():
    # Obtener el directorio absoluto del script. Esto es crucial para que la opción 1 funcione correctamente, independientemente de cómo se ejecute el script.
    directorio_script = os.path.dirname(os.path.abspath(__file__))

    # Menú interactivo para el usuario.
    while True:
        print("\n--- MENÚ ORGANIZADOR ---")
        print("1. Organizar la carpeta actual (donde está este script)")
        print("2. Organizar una carpeta específica (ej. C:\\Users\\...\\Downloads)")
        print("3. Configurar extensiones (Mostrar / Añadir)")
        print("4. Salir")

        opcion = input("\nElige una opción (1, 2, 3 o 4): ")

        if opcion == '4':
            print("👋 ¡Hasta pronto!")
            # Sale del bucle y termina la aplicación.
            break
        elif opcion == '1':
            # Ahora pasamos el directorio ABSOLUTO del script, que es infalible.
            organizar_archivos(directorio_script)
        elif opcion == '2':
            ruta = input(
                "Ingresa la RUTA ABSOLUTA de la carpeta a organizar: ")
            organizar_archivos(ruta)
        elif opcion == '3':
            configurar_extensiones()
        else:
            print("❌ Opción no válida.")

# Función para añadir o ver las configuraciones de extensiones.


def configurar_extensiones():
    while True:
        print("\n--- CONFIGURACIÓN DE EXTENSIONES ---")
        print("1. Mostrar lista de extensiones actuales")
        print("2. Añadir nueva extensión y carpeta")
        print("3. Volver al menú principal")

        opcion_config = input("\nElige una opción (1, 2 o 3): ")

        if opcion_config == '3':
            break

        elif opcion_config == '1':
            print("\n--- LISTA DE CLASIFICACIÓN ---")
            # Ordenamos para mostrar de forma limpia
            carpetas_y_extensiones: Dict[str, List[str]] = {}
            for ext, carpeta in TIPOS_ARCHIVOS.items():
                if carpeta not in carpetas_y_extensiones:
                    carpetas_y_extensiones[carpeta] = []
                carpetas_y_extensiones[carpeta].append(ext)

            for carpeta in sorted(carpetas_y_extensiones.keys()):
                extensiones = ", ".join(
                    sorted(carpetas_y_extensiones[carpeta]))
                print(f"[{carpeta}]: {extensiones}")
            print(f"\nExtensiones sin clasificar van a: [{OTRAS_CARPETAS}]")

        elif opcion_config == '2':
            print("\n--- AÑADIR NUEVA CLASIFICACIÓN ---")
            ext = input(
                "Ingresa la extensión (sin punto, ej. 'iso'): ").strip().lower()
            carpeta = input(
                "Ingresa el nombre de la carpeta de destino (ej. 'Instaladores'): ").strip()

            if not ext or not carpeta:
                print("❌ Extensión o nombre de carpeta no pueden estar vacíos.")
                continue

            # Verificamos si ya existe.
            if ext in TIPOS_ARCHIVOS:
                print(
                    f"⚠️ La extensión '.{ext}' ya está mapeada a la carpeta '{TIPOS_ARCHIVOS[ext]}'.")
                confirma = input(
                    "¿Deseas sobreescribirla? (s/n): ").strip().lower()
                if confirma != 's':
                    continue

            # Nota: Esto solo afecta a la ejecución actual, no se persiste en disco, pero cumple la función de demostración.
            TIPOS_ARCHIVOS[ext] = carpeta
            print(
                f"✅ Extensión '.{ext}' añadida/actualizada a la carpeta '{carpeta}'.")

        else:
            print("❌ Opción no válida.")


# Punto de entrada del programa.
if __name__ == "__main__":
    main()
