
import streamlit as st

# --- Autenticación ---
def login():
    st.title("Inicio de sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        if username == "Canella1" and password == "Canella123":
            st.session_state["authenticated"] = True
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()
# --- Fin de autenticación ---

# --- Funcionalidad posterior al login ---
import pandas as pd
from datetime import datetime, time

if "solicitudes" not in st.session_state:
    st.session_state["solicitudes"] = []

st.title("Registro de Solicitudes de Transporte")

# 1. Origen predeterminado
origen = st.text_input("Origen", value="Álamos, Zona 6, San Miguel Petapa")

# 2. Fecha y hora de recolección
fecha_recoleccion = st.date_input("Fecha de recolección", value=datetime.today())
hora_recoleccion = st.time_input("Hora de recolección", value=time(4, 0), step=900)

# 3. Fecha y hora esperada de entrega
fecha_entrega = st.date_input("Fecha esperada de entrega", value=datetime.today())
hora_entrega = st.time_input("Hora esperada de entrega", value=time(4, 0), step=900)

# 4. Comentarios
comentarios = st.text_area("Observaciones de entrega")

# 5. Botón para registrar solicitud
if st.button("Registrar solicitud"):
    nueva_solicitud = {
        "Origen": origen,
        "Fecha Recolección": fecha_recoleccion.strftime("%Y-%m-%d") + " " + hora_recoleccion.strftime("%H:%M"),
        "Fecha Entrega": fecha_entrega.strftime("%Y-%m-%d") + " " + hora_entrega.strftime("%H:%M"),
        "Comentarios": comentarios,
        "Costo (Q)": 500  # Costo fijo temporal
    }
    st.session_state["solicitudes"].append(nueva_solicitud)
    st.success("Solicitud registrada con éxito.")

# 6. Resumen de solicitudes
if st.session_state["solicitudes"]:
    df = pd.DataFrame(st.session_state["solicitudes"])
    st.subheader("Resumen de solicitudes")
    st.dataframe(df)

    # 7. Total en quetzales
    total = sum(item["Costo (Q)"] for item in st.session_state["solicitudes"])
    st.markdown(f"### Total acumulado: Q{total:,.2f}")

    # 8. Calendario
    st.subheader("Calendario de entregas")
    calendar_df = df[["Fecha Recolección", "Fecha Entrega"]].copy()
    calendar_df["Evento"] = "Entrega"
    calendar_df = calendar_df.rename(columns={"Fecha Entrega": "Fecha"})
    calendar_df = calendar_df[["Fecha", "Evento"]]
    st.dataframe(calendar_df)
# --- Fin de funcionalidad posterior al login ---




import streamlit as st

# Tarifario completo con 30 destinos, km, precios 5T y 10T
tarifario = {
    "Amatitlan": {"km": "LOCAL", "precio_5t": 1200, "precio_10t": 1500},
    "Asuncion Mita Jutiapa": {"km": 144, "precio_5t": 2300, "precio_10t": 2900},
    "Chimaltenango": {"km": 55, "precio_5t": 1200, "precio_10t": 1400},
    "Chiquimula": {"km": 204, "precio_5t": 3400, "precio_10t": 4500},
    "Ciudad Capital": {"km": "LOCAL", "precio_5t": 1200, "precio_10t": 1200},
    "Coban": {"km": 223, "precio_5t": 4000, "precio_10t": 4000},
    "El Chal Peten": {"km": 508, "precio_5t": 7500, "precio_10t": 11300},
    "Escuintla": {"km": 65, "precio_5t": 1300, "precio_10t": 1300},
    "Huehuetenango": {"km": 229, "precio_5t": 3893, "precio_10t": 4900},
    "Jalapa": {"km": 109, "precio_5t": 1853, "precio_10t": 1853},
    "La Libertad Peten": {"km": 506, "precio_5t": 10120, "precio_10t": 11132},
    "Malacatan San Marcos": {"km": 295, "precio_5t": 4500, "precio_10t": 4500},
    "Mazatenango": {"km": 164, "precio_5t": 2400, "precio_10t": 2400},
    "Mixco": {"km": "LOCAL", "precio_5t": 1200, "precio_10t": 1200},
    "Pajapita San Marcos": {"km": 263, "precio_5t": 4148, "precio_10t": 4148},
    "Poptun Peten": {"km": 389, "precio_5t": 7780, "precio_10t": 8000},
    "Puerto Barrios": {"km": 302, "precio_5t": 5085, "precio_10t": 6000},
    "Quetzaltenango": {"km": 203, "precio_5t": 3400, "precio_10t": 3500},
    "Quiche": {"km": 259, "precio_5t": 3300, "precio_10t": 4100},
    "Retalhuleu": {"km": 211, "precio_5t": 3281, "precio_10t": 4100},
    "Salama": {"km": 154, "precio_5t": 2681, "precio_10t": 3388},
    "San Benito": {"km": 494, "precio_5t": 10000, "precio_10t": 10800},
    "San Marcos": {"km": 253, "precio_5t": 4301, "precio_10t": 4800},
    "San Miguel Petapa": {"km": "LOCAL", "precio_5t": 1100, "precio_10t": 1200},
    "Santa Lucia Cotzumalguapa": {"km": 100, "precio_5t": 1900, "precio_10t": 1900},
    "Solola": {"km": 137, "precio_5t": 2740, "precio_10t": 2900},
    "Teculutan, Zacapa": {"km": 132, "precio_5t": 2244, "precio_10t": 2904},
    "Totonicapan": {"km": 179, "precio_5t": 3540, "precio_10t": 3600},
    "Villa Nueva": {"km": "LOCAL", "precio_5t": 1200, "precio_10t": 1200},
    "Zona 4 Canella": {"km": "LOCAL", "precio_5t": 1200, "precio_10t": 1200}
}

# Título de la app
st.title("Solicitud de Transporte")

# Paso 1: Origen predeterminado
origen = "Zona 6 San Miguel Petapa"
st.markdown(f"**Origen predeterminado:** {origen}")

# Paso 2: Destino a elegir
destino = st.selectbox("Selecciona el destino", list(tarifario.keys()))

# Paso 3: Selección de camión
tipo_camion = st.radio("Selecciona el tipo de camión", ["5T", "10T"])

# Paso 4: Resumen de selección
if destino:
    datos = tarifario.get(destino)
    km = datos["km"]
    precio = datos["precio_5t"] if tipo_camion == "5T" else datos["precio_10t"]

    st.subheader("Resumen de solicitud")
    st.write(f"**Origen:** {origen}")
    st.write(f"**Destino:** {destino}")
    st.write(f"**Kilometraje estimado:** {km}")
    st.write(f"**Precio estimado ({tipo_camion}):** Q{precio:,.2f}")
