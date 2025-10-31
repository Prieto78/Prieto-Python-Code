# Importamos requests para las peticiones (mantenido para documentación de uso real).
# import requests
# Importamos json para leer los archivos idem.
import json
# Importamos datetime para mostrar las fechas.
import datetime
# Importamos matplotlib para el gráfico.
import matplotlib.pyplot as plt
# Importamos os para guardar el gráfico.
import os

# --- NOTA IMPORTANTE PARA EL PORTAFOLIO ---

# En un entorno de producción, la clave API nunca debe estar hardcodeada, se carga desde una variable de entorno, aquí usamos un marcador de posicion.
API_KEY = "TU_CLAVE_DE_API_SEGURA"

# --- SIMULACIÓN DE RESPUESTAS DE LA API (MOCK DATA) ---


# Respuesta simulada de /weather para obtener clima actual y coordenadas (Ejemplo: Granada, España), para evitar peticiones HTTP reales.
def mock_clima_actual(ciudad):

    if "granada" in ciudad.lower():
        # Datos basados en Granada, España.
        return {
            # Coordenadas para la segunda llamada
            "coord": {"lon": -3.6, "lat": 37.18},
            "weather": [{"id": 800, "main": "Clear", "description": "cielo despejado", "icon": "01d"}],
            "main": {"temp": 25.5, "feels_like": 25.0, "temp_min": 20.0, "temp_max": 28.0,
                     "pressure": 1012, "humidity": 35},
            "name": "Granada",
            "cod": 200
        }
    else:
        # Simulación de ciudad no encontrada
        print(
            f"❌ Error al obtener el clima: Ciudad '{ciudad}' no encontrada en la simulación.")
        return None


# Respuesta simulada de /onecall para el pronóstico de 7 días para evitar peticiones HTTP reales.
def mock_pronostico_7_dias(latitud, longitud):

    # Generamos timestamps simulados para los próximos 7 días
    now = datetime.datetime.now()
    daily_forecast = []

    # Temperaturas simuladas (con una ligera variación de +2 a -2 grados por día)
    base_temp = 25

    for i in range(7):
        day_date = now + datetime.timedelta(days=i)

        # Simulación de variación de temperatura (baja, media, alta)
        temp_simulada_day = base_temp + (i % 3) - 1
        temp_simulada_min = temp_simulada_day - 5
        temp_simulada_max = temp_simulada_day + 3

        daily_forecast.append({
            "dt": int(day_date.timestamp()),
            "temp": {
                "day": temp_simulada_day,
                "min": temp_simulada_min,
                "max": temp_simulada_max
            },
            "weather": [{"description": "sol" if i < 3 else "nubes dispersas"}]
        })

    return {
        "lat": latitud,
        "lon": longitud,
        "daily": daily_forecast
    }


# --- FUNCIONES CENTRALES CORREGIDAS PARA SIMULACIÓN ---

# Función que llama a la SIMULACIÓN de clima actual, en un entorno real, haría: requests.get(ENDPOINT, params=parametros).
def clima_actual(ciudad):
    return mock_clima_actual(ciudad)

# Función que llama a la SIMULACIÓN del pronóstico, en un entorno real, haría: requests.get(ENDPOINT, params=parametros).


def pronostico_7_dias(latitud, longitud):
    return mock_pronostico_7_dias(latitud, longitud)


def main():
    # Determinamos la ruta del script para guardar el gráfico
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()

    ciudad_buscada = input(
        "Ingresa la ciudad para ver el clima (Ej: Granada): ")

    # Petición 1: Clima actual (ahora simulación) para obtener coordenadas
    datos_clima = clima_actual(ciudad_buscada)

    # --- EXTRACCIÓN Y LLAMADA A PRONÓSTICO ---
    if datos_clima and datos_clima.get('cod', 200) == 200:

        # Extracción de datos del clima actual (temperatura, humedad, descripción)
        temp = datos_clima['main']['temp']
        humedad = datos_clima['main']['humidity']
        descripcion = datos_clima["weather"][0]['description']

        # Extracción de coordenadas para la segunda petición
        lat = datos_clima['coord']['lat']
        lon = datos_clima['coord']['lon']

        # Petición 2: Pronóstico de 7 días (ahora simulación)
        datos_pronostico = pronostico_7_dias(lat, lon)

        # --- EXTRACCIÓN DE DATOS PARA EL GRÁFICO ---
        if datos_pronostico:
            print("\n✅ Datos del pronóstico obtenidos correctamente (simulación).")

            pronostico_semanal = datos_pronostico['daily']
            dias_temp = []
            temperaturas = []

            for dia in pronostico_semanal[:7]:
                timestamp = dia['dt']
                # Usaremos la temperatura del día
                temp_media = dia['temp']['day']

                # Convierte el timestamp a día de la semana (ej. 'Lunes'), configuración local para nombres de días en español.
                import locale
                try:
                    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                except locale.Error:
                    try:
                        locale.setlocale(locale.LC_TIME, 'es_ES')
                    except locale.Error:
                        # Si falla, usa la configuración por defecto (ej. 'Mon')
                        pass

                fecha_formateada = datetime.datetime.fromtimestamp(
                    timestamp).strftime('%a')

                dias_temp.append(fecha_formateada)
                temperaturas.append(temp_media)

            # --- IMPRESIÓN DE DATOS Y GRÁFICO ---

            # Imprime la información del clima actual.
            print(
                f"\n--- CLIMA ACTUAL EN {datos_clima.get('name', ciudad_buscada).capitalize()} ---")
            print(f"🌡️ Temperatura: {temp}°C")
            print(f"💧 Humedad: {humedad}%")
            print(f"☁️ Descripción: {descripcion.capitalize()}")

            print("\n--- GRÁFICO DE PRONÓSTICO ---")

            # Configuración de la figura
            plt.figure(figsize=(10, 5))

            # Gráfico de línea: días en X, temperaturas en Y
            plt.plot(dias_temp, temperaturas, marker='o', linestyle='-',
                     color='#FF6600', linewidth=2, markersize=8)

            # Título y etiquetas
            plt.title(
                f"Pronóstico de Temperatura Media para {datos_clima.get('name', ciudad_buscada).capitalize()}",
                fontsize=14, fontweight='bold')
            plt.xlabel("Día de la semana", fontsize=12)
            plt.ylabel("Temperatura (°C)", fontsize=12)

            # Estilización
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            # Mostrar valores en los puntos
            for i, temp_val in enumerate(temperaturas):
                plt.annotate(f"{temp_val:.1f}°C",
                             (dias_temp[i], temp_val + 0.5), ha='center')

            plt.ylim(min(temperaturas) - 5, max(temperaturas) + 5)

            plt.tight_layout()

            # Guardamos el gráfico en lugar de mostrarlo
            nombre_archivo_salida = "pronostico_semanal.png"
            ruta_salida_completa = os.path.join(
                script_dir, nombre_archivo_salida)

            try:
                plt.savefig(ruta_salida_completa)
                print(
                    f"\n✨ GRÁFICO CREADO: Se ha guardado el gráfico '{nombre_archivo_salida}' en la ruta:\n{ruta_salida_completa}")
                print("\n--- NOTA PARA EL PORTAFOLIO ---")
                print(
                    "Para ver el gráfico, ejecuta este script de forma local y abre el archivo PNG generado.")

            except Exception as e:
                print(f"\n❌ Error al guardar el gráfico: {e}")

    else:
        # Se maneja el caso de que la primera petición (simulada) falle.
        print("\n❌ No se pudo continuar con el pronóstico.")


if __name__ == "__main__":
    main()
