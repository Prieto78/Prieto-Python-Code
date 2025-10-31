from PIL import Image
import os

# La cadena de caracteres ASCII que mapea el brillo: de los más densos/oscuros (izquierda) a los más claros/vacíos (derecha).
CARACTERES_ASCII = "@%#*+=-:. "

# =====================================================================
#                        FUNCIONES AUXILIARES
# =====================================================================


# Carga una imagen desde una ruta, la abre y la convierte a escala de grises.
def cargar_imagen(ruta_imagen):
    try:
        # 1. Abre la imagen del disco.
        imagen_original = Image.open(ruta_imagen)
        # 2. Convierte la imagen al modo 'L' (Luminosidad/Escala de grises).
        imagen_gris = imagen_original.convert("L")
        return imagen_gris
    except FileNotFoundError:
        print(f"❌ Error: La imagen en '{ruta_imagen}' no fue encontrada.")
        return None
    # Captura otros posibles errores, como archivos corruptos.
    except Exception as e:
        print(f"❌ Error al cargar la imagen: {e}")
        return None


# Redimensiona una imagen manteniendo su proporción.
def redimensionar_imagen(imagen, nuevo_ancho=100):
    ancho_original, alto_original = imagen.size
    ratio_aspecto = alto_original / ancho_original

    # El factor '0.55' corrige la desproporción de los caracteres en la consola.
    nuevo_alto = int(nuevo_ancho * ratio_aspecto * 0.55)

    # Redimensiona la imagen al nuevo par de dimensiones.
    imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto))
    return imagen_redimensionada


# Mapea un valor de brillo (0-255) a un carácter ASCII.
def pixel_caracter(valor_gris):
    longitud = len(CARACTERES_ASCII)

    # Fórmula de mapeo: normaliza el brillo (0-255) al rango de índices (0-9).
    indice = int((valor_gris / 256) * longitud)

    return CARACTERES_ASCII[indice]


# Convierte la imagen completa (pixel por pixel) a una cadena de texto larga sin saltos de línea.
def generar_ascii(imagen_gris):
    datos_pixel = imagen_gris.getdata()
    caracteres_ascii = ""

    # Itera sobre cada valor de brillo y lo mapea a un carácter.
    for valor_gris in datos_pixel:
        caracteres_ascii += pixel_caracter(valor_gris)

    return caracteres_ascii


# Guarda una cadena de texto multilínea en un archivo .txt.
def guardar_archivo(contenido, ruta_completa):
    try:
        # CORRECCIÓN: Usamos el argumento 'ruta_completa' (que ya no tiene valor por defecto)
        with open(ruta_completa, "w", encoding="utf-8") as archivo:
            # Escribe todo el contenido de una vez
            archivo.write(contenido)
        print(f"✅ Arte ASCII guardado con éxito en: {ruta_completa}")
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")


# =====================================================================
#                          FUNCIÓN PRINCIPAL
# =====================================================================


# Función principal que orquesta el proceso de carga, generación y guardado.
def main():
    ruta_imagen = input("Ingresa la ruta de la imagen a convertir: ")

    # Paso 1: Carga la imagen
    imagen_gris = cargar_imagen(ruta_imagen)

    if imagen_gris:
        try:
            print("✅ Imagen cargada (y en escala de grises) correctamente.")

            # Paso 2: Redimensiona la imagen.
            imagen_redimensionada = redimensionar_imagen(imagen_gris)
            print("✅ Imagen redimensionada correctamente.")

            # Paso 3: Genera la cadena de texto ASCII (sin saltos de línea).
            caracteres_ascii = generar_ascii(imagen_redimensionada)
            print("✅ Texto ASCII generado correctamente.")

            # Paso 4: Construye el resultado multilínea y lo imprime.
            resultado_final_multilinea = ""
            ancho_final = imagen_redimensionada.size[0]

            print("\n--- ARTE ASCII GENERADO ---")

            for i in range(0, len(caracteres_ascii), ancho_final):
                segmento_fila = caracteres_ascii[i:i + ancho_final]

                # 1. Concatena la fila con un salto de línea (para guardar en el archivo)
                resultado_final_multilinea += segmento_fila + "\n"

                # 2. Imprime la fila (para mostrar en la consola)
                print(segmento_fila)

            # Paso 5: Opcional - Guardar en un archivo (.txt).
            guardar = input(
                "\n¿Quieres guardar el resultado en un archivo (S/N)? ").lower()
            if guardar == 's':

                # 1. Obtiene el directorio de la imagen de entrada
                directorio_imagen = os.path.dirname(ruta_imagen)
                if not directorio_imagen:
                    # Si solo se dio el nombre del archivo, el directorio es '.' (actual)
                    directorio_imagen = "."

                # 2. Construye la RUTA COMPLETA del nuevo archivo de salida
                nombre_archivo_salida = "resultado_ejemplo.txt"
                ruta_salida = os.path.join(
                    directorio_imagen, nombre_archivo_salida)

                # 3. Llama a guardar_archivo con la RUTA COMPLETA DEL ARCHIVO
                guardar_archivo(resultado_final_multilinea, ruta_salida)

        except Exception as e:
            print(f"❌ Error al procesar: {e}")


if __name__ == "__main__":
    main()
