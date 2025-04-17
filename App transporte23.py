
import streamlit as st
from datetime import datetime

# Lista de estados en orden secuencial
estados = [
    "Pendiente de asignación",
    "Asignada y programada para recolección",
    "Cargando",
    "En proceso de entrega",
    "Descargando",
    "Orden entregada"
]

# Inicialización del historial
if "solicitudes" not in st.session_state:
    st.session_state["solicitudes"] = []

st.title("Gestión de estados de solicitud")

# Formulario de registro básico
cliente = st.text_input("Nombre del cliente")
destino = st.text_input("Destino del envío")
comentario = st.text_area("Comentarios adicionales")

if st.button("Registrar nueva solicitud"):
    nueva = {
        "cliente": cliente,
        "destino": destino,
        "comentario": comentario,
        "estado_actual": estados[0],
        "historial_estados": {estados[0]: datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    }
    st.session_state["solicitudes"].append(nueva)
    st.success("Solicitud registrada como Pendiente de asignación.")

# Mostrar solicitudes con botones para cambiar de estado
st.subheader("Solicitudes registradas")
for i, solicitud in enumerate(st.session_state["solicitudes"]):
    with st.expander(f"Solicitud #{i + 1} - {solicitud['cliente']} → {solicitud['destino']}"):
        st.markdown(f"**Comentario:** {solicitud['comentario']}")
        st.markdown(f"**Estado actual:** :green[{solicitud['estado_actual']}]")
        
        if solicitud['estado_actual'] != estados[-1]:
            siguiente_estado = estados[estados.index(solicitud['estado_actual']) + 1]
            if st.button(f"Avanzar a: {siguiente_estado}", key=f"avance_{i}"):
                solicitud["estado_actual"] = siguiente_estado
                solicitud["historial_estados"][siguiente_estado] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.experimental_rerun()

        # Mostrar historial
        st.markdown("**Historial de estados:**")
        for estado, fecha in solicitud["historial_estados"].items():
            st.write(f"- {estado}: {fecha}")
