
import streamlit as st
import pandas as pd
from datetime import datetime

# Base de datos de usuarios
usuarios = {
    "cliente": {"password": "cliente123", "rol": "cliente"},
    "piloto": {"password": "piloto123", "rol": "piloto"},
    "admin": {"password": "admin123", "rol": "admin"},
}

# Estados definidos para cada solicitud
estados = [
    "Pendiente de asignación",
    "Asignada y programada para recolección",
    "Cargando",
    "En proceso de entrega",
    "Descargando",
    "Orden entregada"
]

# Tarifario
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

# Archivo para guardar solicitudes
archivo_csv = "solicitudes_transportes.csv"

def cargar_solicitudes():
    try:
        return pd.read_csv(archivo_csv)
    except:
        return pd.DataFrame()

def guardar_solicitudes(df):
    df.to_csv(archivo_csv, index=False)

# Pantalla de login
def login():
    st.title("Login")
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if user in usuarios and usuarios[user]["password"] == password:
            st.session_state["usuario"] = user
            st.session_state["rol"] = usuarios[user]["rol"]
            st.session_state["logueado"] = True
        else:
            st.error("Credenciales incorrectas")

# Inicializar sesión
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False


# ====================== MÓDULO CLIENTE ======================
def modulo_cliente():
    st.header("Solicitud de Transporte - Cliente")

    df = cargar_solicitudes()

    st.markdown("### Crear nueva solicitud")

    origen = "Zona 6 Álamos San Miguel Petapa"
    destino = st.selectbox("Destino final", list(tarifario.keys()))
    tipo_camion = st.radio("Tipo de camión", ["5T", "10T"])
    fecha_hora_carga = st.datetime_input("Fecha y hora de carga")
    fecha_hora_entrega = st.datetime_input("Fecha y hora de entrega")

    if st.button("Confirmar solicitud"):
        datos = tarifario.get(destino)
        km = datos["km"]
        precio = datos["precio_5t"] if tipo_camion == "5T" else datos["precio_10t"]
        fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        nueva = {
            "Usuario": st.session_state["usuario"],
            "Fecha creación": fecha_creacion,
            "Origen": origen,
            "Destino": destino,
            "Camión": tipo_camion,
            "KM": km,
            "Precio": precio,
            "Fecha carga": fecha_hora_carga,
            "Fecha entrega": fecha_hora_entrega,
            "Estado": "Pendiente de asignación",
            "Historial": f"Pendiente de asignación - {fecha_creacion}"
        }

        df = df._append(nueva, ignore_index=True)
        guardar_solicitudes(df)
        st.success("Solicitud registrada correctamente")

    st.markdown("### Historial de solicitudes")

    df = df[df["Usuario"] == st.session_state["usuario"]]
    if not df.empty:
        for i, row in df.iterrows():
            with st.expander(f"{row['Destino']} ({row['Estado']})"):
                st.write(f"**Origen:** {row['Origen']}")
                st.write(f"**Camión:** {row['Camión']}")
                st.write(f"**Kilometraje:** {row['KM']}")
                st.write(f"**Precio:** Q{row['Precio']:,.2f}")
                st.write(f"**Carga:** {row['Fecha carga']}")
                st.write(f"**Entrega:** {row['Fecha entrega']}")
                st.markdown(f"**Historial:** {row['Historial']}")
    else:
        st.info("No hay solicitudes registradas.")

# ====================== INTERFAZ PRINCIPAL ======================
if st.session_state["logueado"]:
    st.sidebar.success(f"Bienvenido, {st.session_state['usuario'].capitalize()}")

    if st.session_state["rol"] == "cliente":
        modulo_cliente()
    else:
        st.info("Este usuario aún no tiene módulos implementados.")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.clear()
else:
    login()
