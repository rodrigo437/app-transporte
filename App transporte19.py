
import streamlit as st

tarifario = {
    "Amatitlán": {"km": "Local", "precio_5t": 1200, "precio_10t": 1500},
    "Asuncion Mita Jutiapa": {"km": 144, "precio_5t": 2300, "precio_10t": 2900},
    "Chimaltenango": {"km": 55, "precio_5t": 1200, "precio_10t": 1400},
    "Chiquimula": {"km": 204, "precio_5t": 4500, "precio_10t": 4500},
    "Ciudad Capital": {"km": "Local", "precio_5t": 1200, "precio_10t": 1200},
    "Cobán": {"km": 223, "precio_5t": 4200, "precio_10t": 4800},
    "El Chal Petén": {"km": 508, "precio_5t": 7500, "precio_10t": 11300},
    "Escuintla": {"km": 65, "precio_5t": 1300, "precio_10t": 1300},
    "Huehuetenango": {"km": 229, "precio_5t": 3953, "precio_10t": 4900},
    "Jalapa": {"km": 199, "precio_5t": 2800, "precio_10t": 4000},
    "La Libertad Petén": {"km": 506, "precio_5t": 9000, "precio_10t": 11132},
    "Malacatán San Marcos": {"km": 295, "precio_5t": 4200, "precio_10t": 6300},
    "Mazatenango": {"km": 164, "precio_5t": 2400, "precio_10t": 2900},
    "Mixco": {"km": "Local", "precio_5t": 1200, "precio_10t": 1200},
    "Pajapita San Marcos": {"km": 263, "precio_5t": 3200, "precio_10t": 4148},
    "Poptún Petén": {"km": 389, "precio_5t": 6000, "precio_10t": 9000},
    "Puerto Barrios": {"km": 302, "precio_5t": 6000, "precio_10t": 6000},
    "Quetzaltenango": {"km": 206, "precio_5t": 4000, "precio_10t": 4500},
    "Quiché": {"km": 259, "precio_5t": 3300, "precio_10t": 3800},
    "Retalhuleu": {"km": 211, "precio_5t": 3480, "precio_10t": 3880},
    "Salamá": {"km": 154, "precio_5t": 2681, "precio_10t": 3388},
    "San Benito": {"km": 494, "precio_5t": 6000, "precio_10t": 10800},
    "San Marcos": {"km": 253, "precio_5t": 2100, "precio_10t": 3900},
    "San Miguel Petapa": {"km": 100, "precio_5t": 1200, "precio_10t": 1200},
    "Sololá": {"km": 137, "precio_5t": 2740, "precio_10t": 2900},
    "Teculután, Zacapa": {"km": 132, "precio_5t": 2244, "precio_10t": 2904},
    "Totonicapán": {"km": 179, "precio_5t": 3540, "precio_10t": 3600},
    "Villa Nueva": {"km": "Local", "precio_5t": 1200, "precio_10t": 1200},
    "Zona 4 Canella": {"km": "Local", "precio_5t": 1200, "precio_10t": 1200}
}

st.set_page_config(page_title="Formulario Cliente", layout="centered")
st.title("Solicitud de Transporte")

destino = st.selectbox("Selecciona el destino", list(tarifario.keys()))
tipo_camion = st.radio("Selecciona tipo de camión", ["5T", "10T"])

if destino and tipo_camion:
    datos = tarifario[destino]
    km = datos["km"]
    precio = datos["precio_5t"] if tipo_camion == "5T" else datos["precio_10t"]

    st.markdown("### Resumen del servicio")
    st.write(f"**Kilometraje estimado:** {'Local' if km == 'Local' else str(km) + ' km'}")
    st.write(f"**Precio estimado:** Q{precio}")
    if km != "Local":
        st.write(f"**Resumen:** {km} km – Q{precio}")
    else:
        st.write(f"**Resumen:** Local – Q{precio}")
