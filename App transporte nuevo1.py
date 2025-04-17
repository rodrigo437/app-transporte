
import streamlit as st
from datetime import datetime

# Estados posibles
estados = [
    "Pendiente de asignación",
    "Asignada y programada para recolección",
    "Cargando",
    "En proceso de entrega",
    "Descargando",
    "Orden entregada"
]

# Tarifario actualizado con precios diferentes para 5T y 10T
tarifario = {
    "Amatitlán": {"km": "Local", "precio_5t": 1200, "precio_10t": 1500},
    "Asuncion Mita Jutiapa": {"km": 144, "precio_5t": 2300, "precio_10t": 2900},
    "Chimaltenango": {"km": 55, "precio_5t": 1200, "precio_10t": 1400},
    "Chiquimula": {"km": 204, "precio_5t": 3400, "precio_10t": 4500},
    "Ciudad Capital": {"km": "Local", "precio_5t": 1100, "precio_10t": 1200},
    "Cobán": {"km": 223, "precio_5t": 4400, "precio_10t": 4400},
    "El Chal Petén": {"km": 508, "precio_5t": 7500, "precio_10t": 11300},
    "Escuintla": {"km": 65, "precio_5t": 1300, "precio_10t": 1300},
    "Huehuetenango": {"km": 229, "precio_5t": 3893, "precio_10t": 4900},
    "Jalapa": {"km": 109, "precio_5t": 1853, "precio_10t": 1853},
    "La Libertad Petén": {"km": 506, "precio_5t": 10120, "precio_10t": 11132},
    "Malacatán San Marcos": {"km": 295, "precio_5t": 4500, "precio_10t": 4500},
    "Mazatenango": {"km": 164, "precio_5t": 2400, "precio_10t": 2400},
    "Mixco": {"km": "Local", "precio_5t": 1200, "precio_10t": 1200},
    "Pajapita San Marcos": {"km": 263, "precio_5t": 4148, "precio_10t": 4148},
    "Poptún Petén": {"km": 389, "precio_5t": 7780, "precio_10t": 8000},
    "Puerto Barrios": {"km": 302, "precio_5t": 5085, "precio_10t": 6000},
    "Quetzaltenango": {"km": 203, "precio_5t": 3400, "precio_10t": 3500},
    "Quiché": {"km": 259, "precio_5t": 3300, "precio_10t": 3800},
    "Retalhuleu": {"km": 211, "precio_5t": 3281, "precio_10t": 4100},
    "Salamá": {"km": 154, "precio_5t": 2681, "precio_10t": 3388},
    "San Benito": {"km": 494, "precio_5t": 10000, "precio_10t": 10800},
    "San Marcos": {"km": 253, "precio_5t": 4301, "precio_10t": 4800},
    "San Miguel Petapa": {"km": "Local", "precio_5t": 1100, "precio_10t": 1200},
    "Sololá": {"km": 100, "precio_5t": 1900, "precio_10t": 1900},
    "Teculután, Zacapa": {"km": 137, "precio_5t": 2740, "precio_10t": 2900},
    "Totonicapán": {"km": 132, "precio_5t": 2244, "precio_10t": 2904},
    "Villa Nueva": {"km": 179, "precio_5t": 3540, "precio_10t": 3600},
    "Zona 4 Canella": {"km": "Local", "precio_5t": 1200, "precio_10t": 1200}
}

if "solicitudes" not in st.session_state:
    st.session_state["solicitudes"] = []

st.title("Registro de solicitud de transporte")

def mostrar_guia_estados(estado_actual):
    st.markdown("### Guía de estados del servicio")
    for estado in estados:
        if estado == estado_actual:
            st.markdown(f"- :green[**{estado}**] ← Estado actual")
        else:
            st.markdown(f"- {estado}")

# Formulario
bodega = st.selectbox("Bodega de carga", ["Zona 6 Álamos, San Miguel Petapa"])
destino = st.selectbox("Destino", list(tarifario.keys()))
tipo = st.radio("Tipo de camión", ["5T", "10T"])
comentario = st.text_area("Comentarios adicionales")

fecha_carga = st.date_input("Fecha de carga")
hora_carga = st.time_input("Hora de carga")
fecha_entrega = st.date_input("Fecha de entrega")
hora_entrega = st.time_input("Hora de entrega")
fh_carga = datetime.combine(fecha_carga, hora_carga)
fh_entrega = datetime.combine(fecha_entrega, hora_entrega)

# Obtener precio por tipo
km = tarifario[destino]["km"]
precio = tarifario[destino][f"precio_{tipo.lower()}"]

st.write(f"**KM estimado:** {km}")
st.write(f"**Precio estimado ({tipo}):** Q{precio}")

if st.button("Registrar solicitud"):
    nueva = {
        "bodega": bodega,
        "tipo": tipo,
        "destino": destino,
        "comentario": comentario,
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "carga": fh_carga.strftime("%Y-%m-%d %H:%M:%S"),
        "entrega": fh_entrega.strftime("%Y-%m-%d %H:%M:%S"),
        "km": km,
        "precio": precio,
        "estado_actual": estados[0],
        "historial_estados": {estados[0]: datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    }
    st.session_state["solicitudes"].append(nueva)
    st.success("Solicitud registrada correctamente.")

st.subheader("Solicitudes registradas")
for i, s in enumerate(st.session_state["solicitudes"]):
    with st.expander(f"Solicitud #{i + 1} - {s['destino']}"):
        st.write(f"**Bodega:** {s['bodega']}")
        st.write(f"**Tipo de camión:** {s['tipo']}")
        st.write(f"**Fecha creación:** {s['fecha_creacion']}")
        st.write(f"**Fecha/Hora carga:** {s['carga']}")
        st.write(f"**Fecha/Hora entrega:** {s['entrega']}")
        st.write(f"**KM estimado:** {s['km']}")
        st.write(f"**Precio:** Q{s['precio']}")
        st.write(f"**Comentario:** {s['comentario']}")
        st.markdown(f"**Estado actual:** :green[{s['estado_actual']}]")
        mostrar_guia_estados(s["estado_actual"])
        if s["estado_actual"] != estados[-1]:
            siguiente = estados[estados.index(s["estado_actual"]) + 1]
            if st.button(f"Avanzar a: {siguiente}", key=f"avanza_{i}"):
                s["estado_actual"] = siguiente
                s["historial_estados"][siguiente] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.experimental_rerun()

        st.markdown("**Historial de estados:**")
        for est, f in s["historial_estados"].items():
            st.write(f"- {est}: {f}")
