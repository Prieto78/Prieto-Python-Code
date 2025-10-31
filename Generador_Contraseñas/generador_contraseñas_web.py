# Importamos string para acceder a las colecciones de caracteres predefinidas.
import string
# Importamos random para generar números aleatorios.
import random
# Importamos la librería de la interfaz web (Streamlit).
import streamlit as st
# Tipado
from typing import List


# Definición de sets de caracteres necesarios
LETRAS_MINUSCULAS = string.ascii_lowercase
LETRAS_MAYUSCULAS = string.ascii_uppercase
NUMEROS = string.digits
SIMBOLOS = string.punctuation

# Combinación de todos los caracteres posibles para el relleno aleatorio.
TODOS_CARACTERES = LETRAS_MAYUSCULAS + LETRAS_MINUSCULAS + NUMEROS + SIMBOLOS


# Funcion para generar una contraseña segura garantizando al menos un carácter de cada tipo (Mayúscula, minúscula, número, símbolo).
def generar_contrasena(longitud: int) -> str:

    # 1. Forzar la inclusión de un caracter de cada tipo.
    contraseña: List[str] = [
        random.choice(LETRAS_MAYUSCULAS),
        random.choice(LETRAS_MINUSCULAS),
        random.choice(NUMEROS),
        random.choice(SIMBOLOS)
    ]

    # 2. Calcular cuántos caracteres adicionales necesitamos.
    relleno = longitud - len(contraseña)

    # 3. Rellenar la contraseña con caracteres aleatorios.
    for _ in range(relleno):
        caracter_aleatorio = random.choice(TODOS_CARACTERES)
        contraseña.append(caracter_aleatorio)

    # 4. Mezclar la lista para que los caracteres obligatorios no queden al inicio.
    random.shuffle(contraseña)

    # 5. Convertir la lista barajada de nuevo a una sola cadena y retornarla.
    return "".join(contraseña)


# --- CONFIGURACIÓN DE LA INTERFAZ STREAMLIT ---

# Añadimos un título para la aplicación web
st.set_page_config(page_title="Generador de Contraseñas", layout="centered")
st.title("🛡️ Generador de Contraseñas Seguras")
st.markdown(
    "Crea contraseñas robustas garantizando la inclusión de mayúsculas, minúsculas, números y símbolos.")

# --- INICIALIZACIÓN DEL ESTADO ---

# Inicializamos el estado de sesión de Streamlit para almacenar la contraseña generada y el control de los caracteres (opcionalmente)
if 'contraseña_actual' not in st.session_state:
    st.session_state.contraseña_actual = ""

# 1. Widget para la longitud de la contraseña (Fuera de cualquier condicional)
longitud = st.slider(
    "Longitud de la contraseña",
    min_value=8,
    max_value=128,
    value=16,  # Valor por defecto de 16
    step=1
)

# 2. Botón de Generación
if st.button("Generar Nueva Contraseña", type="primary", use_container_width=True):
    # Generamos la contraseña
    nueva_contraseña = generar_contrasena(longitud)
    # Guardamos la nueva contraseña en el estado de sesión
    st.session_state.contraseña_actual = nueva_contraseña
    st.toast("Contraseña generada con éxito.", icon="✅")


# 3. Campo de Salida y Copiado, al estar fuera del botón, el widget siempre se renderiza, pero su 'value' viene del estado.
st.text_input(
    label="Contraseña Generada",
    value=st.session_state.contraseña_actual,
    type="password",  # Opcional: Oculta la contraseña por defecto
    disabled=True,  # No permitimos la edición manual
    key="password_output"  # Clave única para el widget
)

# Creamos un botón de "Mostrar Contraseña"
if st.session_state.contraseña_actual and st.checkbox("Mostrar Contraseña"):
    st.code(st.session_state.contraseña_actual, language=None)

# 4. Indicador de Seguridad (Visual extra)
if st.session_state.contraseña_actual:
    longitud_str = "Muy débil"
    if longitud >= 12:
        longitud_str = "Media"
    if longitud >= 16:
        longitud_str = "Fuerte"
    if longitud >= 20:
        longitud_str = "Muy Fuerte"

    st.info(
        f"Nivel de Seguridad: **{longitud_str}** ({longitud} caracteres, con caracteres mixtos garantizados).")
