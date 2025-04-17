
import streamlit as st
from datetime import datetime

# Tarifario actualizado
tarifario = {
    "Amatitlán": {"km": "Local", "precio": 1200},
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

if "solicitudes" not in st.session_state:
    st.session_state["solicitudes"] = []

st.title("Registrar nueva solicitud")

bodega = "Zona 6 de San Miguel Petapa"
st.text_input("Bodega de carga", value=bodega, disabled=True)

fecha_carga = st.date_input("Fecha de carga")
hora_carga = st.time_input("Hora de carga")
fecha_hora_carga = datetime.combine(fecha_carga, hora_carga)

destino = st.selectbox("Destino final", list(tarifario.keys()))
fecha_entrega = st.date_input("Fecha de entrega")
hora_entrega = st.time_input("Hora de entrega")
fecha_hora_entrega = datetime.combine(fecha_entrega, hora_entrega)

comentario = st.text_area("Comentarios adicionales")

datos = tarifario[destino]
km = datos["km"]
precio = datos["precio"]

if st.button("Guardar solicitud"):
    st.session_state["solicitudes"].append({
        "Bodega": bodega,
        "Fecha/Hora Carga": str(fecha_hora_carga),
        "Destino": destino,
        "KM": km,
        "Precio": precio,
        "Fecha/Hora Entrega": str(fecha_hora_entrega),
        "Comentario": comentario
    })
    st.success("Solicitud guardada correctamente.")

# Mostrar solicitudes con expanders
st.subheader("Historial de solicitudes")
total_precio = 0
for i, s in enumerate(st.session_state["solicitudes"], 1):
    with st.expander(f"Solicitud #{i} - {s['Destino']}"):
        for k, v in s.items():
            st.write(f"**{k}**: {v}")
        total_precio += s["Precio"]

st.write(f"**Total facturado:** Q{total_precio}")
