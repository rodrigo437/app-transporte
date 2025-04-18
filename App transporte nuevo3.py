
import streamlit as st
from datetime import datetime

# Lista de estados
estados = [
    "Pendiente de asignación",
    "Asignada y programada para recolección",
    "Cargando",
    "En proceso de entrega",
    "Descargando",
    "Orden entregada"
]

# Tarifario con 30 destinos
tarifario = {
    "AMATITLAN": {"km": "LOCAL", "precio_5t": "Q1,200.00", "precio_10t": "Q1,500.00"},
    "ASUNCION MITA JUTIAPA": {"km": "144", "precio_5t": "Q2,300.00", "precio_10t": "Q2,900.00"},
    "CHIMALTENANGO": {"km": "55", "precio_5t": "Q1,200.00", "precio_10t": "Q1,400.00"},
    "CHIQUIMULA": {"km": "204", "precio_5t": "Q3,400.00", "precio_10t": "Q4,500.00"},
    "CIUDAD CAPITAL": {"km": "LOCAL", "precio_5t": "Q1,400.00", "precio_10t": "Q1,200.00"},
    "COBAN": {"km": "223", "precio_5t": "Q4,000.00", "precio_10t": "Q4,000.00"},
    "EL CHAL PETEN": {"km": "508", "precio_5t": "Q7,500.00", "precio_10t": "Q11,300.00"},
    "ESCUINTLA": {"km": "65", "precio_5t": "Q1,300.00", "precio_10t": "Q1,300.00"},
    "HUEHUETENANGO": {"km": "229", "precio_5t": "Q3,893.00", "precio_10t": "Q4,900.00"},
    "JALAPA": {"km": "109", "precio_5t": "Q1,853.00", "precio_10t": "Q1,853.00"},
    "LA LIBERTAD PETEN": {"km": "506", "precio_5t": "Q10,120.00", "precio_10t": "Q11,132.00"},
    "MALACATAN SAN MARCOS": {"km": "295", "precio_5t": "Q4,500.00", "precio_10t": "Q4,500.00"},
    "MAZATENANGO": {"km": "164", "precio_5t": "Q2,400.00", "precio_10t": "Q2,400.00"},
    "MIXCO": {"km": "LOCAL", "precio_5t": "Q1,200.00", "precio_10t": "Q1,200.00"},
    "PAJAPITA SAN MARCOS": {"km": "263", "precio_5t": "Q4,148.00", "precio_10t": "Q4,148.00"},
    "POPTUN PETEN": {"km": "389", "precio_5t": "Q7,780.00", "precio_10t": "Q8,000.00"},
    "PUERTO BARRIOS": {"km": "302", "precio_5t": "Q5,085.00", "precio_10t": "Q6,000.00"},
    "QUETZALTENANGO": {"km": "203", "precio_5t": "Q3,400.00", "precio_10t": "Q3,500.00"},
    "QUICHE": {"km": "259", "precio_5t": "Q3,800.00", "precio_10t": "Q4,000.00"},
    "RETALHULEU": {"km": "211", "precio_5t": "Q3,281.00", "precio_10t": "Q4,100.00"},
    "SALAMA": {"km": "154", "precio_5t": "Q2,681.00", "precio_10t": "Q3,388.00"},
    "SAN BENITO": {"km": "494", "precio_5t": "Q10,000.00", "precio_10t": "Q10,800.00"},
    "SAN MARCOS": {"km": "253", "precio_5t": "Q4,301.00", "precio_10t": "Q4,800.00"},
    "SAN MIGUEL PETAPA": {"km": "LOCAL", "precio_5t": "Q1,100.00", "precio_10t": "Q1,200.00"},
    "SANTA LUCIA COTZUMALGUAPA": {"km": "100", "precio_5t": "Q1,900.00", "precio_10t": "Q1,900.00"},
    "SOLOLA": {"km": "137", "precio_5t": "Q2,740.00", "precio_10t": "Q2,900.00"},
    "TECULUTAN, ZACAPA": {"km": "132", "precio_5t": "Q2,244.00", "precio_10t": "Q2,904.00"},
    "TOTONICAPAN": {"km": "179", "precio_5t": "Q3,540.00", "precio_10t": "Q3,600.00"},
    "VILLA NUEVA": {"km": "LOCAL", "precio_5t": "Q1,200.00", "precio_10t": "Q1,200.00"},
    "ZONA 4 CANELLA": {"km": "LOCAL", "precio_5t": "Q1,200.00", "precio_10t": "Q1,200.00"}
},
    "Asuncion Mita Jutiapa": {"km": 144, "precio": 2900},
    "Chimaltenango": {"km": 55, "precio": 1400},
    "Chiquimula": {"km": 204, "precio": 4500},
    "Ciudad Capital": {"km": "Local", "precio": 1200},
    "Cobán": {"km": 223, "precio": 3600},
    "El Chal Petén": {"km": 508, "precio": 11300},
    "Escuintla": {"km": 65, "precio": 1300},
    "Huehuetenango": {"km": 229, "precio": 4900},
    "Jalapa": {"km": 190, "precio": 3900},
    "La Libertad Petén": {"km": 506, "precio": 11132},
    "Malacatán San Marcos": {"km": 295, "precio": 4100},
    "Mazatenango": {"km": 164, "precio": 2900},
    "Mixco": {"km": "Local", "precio": 1200},
    "Pajapita San Marcos": {"km": 263, "precio": 4148},
    "Poptún Petén": {"km": 389, "precio": 9500},
    "Puerto Barrios": {"km": 302, "precio": 6000},
    "Quetzaltenango": {"km": 206, "precio": 3800},
    "Quiché": {"km": 259, "precio": 3600},
    "Retalhuleu": {"km": 214, "precio": 3600},
    "Salamá": {"km": 154, "precio": 3388},
    "San Benito": {"km": 494, "precio": 10800},
    "San Marcos": {"km": 253, "precio": 3900},
    "San Miguel Petapa": {"km": 100, "precio": 1900},
    "Sololá": {"km": 137, "precio": 2900},
    "Teculután, Zacapa": {"km": 132, "precio": 2904},
    "Totonicapán": {"km": 179, "precio": 3600},
    "Villa Nueva": {"km": "Local", "precio": 1200},
    "Zona 4 Canella": {"km": "Local", "precio": 1200}
}

# Inicializar solicitudes
if "solicitudes" not in st.session_state:
    st.session_state["solicitudes"] = []

st.title("Registro y seguimiento de solicitudes")

def mostrar_guia_estados(estado_actual):
    st.markdown("### Guía de estados del servicio")
    for estado in estados:
        if estado == estado_actual:
            st.markdown(f"- :green[**{estado}**] ← Estado actual")
        else:
            st.markdown(f"- {estado}")

# Formulario del cliente
cliente = st.selectbox("Bodega de carga", ["Zona 6 Álamos, San Miguel Petapa"])
destino = st.selectbox("Destino", list(tarifario.keys()))
comentario = st.text_area("Comentarios adicionales")

fecha_carga = st.date_input("Fecha de carga")
hora_carga = st.time_input("Hora de carga")
fecha_hora_carga = datetime.combine(fecha_carga, hora_carga)

fecha_entrega = st.date_input("Fecha de entrega")
hora_entrega = st.time_input("Hora de entrega")
fecha_hora_entrega = datetime.combine(fecha_entrega, hora_entrega)

tipo_camion = st.radio("Tipo de camión", ["5T", "10T"])

# Obtener datos del tarifario
km = tarifario[destino]["km"]
precio = tarifario[destino]["precio"]

st.write(f"**KM estimado:** {km}")
st.write(f"**Precio estimado:** Q{precio}")

# Guardar solicitud
if st.button("Registrar solicitud"):
    ahora = datetime.now()
    nueva = {
        "cliente": cliente,
        "destino": destino,
        "comentario": comentario,
        "fecha_creacion": ahora.strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_hora_carga": fecha_hora_carga.strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_hora_entrega": fecha_hora_entrega.strftime("%Y-%m-%d %H:%M:%S"),
        "km": km,
        "tipo_camion": tipo_camion,
        "precio": precio,
        "estado_actual": estados[0],
        "historial_estados": {estados[0]: ahora.strftime("%Y-%m-%d %H:%M:%S")}
    }
    st.session_state["solicitudes"].append(nueva)
    st.success("Solicitud registrada correctamente.")

# Mostrar resumen de solicitudes
st.subheader("Solicitudes registradas")
for i, s in enumerate(st.session_state["solicitudes"]):
    with st.expander(f"Solicitud #{i+1} - {s['cliente']} → {s['destino']}"):
        st.write(f"**Fecha de creación:** {s['fecha_creacion']}")
        st.write(f"**Fecha/Hora de carga:** {s['fecha_hora_carga']}")
        st.write(f"**Fecha/Hora de entrega:** {s['fecha_hora_entrega']}")
        st.write(f"**Comentario:** {s['comentario']}")
        st.write(f"**KM estimado:** {s['km']}")
        st.write(f"**Tipo de camión:** {s['tipo_camion']}")
        st.write(f"**Precio estimado:** Q{s['precio']}")
        st.write(f"**Estado actual:** :green[{s['estado_actual']}]")

        mostrar_guia_estados(s['estado_actual'])

        if s['estado_actual'] != estados[-1]:
            siguiente_estado = estados[estados.index(s['estado_actual']) + 1]
            if st.button(f"Avanzar a: {siguiente_estado}", key=f"estado_{i}"):
                s["estado_actual"] = siguiente_estado
                s["historial_estados"][siguiente_estado] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.experimental_rerun()

        st.markdown("**Historial de estados:**")
        for estado, fecha in s["historial_estados"].items():
            st.write(f"- {estado}: {fecha}")
