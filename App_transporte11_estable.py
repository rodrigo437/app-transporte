import streamlit as st
from datetime import datetime
import pandas as pd

# Tarifario
tarifario = {
    "Amatitlan": {"km": "LOCAL", "precio_5t": 1200, "precio_10t": 1500},
    "Chimaltenango": {"km": 55, "precio_5t": 1200, "precio_10t": 1400},
    "Escuintla": {"km": 65, "precio_5t": 1300, "precio_10t": 1300}
}

# Inicializar solicitudes si no existe
if "solicitudes" not in st.session_state:
    st.session_state.solicitudes = []

st.title("Formulario de Solicitud de Transporte")

# Formulario
st.markdown("**Bodega origen**")
origen = st.selectbox("Bodega origen", ["Sede Alamos zona seis San Miguel Petapa"])
destino = st.selectbox("Selecciona el destino", list(tarifario.keys()))
tipo_camion = st.selectbox("Tipo de camión", ["5T", "10T"])
precio = tarifario[destino][f"precio_{tipo_camion.lower()}"]
st.markdown(f"**Kilometraje estimado:** {tarifario[destino]['km']} km")
st.markdown(f"**Precio estimado:** Q{precio:,}")

rango_horas = [f"{h:02d}:00" for h in range(4, 22)]
fecha_recoleccion = st.date_input("Fecha de recolección", datetime.now())
hora_recoleccion = st.selectbox("Hora de recolección", rango_horas)
fecha_entrega = st.date_input("Fecha esperada de entrega", datetime.now())
hora_entrega = st.selectbox("Hora esperada de entrega", rango_horas)
comentarios = st.text_area("Observaciones de entrega")

# Botón para registrar
if st.button("Registrar solicitud"):
    nueva = {
        "Origen": origen,
        "Destino": destino,
        "Tipo de camión": tipo_camion,
        "Precio": precio,
        "Fecha recolección": f"{fecha_recoleccion} {hora_recoleccion}",
        "Fecha entrega": f"{fecha_entrega} {hora_entrega}",
        "Observaciones": comentarios
    }
    if not st.session_state.solicitudes or nueva != st.session_state.solicitudes[-1]:
        st.session_state.solicitudes.append(nueva)

# Mostrar resumen
if st.session_state.solicitudes:
    st.subheader("Resumen de solicitudes")
    total_facturado = sum(s['Precio'] for s in st.session_state.solicitudes)
    st.markdown(f"### Monto total facturado: Q{total_facturado:,.2f}")
    for i, solicitud in enumerate(st.session_state.solicitudes, 1):
        estado = solicitud.get("Estado", "Pendiente de asignación")
        titulo = f"[{estado}] Solicitud #{i} - {solicitud['Destino']} ({solicitud['Tipo de camión']})"
        with st.expander(titulo):
            st.markdown(f"""
**Origen:** {solicitud['Origen']}  
**Destino:** {solicitud['Destino']}  
**Tipo de camión:** {solicitud['Tipo de camión']}  
**Precio:** Q{solicitud['Precio']:,}  
**Fecha recolección:** {solicitud['Fecha recolección']}  
**Fecha entrega:** {solicitud['Fecha entrega']}  
**Observaciones:** {solicitud['Observaciones']}  
""")