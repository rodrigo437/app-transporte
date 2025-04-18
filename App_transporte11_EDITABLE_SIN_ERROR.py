import streamlit as st

if "eliminado" in st.session_state and st.session_state.eliminado:
    del st.session_state["eliminado"]
    st.experimental_rerun()

if "inicia_edicion" in st.session_state and st.session_state.inicia_edicion:
    del st.session_state["inicia_edicion"]
    st.experimental_rerun()
from datetime import datetime

import pandas as pd



# Tarifario completo

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



if "solicitudes" not in st.session_state:

    st.session_state.solicitudes = []



st.title("Formulario de Solicitud de Transporte")



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



                st.session_state.editando = i - 1
                st.session_state.inicia_edicion = True
if st.session_state.solicitudes:

    st.subheader("Resumen de solicitudes")

    total_facturado = sum(s['Precio'] for s in st.session_state.solicitudes)

    st.markdown(f"### Monto total facturado: Q{total_facturado:,.2f}")

    for i, solicitud in enumerate(st.session_state.solicitudes, 1):

        estado = solicitud.get("Estado", "Pendiente de asignación")

        titulo = f"[{estado}] Solicitud #{i} - {solicitud['Destino']} ({solicitud['Tipo de camión']})"

        with st.expander(titulo):

            col1, col2 = st.columns(2)
            if col1.button(f"Editar", key=f"editar_{i}"):
                st.session_state.editando = i - 1
            if col2.button(f"Eliminar", key=f"eliminar_{i}"):
                st.session_state.solicitudes.pop(i - 1)
                st.session_state.editando = i - 1
                st.session_state.solicitudes.pop(i - 1)
            st.markdown(f"""

**Origen:** {solicitud['Origen']}  

**Destino:** {solicitud['Destino']}  

**Tipo de camión:** {solicitud['Tipo de camión']}  

**Precio:** Q{solicitud['Precio']:,}  

**Fecha recolección:** {solicitud['Fecha recolección']}  

**Fecha entrega:** {solicitud['Fecha entrega']}  

**Observaciones:** {solicitud['Observaciones']}  

""")