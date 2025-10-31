# **🐍 Mi Portafolio de Proyectos de Python 2025**

**Hola, soy Prieto, de Granada, España,** mi objetivo con este repositorio es presentar una colección de **11 proyectos** de Python que demuestran habilidades clave en el desarrollo de scripts, manejo de archivos, bases de datos (SQL), consumo de APIs (simulado), y visualización de datos.

## **🚀 Tecnologías Principales Usadas**

* **Lenguaje:** Python 3.10+  
* **Análisis y Datos:** pandas, sqlite3  
* **Visualización:** matplotlib, wordcloud  
* **Manipulación de Archivos:** Pillow (PIL), os, shutil, json, csv  
* **Web (Ejemplos):** Streamlit (en Generador de Contraseñas)

## **✅ Lista de 11 Proyectos Incluidos**

Aquí están los 11 proyectos que demuestran las habilidades clave, organizados por la complejidad de las funcionalidades:

| N° | Nombre del Proyecto | Habilidades Demostradas |
| :---- | :---- | :---- |
| 1\. | **Adivinar\_Numero** | Scripts básicos, bucles, manejo de errores de entrada. |
| 2\. | **Conversor\_Divisas** | Manejo de APIs (simulado), CSV, manejo de errores robusto. |
| 3\. | **Generador\_ASCII** | Manejo de imágenes (Pillow), operaciones con archivos, I/O. |
| 4\. | **Generador\_Contraseñas** | Lógica de seguridad, generación aleatoria, manejo de **Streamlit**. |
| 5\. | **Gestor\_Archivos** | Módulos os y shutil, manipulación de rutas y directorios. |
| 6\. | **Gestor\_Notas** | Manejo de archivos JSON, estructuración de datos. |
| 7\. | **Gestor\_Recetas\_DB** | Programación Orientada a Objetos (POO), **SQLite**, transacciones atómicas. |
| 8\. | **Nube\_Palabras** | Procesamiento de texto, librería wordcloud, manejo de archivos. |
| 9\. | **Panel\_Videojuegos** | Análisis de Datos (pandas), Visualización (matplotlib), limpieza de datos. |
| 10\. | **Seguidor\_Precios** | Simulación de Web Scraping, persistencia en CSV, gráficos de evolución. |
| 11\. | **Visualizador\_Clima** | Consumo de APIs (simulado), extracción de JSON, visualización avanzada. |

## **🛑 Importante: APIs y Simulación (Mocking)**

Los proyectos que dependen de APIs externas (como el **Conversor\_Divisas** o el **Visualizador\_Clima**) están configurados con una **simulación de datos (mocking)** en lugar de hacer llamadas HTTP reales. Esto se hace por dos razones:

1. **Seguridad:** Evita exponer claves API sensibles.  
2. **Entorno:** Garantiza que los scripts demuestren la lógica de extracción de datos, incluso en entornos de ejecución restringidos.

## **🛠️ Cómo Ejecutar los Proyectos**

1. **Clonar el Repositorio:**  
   git clone \[https://github.com/Prieto78/Prieto-Python-Code.git\](https://github.com/Prieto78/Prieto-Python-Code.git)  
   cd Prieto-Python-Code/

2. **Configurar Entorno Virtual (Recomendado):**  
   python \-m venv venv  
   source venv/bin/activate  \# En Linux/macOS  
   venv\\Scripts\\activate     \# En Windows

3. Instalar Dependencias:  
   Accede a la carpeta del proyecto que quieras ejecutar e instala las dependencias de su archivo requisitos.txt.  
   (Ejemplo para el Panel de Videojuegos)  
   cd Panel\_Videojuegos  
   pip install \-r requisitos.txt

4. **Ejecutar el Script:**  
   python panel\_videojuegos.py

   *(Para proyectos que usan Streamlit, usa streamlit run generador\_contraseñas\_web.py)*
