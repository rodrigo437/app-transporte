
import streamlit as st

# Diccionario de usuarios
usuarios = {
    "cliente1": {"password": "cliente123", "rol": "cliente"}
}

# Inicializa el estado de sesión
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False
    st.session_state["usuario"] = ""
    st.session_state["rol"] = ""

# Función de login
def login():
    st.title("Login de Cliente")
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if usuario in usuarios and usuarios[usuario]["password"] == password:
            st.session_state["logueado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["rol"] = usuarios[usuario]["rol"]
        else:
            st.error("Credenciales incorrectas")

# Mostrar login si no está logueado
if not st.session_state["logueado"]:
    login()
    st.stop()



import streamlit as st

st.set_page_config(page_title="Nueva Solicitud", layout="centered")

# Tarifario corregido con 30 destinos, precios iguales si 5T > 10T, y "Local" donde aplica
tarifario = {
    "Amatitlán": {"km": "Local", "precio": 1200},
    "Asuncion Mita Jutiapa": {"km": 144, "precio": 2900},
    "Chimaltenango": {"km": 55, "precio": 1400},
    "Chiquimula": {"km": 204, "precio": 4500},
    "Ciudad Capital": {"km": "Local", "precio": 1200},
    "Cobán": {"km": 223, "precio": 4100},
    "El Chal Peten": {"km": 508, "precio": 11300},
    "Escuintla": {"km": 65, "precio": 1300},
    "Huehuetenango": {"km": 229, "precio": 4900},
    "Jalapa": {"km": 190, "precio": 3000},
    "La Libertad Peten": {"km": 506, "precio": 11132},
    "Malacatán San Marcos": {"km": 295, "precio": 4500},
    "Mazatenango": {"km": 164, "precio": 3300},
    "Mixco": {"km": "Local", "precio": 1200},
    "Pajapita San Marcos": {"km": 263, "precio": 4148},
    "Poptún Peten": {"km": 389, "precio": 6800},
    "Puerto Barrios": {"km": 302, "precio": 6000},
    "Quetzaltenango": {"km": 202, "precio": 3600},
    "Quiché": {"km": 259, "precio": 3800},
    "Retalhuleu": {"km": 231, "precio": 3300},
    "Salamá": {"km": 154, "precio": 3388},
    "San Benito": {"km": 494, "precio": 10800},
    "San Marcos": {"km": 253, "precio": 4400},
    "San Miguel Petapa": {"km": 100, "precio": 1900},
    "Sololá": {"km": 137, "precio": 2900},
    "Teculután, Zacapa": {"km": 132, "precio": 2904},
    "Totonicapán": {"km": 179, "precio": 3600},
    "Villa Nueva": {"km": "Local", "precio": 1200},
    "Zona 4 Canella": {"km": "Local", "precio": 1200},
}


st.title("Registrar nueva solicitud")

st.subheader("Registro de datos de viaje")

bodega_carga = st.text_input("Bodega de carga", value="Zona 6 de San Miguel Petapa")
fecha_hora_carga = st.datetime_input("Fecha y hora de carga")
departamento_destino = st.selectbox("Departamento de destino", list(tarifario.keys()))
fecha_hora_entrega = st.datetime_input("Fecha y hora estimada de entrega")
comentarios = st.text_area("Comentarios adicionales (cliente y especificaciones)")

if "historial_solicitudes" not in st.session_state:
    st.session_state["historial_solicitudes"] = []

if st.button("Guardar solicitud"):
    datos = tarifario[departamento_destino]
    km = datos["km"]
    precio = datos["precio"]
    solicitud = {
        "Bodega de carga": bodega_carga,
        "Fecha y hora de carga": str(fecha_hora_carga),
        "Destino": departamento_destino,
        "Fecha y hora de entrega": str(fecha_hora_entrega),
        "Comentarios": comentarios,
        "KM": km,
        "Precio": precio
    }
    st.session_state["historial_solicitudes"].append(solicitud)
    st.success("Solicitud registrada exitosamente.")

if st.session_state["historial_solicitudes"]:
    st.markdown("### Historial de solicitudes")
    total_precio = 0
    for i, solicitud in enumerate(st.session_state["historial_solicitudes"], 1):
        with st.expander(f"Solicitud #{i} - {solicitud['Destino']}"):
            st.write(f"**Bodega de carga:** {solicitud['Bodega de carga']}")
            st.write(f"**Fecha y hora de carga:** {solicitud['Fecha y hora de carga']}")
            st.write(f"**Destino:** {solicitud['Destino']}")
            st.write(f"**Fecha y hora de entrega:** {solicitud['Fecha y hora de entrega']}")
            st.write(f"**Comentarios:** {solicitud['Comentarios']}")
            st.write(f"**KM estimado:** {solicitud['KM']}")
            st.write(f"**Precio cliente:** Q{solicitud['Precio']}")
            total_precio += solicitud['Precio']

    st.markdown("### Resumen total")
    st.write(f"**Total de solicitudes:** {len(st.session_state['historial_solicitudes'])}")
    st.write(f"**Total cobrado a clientes:** Q{total_precio}")
    st.write(f"**Ganancia estimada (sin ISR ni costos):** Q{total_precio}")

st.subheader("Registro de datos de viaje")

bodega_carga = st.text_input("Bodega de carga", value="Zona 6 de San Miguel Petapa")
hora_carga = st.time_input("Hora de carga")
departamento_destino = st.selectbox("Departamento de destino", list(tarifario.keys()))
hora_entrega = st.time_input("Hora estimada de entrega")
comentarios = st.text_area("Comentarios adicionales (cliente y especificaciones)")

if st.button("Guardar solicitud"):
    st.success("Solicitud registrada exitosamente.")
    st.markdown("### Resumen de solicitud")
    st.write(f"**Bodega de carga:** {bodega_carga}")
    st.write(f"**Hora de carga:** {hora_carga}")
    st.write(f"**Destino:** {departamento_destino}")
    st.write(f"**Hora de entrega:** {hora_entrega}")
    st.write(f"**Comentarios:** {comentarios}")
    datos = tarifario[departamento_destino]
    km = datos["km"]
    precio = datos["precio"]
    st.write(f"**KM estimado:** {km}")
    st.write(f"**Precio cliente:** Q{precio}")


destino = st.selectbox("Destino final", list(tarifario.keys()))
tipo_camion = st.radio("Tipo de camión", ["5T", "10T"])

if destino:
    datos = tarifario[destino]
    km = datos["km"]
    precio = datos["precio"]

    st.markdown(f"**KM estimado:** {km}")
    st.markdown(f"**Precio cliente:** Q{precio}")
