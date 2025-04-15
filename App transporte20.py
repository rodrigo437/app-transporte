
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

destino = st.selectbox("Destino final", list(tarifario.keys()))
tipo_camion = st.radio("Tipo de camión", ["5T", "10T"])

if destino:
    datos = tarifario[destino]
    km = datos["km"]
    precio = datos["precio"]

    st.markdown(f"**KM estimado:** {km}")
    st.markdown(f"**Precio cliente:** Q{precio}")
