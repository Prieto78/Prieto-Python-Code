# Necesario para generar el número secreto aleatorio.
import random
# Necesario para leer y escribir el marcador de puntuaciones (persistencia de datos).
import csv
# Necesario para verificar si el archivo del marcador ya existe (inicialización segura).
import os
# Necesario para registrar la fecha y hora de la partida ganada.
from datetime import datetime
# Tipado para mejorar la legibilidad
from typing import Dict, Any, List

# --- CONSTANTES GLOBALES ---

# Nombre del archivo donde se guardarán los resultados de las partidas.
CSV = "puntuaciones.csv"
# Encabezado que se usa para inicializar el archivo CSV.
CAMPOS_CSV = ["Fecha_Hora", "Dificultad", "Intentos"]

# Diccionario de configuración para mapear dificultades a límites, hace el código más limpio y fácil de escalar.
LIMITES_DIFICULTAD: Dict[str, int] = {
    "facil": 50,
    "normal": 100,
    "dificil": 200
}


# Verifica si el archivo CSV existe y, si no, lo crea con el encabezado, añade un manejo de excepciones más robusto para capturar errores de permisos o disco al crear el archivo.
def inicializar_archivo():
    if not os.path.exists(CSV):
        print(f"\nCreando archivo {CSV} e insertando encabezado...")
        try:
            # Abre el archivo en modo 'w' (escritura), newline="" es necesario para CSV.
            with open(CSV, mode='w', newline='', encoding='utf-8') as archivo_csv:
                # Crea un objeto escritor para trabajar con el archivo.
                escritor = csv.writer(archivo_csv)
                # Escribe la primera fila, que es el encabezado.
                escritor.writerow(CAMPOS_CSV)
            print("✅ Archivo inicializado con éxito.")
        except IOError as e:
            # Captura errores específicos de I/O (permisos, bloqueo de disco, etc.)
            print(f"❌ ERROR CRÍTICO al inicializar el archivo {CSV}: {e}")
            # Si falla, salimos para evitar errores posteriores.
            exit()
        except Exception as e:
            # Otros errores inesperados.
            print(f"❌ ERROR INESPERADO al inicializar el archivo {CSV}: {e}")
            exit()


# Guarda los resultados de una partida ganada en el archivo CSV.
def guardar_resultado(dificultad: str, intentos: int):

    # Asegura que el archivo exista y tenga el encabezado antes de intentar escribir.
    inicializar_archivo()

    # Obtiene la fecha y hora actual y le da formato legible.
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Crea una lista con los datos de la partida, en el orden del encabezado.
    fila_datos = [fecha_hora, dificultad, intentos]

    try:
        # Abre el archivo en modo 'a' (append/añadir) para agregar una nueva línea al final.
        with open(CSV, mode='a', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.writer(archivo_csv)
            # Escribe la fila de datos en el archivo.
            escritor.writerow(fila_datos)
            print("Puntuación guardada en el archivo.")
    except IOError as e:
        # Manejo de errores si, por ejemplo, el archivo estuviera bloqueado por otro programa.
        print(f"❌ Error de I/O al escribir en el archivo CSV: {e}")
    except Exception as e:
        print(f"❌ Error inesperado al guardar el resultado: {e}")


# Lee el archivo CSV, ordena las puntuaciones por intentos y muestra el Top 5.
def mostrar_marcador():

    # Si el archivo no existe, no hay nada que mostrar.
    if not os.path.exists(CSV):
        print("\nℹ️ El marcador aún está vacío, ¡Empieza a jugar!")
        return

    puntuaciones: List[List[Any]] = []

    try:
        # Abre el archivo en modo lectura ('r').
        with open(CSV, mode='r', newline='', encoding='utf-8') as archivo_csv:
            lector = csv.reader(archivo_csv)
            # next() se usa para saltar la primera fila (el encabezado).
            try:
                next(lector)
            except StopIteration:
                # Caso especial si el archivo solo tiene el encabezado y está vacío.
                print("\nℹ️ El marcador está vacío.")
                return

            # Itera sobre todas las filas restantes del archivo.
            for fila in lector:
                # Añade cada fila de datos a la lista.
                puntuaciones.append(fila)

        # Si la lista está vacía después de leer
        if not puntuaciones:
            print("\nℹ️ El marcador está vacío.")
            return

        # Ordenar: sorted() devuelve una nueva lista ordenada, usando el índice 2 (Intentos) como número entero.
        puntuaciones_ordenadas = sorted(puntuaciones, key=lambda x: int(x[2]))

        print("\n--- 🏆 MEJORES PUNTUACIONES ---")

        # Recorre las primeras 5 filas ([:5]) de la lista ordenada, enumerate() añade un contador (i) para numerar los puestos.
        for i, (fecha, dificultad, intentos) in enumerate(puntuaciones_ordenadas[:5]):
            # Imprime el resultado. i+1 convierte el índice 0 en el puesto 1, capitalize() pone en mayúscula la primera letra de la dificultad.
            print(
                f"{i + 1}. ({dificultad.capitalize()}) Intentos: {intentos} - Fecha: {fecha}")

    except IOError as e:
        print(f"❌ Error de I/O al leer el archivo de marcador: {e}")
    except Exception as e:
        print(
            f"❌ Error inesperado al leer o procesar el archivo de marcador: {e}")


# Lógica principal del juego. Adivinar un número en un rango dado por la dificultad.
def adivinar_numero(dificultad: str):

    # Usa el diccionario de configuración para obtener el límite.
    limite = LIMITES_DIFICULTAD.get(dificultad)

    if limite is None:
        print("Dificultad no válida, inténtalo de nuevo.")
        # Si la dificultad no es válida, termina la ejecución de la función.
        return

    # Genera el número secreto dentro del rango (1 a 'limite').
    numero_secreto = random.randint(1, limite)
    intentos = 0

    print(
        f"\nJUGANDO: Dificultad {dificultad.capitalize()}, Rango: 1 a {limite}.")

    # Bucle infinito que se ejecuta hasta que el usuario acierta (break).
    while True:
        try:
            # Pide la entrada del usuario y la convierte inmediatamente a entero.
            suposicion = int(input("Ingresa tu número: "))
        except ValueError:
            # Manejo de errores si el usuario ingresa texto en lugar de un número.
            print("Entrada no válida, por favor ingresa un número entero.")
            # Vuelve al inicio del bucle sin contar el intento fallido.
            continue

        # Verificación adicional para asegurar que el número esté dentro del rango
        if not (1 <= suposicion <= limite):
            print(f"⚠️ ¡Ojo! El número debe estar entre 1 y {limite}.")
            continue

        # Incrementa el contador de intentos solo si la entrada es un número válido.
        intentos += 1

        if suposicion == numero_secreto:
            # Si acierta, imprime el mensaje de felicitación.
            print(
                f"¡Felicidades! Adivinaste el número secreto en {intentos} intentos.")
            # Llama a la función para guardar el resultado en el marcador.
            guardar_resultado(dificultad, intentos)
            # Sale del bucle While.
            break
        elif suposicion < numero_secreto:
            # Pista si el número secreto es mayor.
            print("El número secreto es MAYOR, inténtalo de nuevo.")
        else:
            # Pista si el número secreto es menor.
            print("El número secreto es MENOR, inténtalo de nuevo.")


# Función principal que gestiona el menú y la interacción con el usuario.
def main():
    while True:
        print("\n--- ELIGE LA DIFICULTAD ---")
        print("1. Fácil (1-50)")
        print("2. Normal (1-100)")
        print("3. Dificil (1-200)")
        print("4. Ver Marcador 🏆")
        print("'s' para salir")

        opcion = input("Ingresa tu opción (1, 2, 3, 4 o 's' para salir): ")
        opcion_limpia = opcion.lower().strip()  # Normalizar la entrada

        if opcion_limpia == 's':
            print("👋 ¡Adiós! Gracias por jugar.")
            break
        elif opcion_limpia == '1':
            adivinar_numero("facil")
        elif opcion_limpia == '2':
            adivinar_numero("normal")
        elif opcion_limpia == '3':
            adivinar_numero("dificil")
        elif opcion_limpia == '4':
            # Llama a la función de visualización.
            mostrar_marcador()
        else:
            print("❌ Opción no válida. Por favor, ingresa 1, 2, 3, 4 o 's'.")


if __name__ == "__main__":
    # Garantiza que main() se ejecute solo cuando el script se inicia directamente.
    main()
