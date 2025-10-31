# Importamos el modulo para hacer las peticiones.
import requests
# El modulo para trabajar con los archivos CSV.
import csv
# El modulo para interactuar con el sistema operativo.
import os
# Y el modulo para trabajar con fechas y horas.
from datetime import datetime
# Tipado
from typing import Dict, Any, Optional, List

# --- 1. CONSTANTES GLOBALES ---

# URL base para la API de tasas de cambio, Frankfurter tiene un endpoint específico para listar todas las monedas.
API_URL = "https://api.frankfurter.app/latest"
API_URL_MONEDAS = "https://api.frankfurter.app/currencies"

# Nombre del archivo, usaremos la ruta absoluta para guardarlo en la misma carpeta del script.
NOMBRE_CSV = "historico.csv"

# Construye la RUTA ABSOLUTA al archivo CSV para que se guarde junto al script.
CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), NOMBRE_CSV)

# Define el encabezado (la primera fila) del archivo CSV.
CAMPOS_CSV: List[str] = ["Fecha_Hora",
                         "Cantidad", "Origen", "Destino", "Resultado"]


# Obtiene la tasa de cambio actual desde la API, moneda_base (ej. "EUR"), moneda_objetivo (ej. "USD"), Returns: La tasa de cambio (float) o None si hay un error.
def obtener_tasa(moneda_base: str, moneda_objetivo: str) -> Optional[float]:

    # La API de Frankfurter requiere 'base' y 'to' (en lugar de 'symbols') como parámetros GET.
    parametros: Dict[str, str] = {
        "from": moneda_base, "to": moneda_objetivo}

    try:
        # Petición GET al servidor de la API, usando 'params' para adjuntar las monedas a la URL, y ponemos un limite de tiempo de 10 segundos.
        respuesta = requests.get(API_URL, params=parametros, timeout=10)

        # Si la respuesta HTTP no es 200 (éxito), levanta una excepción (ej: 404, 403).
        respuesta.raise_for_status()

        # Deserializa la cadena JSON (texto) de la respuesta y la convierte en un diccionario de Python.
        datos: Dict[str, Any] = respuesta.json()

        # Acceso anidado a la estructura de datos (rates).
        tasa: float = datos['rates'][moneda_objetivo]

        return tasa

    except requests.exceptions.Timeout:
        print("❌ Error: Tiempo de espera agotado al conectar con la API.")
        return None
    except requests.exceptions.RequestException as e:
        # Captura errores de red (no hay internet) o errores HTTP del servidor.
        print(f"❌ Error al conectar con la API o respuesta inválida: {e}")
        return None
    except KeyError:
        # Captura errores si los códigos de divisa no son válidos o el JSON es incorrecto.
        print(
            "❌ Error: No se pudo encontrar la tasa, ¿Son correctos los códigos de divisa?")
        return None


# Obtiene y muestra la lista de divisas soportadas por la API.
def mostrar_divisas_soportadas():
    print("\n--- 🌐 DIVISAS SOPORTADAS ---")
    try:
        # Endpoint específico de Frankfurter para obtener la lista de monedas.
        respuesta = requests.get(API_URL_MONEDAS, timeout=10)
        respuesta.raise_for_status()

        # El resultado es un diccionario de {'CODIGO': 'Nombre de la Moneda'}
        monedas: Dict[str, str] = respuesta.json()

        if not monedas:
            print("❌ No se pudieron obtener los códigos de divisa.")
            return

        # Imprimimos las monedas en dos columnas
        items = list(monedas.items())
        # Calcula la mitad de la lista para dividirla en dos columnas
        mitad = (len(items) + 1) // 2

        print(f"Total de divisas: {len(items)}\n")

        for i in range(mitad):
            codigo1, nombre1 = items[i]
            linea = f"{codigo1:<5}: {nombre1:<35}"

            # Si hay un segundo elemento para la fila
            if i + mitad < len(items):
                codigo2, nombre2 = items[i + mitad]
                linea += f"{codigo2:<5}: {nombre2}"

            print(linea)

    except requests.exceptions.Timeout:
        print("❌ Error: Tiempo de espera agotado al obtener la lista de divisas.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con la API para obtener divisas: {e}")
    except Exception as e:
        print(f"❌ Error inesperado al procesar la lista de divisas: {e}")


# Verifica si el archivo CSV existe y, si no, lo crea con el encabezado e implementa manejo de errores robusto para I/O.
def inicializar_historico():

    # Comprueba si el archivo histórico NO existe en la RUTA ABSOLUTA.
    if not os.path.exists(CSV):
        # Usamos NOMBRE_CSV en la impresión, pero CSV para la ruta.
        print(f"Creando archivo {NOMBRE_CSV} e insertando encabezado...")

        try:
            # Abre el archivo en modo escritura ('w') usando la RUTA ABSOLUTA (CSV).
            with open(CSV, mode='w', newline='', encoding='utf-8') as archivo_csv:
                # Crea un objeto para escribir datos en formato CSV.
                escritor = csv.writer(archivo_csv)
                # Escribe la lista CAMPOS_CSV como la primera fila (el encabezado).
                escritor.writerow(CAMPOS_CSV)
            print("✅ Histórico inicializado.")
        except IOError as e:
            print(
                f"❌ ERROR CRÍTICO al inicializar el archivo {NOMBRE_CSV}. Posiblemente por permisos: {e}")
            exit()
        except Exception as e:
            print(f"❌ ERROR INESPERADO al inicializar el archivo: {e}")
            exit()


# Guarda el registro de la conversión en el archivo CSV.
def guardar_historico(cantidad: float, moneda_origen: str, moneda_destino: str, resultado: float):

    # Se asegura de que el archivo exista antes de intentar añadir datos.
    inicializar_historico()

    # Obtiene el momento actual y lo formatea en un string legible.
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Combina todos los datos en una lista que representa una fila del CSV, usamos f-string para formatear los números a dos decimales antes de guardar (limpieza).
    fila_datos = [
        fecha_hora_actual,
        f"{cantidad:.2f}",
        moneda_origen,
        moneda_destino,
        f"{resultado:.2f}"
    ]

    try:
        # Abre el archivo en modo añadir ('a') usando la RUTA ABSOLUTA (CSV).
        with open(CSV, mode='a', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.writer(archivo_csv)
            # Escribe la lista de datos como una nueva fila en el CSV.
            escritor.writerow(fila_datos)
            print("💾 Conversión registrada en el histórico.")
    except Exception as e:
        print(f"❌ Error al escribir en el histórico CSV: {e}")


# Lee y muestra todas las conversiones guardadas en el archivo CSV.
def mostrar_historico():

    if not os.path.exists(CSV):
        print("\nℹ️ El histórico aún está vacío, ¡Empieza a convertir divisas!")
        return

    print("\n--- 📜 HISTÓRICO DE CONVERSIONES ---")

    try:
        # Abre el archivo en modo lectura ('r') usando la RUTA ABSOLUTA (CSV).
        with open(CSV, mode='r', newline='', encoding='utf-8') as archivo_csv:
            lector = csv.reader(archivo_csv)

            # Saltamos el encabezado para no mostrarlo.
            try:
                next(lector)
            except StopIteration:
                print("\nℹ️ El histórico está vacío.")
                return

            # Imprime el encabezado de la tabla para mejor visualización
            print(
                f"{'Fecha_Hora':<20} | {'Cantidad':<10} | {'Origen':<6} | {'Destino':<7} | {'Resultado':<10}")
            print("-" * 55)

            for fila in lector:
                # Desempaquetamos la fila para imprimir con formato
                fecha_hora, cantidad, origen, destino, resultado = fila
                print(
                    f"{fecha_hora:<20} | {cantidad:<10} | {origen:<6} | {destino:<7} | {resultado:<10}")

    except Exception as e:
        print(f"❌ Error al leer o procesar el archivo histórico: {e}")


# Función para gestionar la entrada de datos, obtener la tasa y mostrar el resultado.
def convertir_divisas():
    print("\n--- CONVERSOR DE DIVISAS ---")

    # 1. Entrada de la cantidad
    try:
        cantidad = float(input("Cantidad a convertir: "))
        if cantidad <= 0:
            print("❌ La cantidad debe ser un número positivo.")
            return
    except ValueError:
        print("❌ Error: La cantidad debe ser un número válido.")
        return

    # 2. Entrada de divisas y normalización a mayúsculas
    moneda_origen = input("Divisa de origen (ej. EUR): ").strip().upper()
    moneda_destino = input("Divisa de destino (ej. USD): ").strip().upper()

    # VALIDACIÓN DE ROBUSTEZ: Verifica que los códigos sean de 3 letras.
    if not moneda_origen or not moneda_destino or len(moneda_origen) != 3 or len(moneda_destino) != 3:
        print("❌ Debe ingresar códigos de divisa válidos de 3 letras (ej. EUR).")
        return

    # 3. Obtener la tasa de cambio
    tasa = obtener_tasa(moneda_origen, moneda_destino)

    if tasa is not None:
        # 4. Cálculo y presentación del resultado
        resultado = cantidad * tasa

        # Llama a la función para guardar el registro.
        guardar_historico(cantidad, moneda_origen, moneda_destino, resultado)

        # Muestra el resultado final, formateando a dos decimales (:.2f) para el estándar monetario.
        print(
            f"\nResultado: {cantidad:.2f} {moneda_origen} equivale a {resultado:.2f} {moneda_destino}")


# Función principal que gestiona el menú y la interacción con el usuario.
def main():

    # Se ejecuta una única vez para garantizar que el archivo CSV exista antes de empezar.
    inicializar_historico()

    # Bucle infinito para que la aplicación no se cierre tras una única acción.
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Convertir divisas")
        print("2. Ver histórico 📜")
        print("3. Ver divisas soportadas 🌐")  # Nueva opción
        print("4. Salir")                     # La opción Salir es ahora la 4

        opcion = input("\nElige una opción (1, 2, 3 o 4): ")

        if opcion == '4':
            # El 'break' sale del bucle 'while True' y termina la ejecución del programa.
            print("👋 ¡Hasta pronto!")
            break
        elif opcion == '1':
            convertir_divisas()
        elif opcion == '2':
            mostrar_historico()
        elif opcion == '3':
            # Llamamos a la nueva función
            mostrar_divisas_soportadas()
        else:
            print("❌ Opción no válida, por favor, elige 1, 2, 3 o 4.")


if __name__ == "__main__":
    main()
