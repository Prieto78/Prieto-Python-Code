import sqlite3

# =====================================================================
#                          CLASES (POO)
# =====================================================================


# Clase para modelar un ingrediente con sus propiedades: nombre, cantidad y unidad.
class Ingrediente:

    def __init__(self, nombre: str, cantidad: float, unidad: str):
        # Atributos de la instancia
        self.nombre = nombre
        self.cantidad = cantidad
        self.unidad = unidad

    def mostrar_info(self):
        # Devuelve una cadena legible con la información del ingrediente.
        return f"{self.cantidad} {self.unidad} de {self.nombre}"


# Clase principal que modela una receta, compuesta por objetos Ingrediente.
class Receta:

    def __init__(self, nombre: str, tiempo_prep: int):
        self.nombre = nombre
        self.tiempo_prep = tiempo_prep
        # Composición: Cada receta contiene una lista de objetos Ingrediente.
        self.ingredientes = []

    def agregar_ingrediente(self, ingrediente: Ingrediente):
        # Añade un objeto Ingrediente a la lista de la receta.
        self.ingredientes.append(ingrediente)

    # MÉTODO DE INSTANCIA: Guarda el objeto actual en la BD.
    def guardar_db(self, conn, cursor):

        # Guarda la instancia actual (la receta) y todos sus ingredientes en una ÚNICA transacción atómica, si algo falla, se deshace todo.
        print(f"\nIniciando guardado atómico de receta: {self.nombre}")

        try:
            # La transacción se maneja externamente, no hacemos commit aquí.

            # 1. Guardar la receta principal y obtener el ID autogenerado.
            receta_id = insertar_receta_db_no_commit(
                cursor, self.nombre, self.tiempo_prep)

            print(
                f"-> Receta insertada, esperando confirmación, ID: {receta_id}")

            # 2. Iterar sobre todos los objetos Ingrediente.
            for ingrediente in self.ingredientes:
                # 3. Guardar cada ingrediente, usando 'receta_id' como CLAVE FORÁNEA (FK).
                insertar_ingrediente_db(cursor,
                                        ingrediente.nombre,
                                        ingrediente.cantidad,
                                        ingrediente.unidad,
                                        receta_id)

            # 3. Confirmar la inserción de la Receta y TODOS sus ingredientes.
            conn.commit()
            print("✅ Transacción completada con éxito, datos confirmados en la BD.")

        except sqlite3.Error as e:
            # Si algo falla (ej. error de datos), hacemos rollback.
            conn.rollback()
            print(f"❌ ERROR de Transacción, se ejecutó ROLLBACK, detalle: {e}")

        except Exception as e:
            conn.rollback()
            print(f"❌ ERROR INESPERADO, se ejecutó ROLLBACK, detalle: {e}")

    # MÉTODO DE CLASE: Carga y crea un nuevo objeto Receta a partir de la BD.

    @classmethod
    def cargar_por_id(cls, cursor, id_cargar: int):
        # Crea y devuelve un objeto Receta completo (con ingredientes) desde la BD.

        # 1. Cargar la fila principal de la receta.
        datos_receta = cargar_receta_id_db(cursor, id_cargar)

        if not datos_receta:
            # Receta no encontrada.
            return None

        # Desempaquetar los datos: (id, nombre, tiempo_prep)
        receta_id, nombre, tiempo_prep = datos_receta

        # 2. Crear la nueva instancia de la Receta
        receta_cargada = cls(nombre, tiempo_prep)

        # 3. Cargar las filas de los ingredientes usando el ID.
        filas_ingredientes = cargar_ingredientes_de_receta_db(
            cursor, receta_id)

        # 4. Iterar sobre las filas y crear objetos Ingrediente.
        for nombre_ing, cantidad_ing, unidad_ing in filas_ingredientes:
            nuevo_ing = Ingrediente(nombre_ing, cantidad_ing, unidad_ing)

            # 5. Añadir el objeto Ingrediente a la Receta cargada.
            receta_cargada.agregar_ingrediente(nuevo_ing)

        print(f"✅ Receta '{nombre}' (ID {receta_id}) cargada con éxito.")

        # 6. Devolver el objeto POO completo.
        return receta_cargada


# =====================================================================
#                        FUNCIONES AUXILIARES (SQL)
# =====================================================================


# Conecta o crea la base de datos y devuelve la conexión, usamos el manejador de contexto (with) para la conexión en main()
def inicializar_bd():
    conn = sqlite3.connect("Recetas_veganas.db")
    # PRAGMA: Asegura que la integridad referencial (Foreign Keys) sea aplicada.
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Crea las tablas RECETAS y INGREDIENTES y define la Clave Foránea (FK).
def crear_tablas_iniciales(cursor, conn=None):

    # 1. Tabla Padre: RECETAS
    comando_sql_recetas = """
    CREATE TABLE IF NOT EXISTS RECETAS (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL, 
        tiempo_prep INTEGER
    )
    """
    cursor.execute(comando_sql_recetas)

    # 2. Tabla Hija: INGREDIENTES
    comando_sql_ingredientes = """
    CREATE TABLE IF NOT EXISTS INGREDIENTES (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        cantidad REAL,
        unidad TEXT,
        receta_id INTEGER,
        
        -- CLAVE FORÁNEA: El vínculo al ID de la tabla RECETAS
        FOREIGN KEY (receta_id) REFERENCES RECETAS(id) ON DELETE CASCADE
    )
    """
    cursor.execute(comando_sql_ingredientes)

    if conn:
        conn.commit()
    print("✅ Tablas 'RECETAS' e 'INGREDIENTES' verificadas o creadas con éxito.")


# Función para limpiar los datos para demostración.
def limpiar_tablas(cursor, conn):
    cursor.execute("DELETE FROM INGREDIENTES")
    cursor.execute("DELETE FROM RECETAS")
    conn.commit()
    print("🧹 Tablas 'RECETAS' e 'INGREDIENTES' limpiadas para la demostración.")


# Inserta una receta pero NO hace commit, dejando la transacción abierta.
def insertar_receta_db_no_commit(cursor, nombre: str, tiempo_prep: int):
    comando_sql = "INSERT INTO RECETAS (nombre, tiempo_prep) VALUES (?, ?)"
    cursor.execute(comando_sql, (nombre, tiempo_prep))
    receta_id = cursor.lastrowid
    return receta_id


# Inserta un ingrediente, vinculándolo con la receta_id (NO hace commit).
def insertar_ingrediente_db(cursor, nombre: str, cantidad: float, unidad: str, receta_id: int):
    comando_sql = "INSERT INTO INGREDIENTES (nombre, cantidad, unidad, receta_id) VALUES (?, ?, ?, ?)"
    datos_ingrediente = (nombre, cantidad, unidad, receta_id)
    cursor.execute(comando_sql, datos_ingrediente)
    print(f"   -> Ingrediente '{nombre}' insertado en buffer.")


# Busca una fila en RECETAS por su ID.
def cargar_receta_id_db(cursor, receta_id: int):
    comando_sql = "SELECT id, nombre, tiempo_prep FROM RECETAS WHERE id = ?"
    cursor.execute(comando_sql, (receta_id,))
    return cursor.fetchone()


# Busca todas las filas de INGREDIENTES vinculadas a un receta_id.
def cargar_ingredientes_de_receta_db(cursor, receta_id: int):
    comando_sql = "SELECT nombre, cantidad, unidad FROM INGREDIENTES WHERE receta_id = ?"
    cursor.execute(comando_sql, (receta_id,))
    return cursor.fetchall()


# =====================================================================
#                                EJECUCIÓN
# =====================================================================


# Función principal que demuestra las funcionalidades de guardar y cargar.
def main():

    # Utilizamos el manejador de contexto 'with' para la conexión, asegura el cierre y maneja la transacción.
    with inicializar_bd() as conn:
        cursor = conn.cursor()

        # 1. Crear la estructura de la BD y limpiar datos antiguos
        crear_tablas_iniciales(cursor)
        # Limpiar para que el ID siempre sea 1 en la demo
        limpiar_tablas(cursor, conn)

        # --- DEMOSTRACIÓN DE GUARDADO (Persistencia: POO -> SQL) ---

        # Creamos un objeto Receta con sus objetos Ingrediente
        mi_receta = Receta("Curry de Garbanzos y Espinacas", 35)
        mi_receta.agregar_ingrediente(
            Ingrediente("Garbanzos Cocidos", 400.0, "gramos"))
        mi_receta.agregar_ingrediente(
            Ingrediente("Leche de Coco", 200.0, "ml"))
        mi_receta.agregar_ingrediente(
            Ingrediente("Espinacas", 100.0, "gramos"))

        print("\n--- PASO 1: GUARDADO (POO -> SQL) ---")

        # La transacción se maneja internamente en el método guardar_db
        mi_receta.guardar_db(conn, cursor)

        # --- DEMOSTRACIÓN DE CARGA (Reconstrucción: SQL -> POO) ---

        id_a_cargar = 1  # Usamos el ID que sabemos que se guardó
        print("\n--- PASO 2: CARGA (SQL -> POO) ---")

        # Usamos el método de clase 'cargar_por_id' para crear el objeto.
        receta_cargada = Receta.cargar_por_id(cursor, id_a_cargar)

        # Verificación del objeto recreado
        if receta_cargada:
            print("\n--- Verificación del Objeto Cargado ---")
            print(f"Objeto de Python recreado: {receta_cargada.nombre}")
            print(
                f"Tiempo de preparación: {receta_cargada.tiempo_prep} minutos")
            print("Detalle de Ingredientes (cargados de la BD):")
            for ing in receta_cargada.ingredientes:
                print(f" - {ing.mostrar_info()}")
        else:
            print("❌ Error: No se pudo cargar la receta con ID 1.")

    # La conexión se cierra automáticamente al salir del bloque 'with'


if __name__ == "__main__":
    main()
