# Necesario para hacer peticiones HTTP (descargar la página web), ya no se usa pero lo mantenemos para documentación.
# import requests
# Necesario para parsear el HTML y encontrar elementos específicos (el precio), tampoco lo usamos pero tambien lo mantenemos para documentación.
# from bs4 import BeautifulSoup
# Necesario para interactuar con el sistema de archivos (ej. comprobar si el CSV existe).
import os
# Necesario para leer y escribir en el archivo de historial de forma estructurada.
import csv
# Necesario para obtener la marca de tiempo actual al registrar un precio.
from datetime import datetime
# Necesario para crear gráficos de líneas (la visualización del bonus).
import matplotlib.pyplot as plt


# --- CONSTANTES GLOBALES ---

# Nombre del archivo donde se guardará el historial de precios.
ARCHIVO_PRECIOS = "precios_historico.csv"
# Define el encabezado (la primera fila) del archivo CSV.
CAMPOS_CSV = ["Fecha_Hora", "Producto", "Precio", "URL"]

# Simula la obtención del precio desde una web, en un entorno real, requests y bs4 harían esta función, aquí solicitamos el precio al usuario para mantener el flujo de la app.


def obtener_precio(url_producto, nombre_producto):

    print(f"\n--- SIMULACIÓN DE RASTREO para: {nombre_producto} ---")

    # 1. Solicitamos el precio simulado al usuario
    while True:
        precio_texto = input(
            f"Ingresa el precio actual para '{nombre_producto}' (ej. 15.99): ")

        # 2. Delegamos la limpieza (símbolos, comas) y la conversión a float a la función auxiliar.
        precio_limpio = limpiar_y_convertir(precio_texto)

        if precio_limpio is not None:
            return precio_limpio
        else:
            print(
                "❌ Entrada no válida, por favor, ingresa un número decimal o entero válido.")


# Limpia el texto de un precio (ej. '15,99 €') y lo convierte a float (15.99)
def limpiar_y_convertir(precio_texto):

    try:
        # 1. Encadenamiento de métodos para la limpieza y estandarización del formato.
        precio_limpio = (
            precio_texto
            # Elimina el símbolo de moneda.
            .replace("€", "")
            # Convierte la coma decimal (formato EU) a punto (formato Python/EN).
            .replace(",", ".")
            # Asegura que no queden espacios al inicio/final.
            .strip()
        )

        # 2. Convierte el texto limpio a número flotante.
        return float(precio_limpio)

    except ValueError:
        # Captura el error si el texto limpio no se puede convertir a float, no imprimimos aquí, lo maneja obtener_precio para el loop
        return None

# Inicializa el archivo CSV si no existe, asegurando el encabezado.


def inicializar_historico_precios(script_dir):
    ruta_completa = os.path.join(script_dir, ARCHIVO_PRECIOS)

    # Comprueba si el archivo histórico NO existe usando os.path.exists().
    if not os.path.exists(ruta_completa):
        print(
            f"Creando archivo {ARCHIVO_PRECIOS} e insertando encabezado...")

        # Abre el archivo en modo escritura ('w') para crearlo, 'newline='''' evita filas en blanco.
        with open(ruta_completa, mode='w', newline='', encoding='utf-8') as archivo_csv:

            # Crea un objeto para escribir datos en formato CSV.
            escritor = csv.writer(archivo_csv)

            # Escribe la lista CAMPOS_CSV como la primera fila (el encabezado).
            escritor.writerow(CAMPOS_CSV)

        print("✅ Histórico inicializado.")

    return ruta_completa


# Función para guardar el registro de precios.
def guardar_historico(ruta_completa, Producto, Precio, URL):

    # Obtiene el momento actual y lo formatea en un string legible para el CSV.
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Combina todos los datos en una lista que representa una fila del CSV.
    fila_datos = [fecha_hora, Producto, Precio, URL]

    try:
        # Abre el archivo en modo añadir ('a') para agregar la nueva fila sin borrar las anteriores.
        with open(ruta_completa, mode='a', newline='', encoding='utf-8') as archivo_csv:

            escritor = csv.writer(archivo_csv)

            # Escribe la lista de datos como una nueva fila.
            escritor.writerow(fila_datos)

            print("💾 Precio registrado en el histórico.")

    except Exception as e:
        # Captura cualquier error durante la escritura en el archivo.
        print(f"❌ Error al escribir en el histórico CSV: {e}")


def rastrear_precio(ruta_historico):
    print("\n--- RASTREADOR DE PRECIOS ---")

    # 1. Pedir inputs (URL y Producto).
    url_producto = input("Ingresa la URL del producto (para referencia): ")
    nombre_producto = input(
        "Ingresa el nombre del producto (ej. 'Libro Cocina'): ")

    # 2. Obtener el precio (llama a la función de simulación, que devuelve un float o None/string de error).
    precio_obtenido = obtener_precio(url_producto, nombre_producto)

    # 3. Verificar y guardar, comprobamos que sea un float válido.
    if isinstance(precio_obtenido, float):

        # Guardado exitoso: Llama a la función con los datos.
        guardar_historico(ruta_historico, nombre_producto,
                          precio_obtenido, url_producto)
        print(
            f"✅ Rastreo exitoso: {nombre_producto} | Precio: {precio_obtenido:.2f}")

    else:
        # Muestra un mensaje si el rastreo falló.
        print(f"❌ No se pudo rastrear el precio de {nombre_producto}.")


def grafico_precios(script_dir, ruta_historico):
    """Lee el CSV y genera un gráfico de la evolución de precios."""

    # Listas vacías para almacenar los datos X e Y del gráfico.
    fechas = []
    precios = []

    # Usamos un diccionario para manejar productos múltiples y solo graficar uno
    productos_registrados = {}

    try:
        # Abrir el archivo en modo lectura ('r').
        with open(ruta_historico, mode='r', newline='', encoding='utf-8') as archivo_csv:
            lector = csv.reader(archivo_csv)
            # Ignora el encabezado (la primera fila).
            next(lector)
            for fila in lector:
                # Extrae los datos: fecha (índice 0), nombre (índice 1) y precio (índice 2, convertido a float).
                fecha_str = fila[0]
                nombre = fila[1]
                precio_float = float(fila[2])

                if nombre not in productos_registrados:
                    productos_registrados[nombre] = {
                        'fechas': [], 'precios': []}

                productos_registrados[nombre]['fechas'].append(
                    datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S"))
                productos_registrados[nombre]['precios'].append(precio_float)

    except FileNotFoundError:
        print(
            f"❌ Error: No se encontró el archivo {ARCHIVO_PRECIOS} en la ruta:\n{ruta_historico}\nAsegúrate de haber rastreado algún precio ya.")
        return

    # Comprobación de seguridad: ¿Hay datos para graficar?
    if not productos_registrados:
        print("ℹ️ El archivo histórico está vacío o solo contiene el encabezado, rastrea un precio primero.")
        return

    # --- SELECCIÓN DEL PRODUCTO (Si hay múltiples) ---
    productos = list(productos_registrados.keys())

    if len(productos) > 1:
        print("\n--- PRODUCTOS RASTREADOS ---")
        for i, nombre in enumerate(productos):
            print(f"{i + 1}. {nombre}")

        while True:
            try:
                seleccion = int(
                    input("Elige el número del producto a graficar: ")) - 1
                if 0 <= seleccion < len(productos):
                    producto_seleccionado = productos[seleccion]
                    fechas = productos_registrados[producto_seleccionado]['fechas']
                    precios = productos_registrados[producto_seleccionado]['precios']
                    break
                else:
                    print("Selección no válida.")
            except ValueError:
                print("Por favor, ingresa un número.")
    else:
        # Solo hay un producto, lo seleccionamos automáticamente
        producto_seleccionado = productos[0]
        fechas = productos_registrados[producto_seleccionado]['fechas']
        precios = productos_registrados[producto_seleccionado]['precios']
        print(
            f"\nGenerando gráfico para el único producto rastreado: {producto_seleccionado}")

    # --- CÓDIGO DE MATPLOTLIB ---

    # 1. Configuración de la figura
    plt.figure(figsize=(12, 6))

    # 2. Dibuja la línea: precios (Y) en función de las fechas (X).
    plt.plot(fechas, precios, marker='o', linestyle='-', color='#1f77b4')

    # 3. Etiquetas y títulos
    plt.xlabel("Fecha y Hora", fontsize=12)
    plt.ylabel("Precio (€)", fontsize=12)
    plt.title(
        f"Evolución de Precio de: {producto_seleccionado}", fontsize=14, weight='bold')

    # 4. Configuración adicional
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45, ha='right')

    # 5. Asegura que el espacio se ajuste correctamente
    plt.tight_layout()

    # 6. Guarda el gráfico en la misma carpeta que el script (reemplazando plt.show())
    nombre_archivo_salida = "evolucion_precios.png"
    ruta_salida_completa = os.path.join(script_dir, nombre_archivo_salida)

    try:
        plt.savefig(ruta_salida_completa)
        print(
            f"\n✨ GRÁFICO CREADO: Se ha guardado el gráfico '{nombre_archivo_salida}' en la ruta:\n{ruta_salida_completa}")
        print("\n--- NOTA PARA EL PORTAFOLIO ---")
        print("La visualización con 'plt.show()' no es compatible con el entorno web de Canvas.")
        print("Para ver el gráfico, ejecuta este script de forma local (asegúrate de tener el CSV) y abre el archivo PNG generado.")

    except Exception as e:
        print(f"\n❌ Error al guardar el gráfico: {e}")


def main():
    # ---------------------------------------------------------------
    # Solución al problema de ruta: Construimos la ruta ABSOLUTA del script.
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()

    # Inicializa el archivo CSV al inicio de la aplicación y obtiene su ruta.
    ruta_historico_completa = inicializar_historico_precios(script_dir)
    # ---------------------------------------------------------------

    # Bucle infinito para mantener la aplicación en ejecución.
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Rastrear precio de producto (SIMULACIÓN)")
        print("2. Mostrar gráfico de evolución (BONUS)")
        print("3. Salir")

        opcion = input("\nElige una opción (1, 2 o 3): ")

        if opcion == '3':
            print("👋 ¡Hasta pronto!")
            break  # Sale del bucle y termina la aplicación.
        elif opcion == '1':
            # Llama a la función de rastreo, pasándole la ruta del CSV.
            rastrear_precio(ruta_historico_completa)
        elif opcion == '2':
            # Llama a la función de visualización, pasándole la ruta del CSV y el directorio.
            grafico_precios(script_dir, ruta_historico_completa)
        else:
            print("❌ Opción no válida.")


if __name__ == "__main__":
    # Inicia la ejecución de la aplicación.
    main()
