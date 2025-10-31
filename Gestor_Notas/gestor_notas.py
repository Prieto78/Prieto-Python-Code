# Módulos y Persistencia de Datos: Esta sección se encarga de guardar y cargar las notas para que persistan entre sesiones del programa.

# Módulo esencial para trabajar con JSON, para la conversión de datos entre el formato que usa el programa (la memoria de Python) y el formato que usa el almacenamiento (el archivo JSON), llamado tambien serializar/deserializar datos.
import json
# Módulo para interactuar con el sistema operativo (lo usamos para comprobar si un archivo existe).
import os

# Creamos una variable con el ombre del archivo donde se guardarán todas las notas.
nombre_archivo = "notas.json"


# Creamos la funcion que cargara la lista de notas desde el archivo JSON, si no existe o está vacío, devuelve una lista vacía."""
def cargar_notas():

    # Comprueba si el archivo 'notas.json' existe en el directorio actual.
    if os.path.exists(nombre_archivo):

        # El bloque 'try' intenta ejecutar el código, es crucial para el manejo de archivos.
        try:
            # Abre el archivo en modo lectura (r) con 'with open', lo que asegura que el archivo se cierre automáticamente.
            with open(nombre_archivo, 'r') as f:

                # json.load(f) deserializa y convierte los datos JSON (texto) del archivo de nuevo a objetos de Python (lista de diccionarios) y devuelve el resultado.
                return json.load(f)

        # El bloque 'except' se ejecuta si 'json.load()' falla (Si el archivo existe pero está vacío o corrupto).
        except json.JSONDecodeError:
            print(
                "Advertencia: Archivo de notas vacío o corrupto, iniciando con lista vacía.")

            # Devuelve una lista vacía para que el programa pueda continuar sin errores.
            return []

    # Si el archivo NO existe (primera ejecución), simplemente devuelve una lista vacía para empezar de cero.
    else:
        return []


# Creamos la funcion que guardara la lista de notas de Python en el archivo JSON.
def guardar_notas(notas):

    # Abre el archivo en modo escritura (w)m esto sobrescribe completamente cualquier contenido anterior.
    with open(nombre_archivo, 'w') as f:

        # json.dump(datos, archivo) serializa y convierte la lista de Python ('notas') a formato JSON y la escribe en el archivo (f), podemos usar 'json.dump(notas, f, indent=4)' para que el archivo JSON sea más legible.
        json.dump(notas, f, indent=4)

        # Y podemos imprimir un mensaje de confirmacion.
        print("Notas guardadas correctamente.")


# Funciones CRUD (Crear, Leer, Actualizar, Borrar) y Búsqueda.

# Esta funcion muestra todas las notas guardadas de forma legible.
def leer_notas():

    # Obtiene la lista actual.
    notas = cargar_notas()

    if notas:
        print("\n--- TUS NOTAS ---")

        # Itera sobre cada diccionario ('nota') en la lista.
        for nota in notas:

            # Usa f-strings para imprimir de forma limpia el ID y el Contenido de cada nota.
            print(f"\nID: {nota['id']}")
            print(f"Contenido: {nota['contenido']}")

    # Si no hay ninguna avisamos con un mensaje.
    else:
        print("\nTodavía no tienes ninguna nota.")


# Esta pide el contenido al usuario, crea una ID única y añade la nueva nota a la lista.
def crear_nota():

    # Carga la lista actual para poder añadirle algo.
    notas = cargar_notas()

    # Lógica de ID, garantiza que el nuevo ID sea el más alto + 1.
    if notas:

        # Comprensión de lista, crea una lista temporal con solo los IDs de todas las notas existentes.
        todos_ids = [nota['id'] for nota in notas]

        # Encuentra el ID más grande y le suma 1 para el nuevo ID.
        id_nota = max(todos_ids) + 1

    # Si la lista está vacía, el primer ID es 1.
    else:
        id_nota = 1

    contenido = input("Escribe el contenido de la nueva nota: ")

    # Construye la nueva nota como un diccionario.
    nueva_nota = {"id": id_nota, "contenido": contenido}

    # Añade el nuevo diccionario a la lista de notas.
    notas.append(nueva_nota)

    # Guarda la lista completa (con la nueva nota) en el archivo JSON.
    guardar_notas(notas)

    # Imprimimos un mensaje confirmando que se han guardado los datos.
    print(f"\n✅ Nota con ID {id_nota} creada y guardada.")


# Esta funcion pide un ID y un nuevo contenido, y reemplaza el contenido de la nota correspondiente.
def actualizar_nota():

    # Muestra las notas existentes para que el usuario sepa qué ID elegir.
    leer_notas()
    notas = cargar_notas()

    # El bloque 'try' intenta ejecutar el código.
    try:
        # Pedimos cual nota actualizar en base a su ID.
        id_actualizar = int(
            input("\nIngresa el ID de la nota que quieres actualizar: "))

    # Sale de la función si el ID no es un número.
    except ValueError:
        print("❌ Error: Por favor, ingresa un número válido para el ID.")
        return

    # Bucle para buscar la nota con el ID proporcionado.
    for nota in notas:
        if nota['id'] == id_actualizar:

            # Si se encuentra la nota se pide el nuevo contenido.
            nuevo_contenido = input(
                f"Nota ID {id_actualizar} (Antiguo: '{nota['contenido']}'). Ingresa nuevo contenido: ")

            # Actualiza el diccionario en la lista, al modificar 'nota', esta modificando directamente el diccionario dentro de la lista 'notas'.
            nota['contenido'] = nuevo_contenido

            # Guarda la lista modificada.
            guardar_notas(notas)
            print(f"✅ Nota con ID {id_actualizar} actualizada correctamente.")

            # Detiene la función (ya no es necesario seguir buscando).
            return

    # Este código se ejecuta si el bucle termina sin encontrar la nota (sin ejecutar 'return').
    print(f"❌ Error: No se encontró ninguna nota con el ID {id_actualizar}.")


# Esta funcion pide un ID y lo elimina de la lista de notas.
def borrar_nota():

    leer_notas()
    notas = cargar_notas()

    # El bloque 'try' intenta ejecutar el código.
    try:
        id_borrar = int(
            input("\nIngresa el ID de la nota que quieres borrar: "))

    # Sale de la función si el ID no es un número.
    except ValueError:
        print("❌ Error: Por favor, ingresa un número válido para el ID.")
        return

    # Guarda la cantidad original de notas.
    longitud_inicial = len(notas)

    # Comprensión de lista, crea una NUEVA lista ('notas_filtradas') que incluye SÓLO las notas cuyo ID NO coincide con 'id_borrar', si encuentra el ID, simplemente se salta esa nota, es una forma limpia de "borrar".
    notas_filtradas = [nota for nota in notas if nota['id'] != id_borrar]

    # Si la nueva lista es más corta, significa que se eliminó una nota, reemplaza la lista vieja por la nueva (filtrada).
    if len(notas_filtradas) < longitud_inicial:
        notas = notas_filtradas

        # Guarda la lista más corta.
        guardar_notas(notas)
        print(f"\n✅ Nota con ID {id_borrar} eliminada correctamente.")

    # Las longitudes son iguales, lo que significa que el ID no existía.
    else:
        print(f"\n❌ Error: No se encontró la nota con ID {id_borrar}.")


# Definimos una funcion para la busqueda de notas, pide una palabra clave y muestra todas las notas que la contienen (sin distinguir mayúsculas/minúsculas).
def buscar_notas():

    notas = cargar_notas()

    termino_busqueda = input("\nIngresa la palabra clave para buscar: ")

    # Normaliza el término de búsqueda a minúsculas.
    termino_busqueda = termino_busqueda.lower()

    # Comprensión de lista, filtra las notas donde la palabra clave (en minúsculas) está dentro del contenido de la nota (también en minúsculas).
    notas_encontradas = [
        nota for nota in notas if termino_busqueda in nota['contenido'].lower()]

    # Ponemos un condicional, si la nota es encontrada imprimimos estos mensajes.
    if notas_encontradas:
        print("\n--- RESULTADOS DE BÚSQUEDA ---")
        for nota in notas_encontradas:
            print(f"\nID: {nota['id']}")
            print(f"Contenido: {nota['contenido']}")

    # Mensaje al usuario cuando la búsqueda no produce resultados.
    else:
        print(
            f"\n❌ No se encontraron notas que contengan '{termino_busqueda}'.")

# Bucle principal de la aplicación de consola.


def main():
    # Bucle infinito que mantiene el programa en ejecución hasta que se pulsa '6', muestra el menú de opciones.
    while True:
        print("\n--- GESTOR DE NOTAS ---")
        print("1. Crear nota")
        print("2. Leer notas")
        print("3. Actualizar nota")
        print("4. Borrar nota")
        print("5. Buscar notas")
        print("6. Salir")

        opcion = input("\nElige una opción (1-6): ")

        # Estructura de control: Llama a la función correspondiente según la opción elegida.
        if opcion == '6':
            print("👋 Gracias por usar el gestor de notas. ¡Hasta pronto!")
            # El comando 'break' detiene el bucle 'while True' y termina el programa.
            break
        elif opcion == '1':
            crear_nota()
        elif opcion == '2':
            leer_notas()
        elif opcion == '3':
            actualizar_nota()
        elif opcion == '4':
            borrar_nota()
        elif opcion == '5':
            buscar_notas()
        else:
            # Manejo de error si el usuario no ingresa una opción válida.
            print("❌ Opción no válida, por favor, elige un número del 1 al 6.")


# Punto de entrada del programa
if __name__ == "__main__":
    # Esta línea asegura que la función 'main()' solo se ejecute cuando el archivo se ejecuta directamente (no cuando se importa como un módulo en otro archivo).
    main()
