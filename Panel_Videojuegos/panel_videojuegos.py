# Importa la librería fundamental para la manipulación y análisis de datos.
import pandas as pd
# Importa la librería para la creación de gráficos (visualización).
import matplotlib.pyplot as plt
# Importa el módulo OS para la gestión de rutas de archivos.
import os
from typing import Optional, List, Dict, Any

# Nombre del archivo de datos CSV.
RUTA_ARCHIVO = "steam_juegos.csv"


# Carga, limpia, calcula métricas y visualiza el Top 10 de juegos.
def analizar_juegos(ruta_archivo: str):

    # ---------------------------------------------------------------
    # Solución al problema de ruta: Construimos la ruta ABSOLUTA del script, el script busca el archivo en la misma carpeta donde se encuentra este script.
    try:
        # Intenta obtener el directorio del script
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # Fallback si __file__ no está disponible (ejecución en entorno interactivo)
        script_dir = os.getcwd()

    # Ruta completa del archivo CSV para la carga
    ruta_archivo_completa = os.path.join(script_dir, ruta_archivo)
    # ---------------------------------------------------------------

    # --- FASE DE CARGA DE DATOS ---
    try:
        # pd.read_csv() es una función del módulo pandas que carga el archivo en el objeto DataFrame (df), usamos la ruta absoluta calculada.
        df = pd.read_csv(ruta_archivo_completa)
    except FileNotFoundError:
        print(
            f"❌ Error: El archivo de datos '{ruta_archivo}' no fue encontrado en la ruta:\n{ruta_archivo_completa}")
        print("Asegúrate de que 'steam_juegos.csv' está en la misma carpeta que el script.")
        return
    except Exception as e:
        print(f"❌ Error al cargar el archivo de datos: {e}")
        return

    print("--- ✅ Analisis inicial de datos ---")
    print(df.head())
    print("\nDetalles del DataFrame (antes de la limpieza):")
    df.info()

    # --- FASE DE LIMPIEZA Y PREPARACIÓN ---

    # 1. Limpieza de símbolos, convertimos a string primero para manejar valores mixtos, reemplazamos '€', y reemplazamos comas (,) por puntos (.) por robustez.
    df['Precio'] = df['Precio'].astype(str).str.replace(
        '€', '').str.replace(',', '.').str.strip()

    # 2. Conversión a numérico, 'errors="coerce"' convierte cualquier valor problemático a NaN (nulo).
    df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')

    # Aseguramos que las columnas de calificaciones sean numéricas (manejando posibles strings)
    df['Calificaciones_Positivas'] = pd.to_numeric(
        df['Calificaciones_Positivas'], errors='coerce')
    df['Calificaciones_Negativas'] = pd.to_numeric(
        df['Calificaciones_Negativas'], errors='coerce')

    # 3. Filtrado de nulos
    df = df.dropna(
        subset=['Precio', 'Calificaciones_Positivas', 'Calificaciones_Negativas'])

    # 4. Eliminacion de gratuitos
    df = df[df['Precio'] > 0.0]

    # --- FASE DE CÁLCULO DE MÉTRICAS ---

    # 5. Creamos la nueva columna 'Ratio_Positivo'
    df['Total_Calificaciones'] = df['Calificaciones_Positivas'] + \
        df['Calificaciones_Negativas']

    # Filtro Adicional: Solo consideramos juegos con un mínimo de calificaciones para asegurar relevancia, se recomienda un umbral de al menos 50 calificaciones para que el ratio sea significativo.
    df = df[df['Total_Calificaciones'] > 50]

    # Calcular el Ratio
    df['Ratio_Positivo'] = df['Calificaciones_Positivas'] / \
        df['Total_Calificaciones']

    # 6. Ordenamiento del dataframe
    df_ordenado = df.sort_values(by='Ratio_Positivo', ascending=False)

    # Selección del Top 10
    top_10 = df_ordenado.head(10)

    print("\n--- ✅ Top 10 Juegos por Ratio de Calificaciones Positivas ---")
    # Mostramos las columnas clave en la consola
    if not top_10.empty:
        print(top_10[['Nombre', 'Ratio_Positivo', 'Precio',
                      'Total_Calificaciones']].to_string(index=False))
    else:
        print("No se encontraron 10 juegos que cumplan con los criterios de filtrado.")

    # --- FASE DE VISUALIZACIÓN Y EXPORTACIÓN ---
    if top_10.empty:
        print("\n⚠️ Advertencia: No hay suficientes datos para generar el gráfico después del filtrado.")
        return

    # 8. Creación del Gráfico

    # Define el tamaño de la figura para mejor legibilidad
    plt.figure(figsize=(12, 7))

    # Gráfico de barras
    plt.bar(top_10['Nombre'], top_10['Ratio_Positivo'], color='#1f77b4')

    # 9. Etiquetas y títulos
    plt.xlabel('Juego', fontsize=12, labelpad=15)
    plt.ylabel("Ratio Positivo (1.0 = 100%)", fontsize=12, labelpad=15)
    plt.title("Top 10 Juegos por Ratio de Calificaciones Positivas (Steam)",
              fontsize=16, weight='bold')

    # Rota las etiquetas del eje X 45 grados para evitar que los nombres largos se superpongan.
    plt.xticks(rotation=45, ha='right', fontsize=10)

    # Configuración de ejes
    plt.yticks(fontsize=10)
    # Ajusta el límite Y para centrar la atención en los ratios altos
    plt.ylim(0.9, 1.0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # Asegura que las etiquetas no se corten
    plt.tight_layout()

    # 10. Guarda el gráfico en la misma carpeta que el script
    nombre_archivo_salida = "top10_juegos_steam.png"

    try:
        # La ruta absoluta del script (script_dir) fue calculada al inicio y construimos ahora la ruta completa
        ruta_salida_completa = os.path.join(script_dir, nombre_archivo_salida)

        # Guarda el gráfico en la ruta completa
        plt.savefig(ruta_salida_completa)
        print(
            f"\n✨ GRÁFICO CREADO: Se ha guardado el gráfico '{nombre_archivo_salida}' en la ruta:\n{ruta_salida_completa}")

        print("\n--- NOTA PARA EL PORTAFOLIO ---")
        print("La visualización con 'plt.show()' no es compatible con el entorno web de Canvas.")
        print("Para ver el gráfico, ejecuta este script de forma local (asegúrate de tener el CSV) y abre el archivo PNG generado.")

    except Exception as e:
        print(f"\n❌ Error al guardar el gráfico: {e}")


def main():
    analizar_juegos(RUTA_ARCHIVO)


if __name__ == "__main__":
    main()
