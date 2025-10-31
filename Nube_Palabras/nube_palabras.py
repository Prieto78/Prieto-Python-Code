# Módulos y dependencias de Python (Necesitarán instalación local: pip install wordcloud matplotlib)
import collections
import string
# Importamos la clase WordCloud directamente para generar la nube.
from wordcloud import WordCloud
# Importamos Matplotlib para mostrar la imagen generada (solo necesario para plt.show() localmente).
import matplotlib.pyplot as plt
# Módulo para el sistema operativo
import os
from typing import Optional, List, Dict, Any

# --- CONSTANTES ---


# Lista de palabras comunes que no aportan valor significativo (stopwords) en español.
STOPWORDS_ESPANOL = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "u", "de", "en", "que", "a",
    "al", "del", "es", "son", "se", "por", "para", "con", "como", "mas", "más", "mi", "me", "te",
    "tu", "su", "sus", "no", "si", "lo", "le", "les", "ha", "han", "he", "está", "están", "este",
    "esta", "esto", "pero", "además", "sin", "también", "yo", "nos", "vos", "ello", "ese", "esa", "aquel", "aquella",
    "ser", "estar", "tener", "hacer", "poder", "ir", "haber"
}


# Lee el contenido de un archivo de texto de forma segura manejando errores, ruta_archivo: La ruta completa del archivo a leer, :return: El contenido del archivo como una cadena, o None si hay error.
def leer_archivo(ruta_archivo: str) -> Optional[str]:
    try:
        # Usamos 'with open' para asegurar que el archivo se cierre automáticamente. es crucial especificar la codificación 'utf-8' para manejar tildes y caracteres especiales.
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            return contenido

    except FileNotFoundError:
        print(f"❌ Error: El archivo '{ruta_archivo}' no fue encontrado.")
        return None
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return None


# Limpia, analiza el texto, muestra las estadísticas y genera la Nube de Palabras
def analizar_texto(texto: str):

    # 1. LIMPIEZA INICIAL: Convierte a minúsculas y elimina la puntuación de los bordes, usamos .split() sin argumentos para dividir por cualquier espacio en blanco (incluyendo saltos de línea).
    palabras_divididas = texto.lower().split()

    # Lista para almacenar las palabras limpias y relevantes
    texto_final: List[str] = []

    # 2. PROCESAMIENTO, FILTRADO Y REFINAMIENTO
    for palabra in palabras_divididas:
        # Elimina la puntuación de los bordes (ej: "palabra." -> "palabra")
        palabra_limpia = palabra.strip(string.punctuation)

        # Filtra palabras vacías (que eran solo puntuación), stopwords y palabras muy cortas (ej: letras sueltas)
        if palabra_limpia and palabra_limpia not in STOPWORDS_ESPANOL and len(palabra_limpia) > 2:
            texto_final.append(palabra_limpia)

    # 3. CONTEO DE FRECUENCIAS

    # collections.Counter es ideal para este propósito.
    contador_palabras = collections.Counter(texto_final)

    # 4. CÁLCULO DE ESTADÍSTICAS
    total_palabras = len(texto_final)
    palabras_unicas = len(contador_palabras)

    # --- SALIDA DE ESTADÍSTICAS EN CONSOLA ---
    print("\n" + "="*40)
    print("--- ✅ ESTADÍSTICAS DEL TEXTO ANALIZADO ---")
    print(f"Total de palabras (relevantes y limpias): {total_palabras}")
    print(f"Palabras únicas (tamaño del vocabulario): {palabras_unicas}")
    print("="*40)

    print("\n--- 🔎 TOP 10 PALABRAS MÁS COMUNES ---")
    if contador_palabras:
        # .most_common(10) devuelve las 10 tuplas (palabra, frecuencia) más frecuentes.
        for palabra, frecuencia in contador_palabras.most_common(10):
            print(f"'{palabra}': {frecuencia} veces")
    else:
        print("No se encontraron palabras relevantes después del filtrado.")

    # --- GENERACIÓN Y EXPORTACIÓN DE NUBE DE PALABRAS ---
    if contador_palabras:
        # 1. Crea el objeto WordCloud con parámetros de diseño.
        wc = WordCloud(
            background_color="white",
            width=800,
            height=400,
            # Asegura el uso de la lista de stopwords de Python
            stopwords=STOPWORDS_ESPANOL,
            # Evita contar frases, solo palabras individuales
            collocations=False
        )

        # 2. Genera la imagen a partir del objeto Counter (las frecuencias).
        wc.generate_from_frequencies(contador_palabras)

        nombre_archivo = "wordcloud_output.png"

        # OBTENEMOS LA RUTA ABSOLUTA DEL SCRIPT:
        # __file__ contiene la ruta del script, pero solo si se ejecuta directamente, os.path.abspath lo convierte en una ruta absoluta, os.path.dirname obtiene el directorio de esa ruta absoluta, y os.path.join une el directorio con el nombre del archivo de salida.
        try:
            # Necesario para el entorno de ejecución, donde __file__ puede no estar definido
            script_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            # Fallback si __file__ no está disponible (ej: en algunos shells interactivos)
            script_dir = os.getcwd()

        # Construimos la ruta completa donde se guardará el archivo
        ruta_salida_completa = os.path.join(script_dir, nombre_archivo)

        # 3. Guarda la imagen generada como un archivo PNG.
        wc.to_file(ruta_salida_completa)
        print(
            f"\n✨ NUBE DE PALABRAS CREADA: Se ha guardado el archivo '{ruta_salida_completa}' en la carpeta del script.")

        # COMENTARIO CRÍTICO PARA EL PORTAFOLIO:
        print("\n--- NOTA IMPORTANTE PARA EL VISUALIZADOR ---")
        print("El comando 'plt.show()' no es compatible con el entorno web de Canvas.")
        print("Si ejecutas este archivo Python de forma local, el archivo 'wordcloud_output.png' se generará en tu carpeta y la siguiente línea lo mostrará")

        # 4. Muestra la imagen en la pantalla usando Matplotlib (descomentar y ejecutar localmente)
        # plt.imshow(wc, interpolation='bilinear')
        # plt.axis("off")
        # plt.show()

    else:
        print("⚠️ Advertencia: No hay suficientes palabras para generar la nube.")


# Función principal para gestionar el menú y la entrada de texto.
def main():
    # Bucle infinito para permitir múltiples análisis.
    while True:
        print("\n--- ANALIZADOR DE TEXTO Y NUBE DE PALABRAS (PYTHON) ---")
        print("1. Ingresar texto directamente")
        print("2. Leer texto desde un archivo (.txt)")
        print("3. Salir")

        opcion = input("Elige una opción (1, 2, 3): ").strip()

        if opcion == '3':
            print("👋 ¡Hasta pronto!")
            break

        texto = None
        if opcion == '1':
            # Opción 1: lee la entrada del usuario directamente.
            print("\nPega o escribe tu párrafo aquí (finaliza con ENTER):")
            texto = input()

        elif opcion == '2':
            # Opción 2: pide la ruta y usa la función de lectura segura.
            ruta = input(
                "Ingresa la ruta completa del archivo .txt (ej: archivo.txt): ").strip()
            texto = leer_archivo(ruta)

        else:
            print("❌ Opción no válida.")
            continue

        # Solo procede al análisis si la variable 'texto' tiene contenido.
        if texto and texto.strip():
            analizar_texto(texto)
        elif texto is not None:
            print("❌ El texto ingresado o leído está vacío. Inténtalo de nuevo.")


if __name__ == "__main__":
    # La variable __file__ solo está definida cuando el script se ejecuta directamente, esta verificación asegura que el script_dir funcione correctamente en 'analizar_texto'.
    main()
