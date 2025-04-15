
import streamlit as st

# Diccionario del tarifario
{
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
    "Amatitlán": {"km": "Local", "precio_5t": 1200, "precio_10t": 1500},
    "Asunción Mita Jutiapa": {"km": 144, "precio_5t": 2300, "precio_10t": 2900},
    "Chimaltenango": {"km": 55, "precio_5t": 1200, "precio_10t": 1400},
    "Chiquimula": {"km": 204, "precio_5t": 3400, "precio_10t": 4500},
    "Ciudad Capital": {"km": "Local", "precio_5t": 1400, "precio_10t": 1200},
    "Cobán": {"km": 223, "precio_5t": 3900, "precio_10t": 4900},
    "El Chal Petén": {"km": 508, "precio_5t": 7500, "precio_10t": 11300},
    "Escuintla": {"km": 65, "precio_5t": 1200, "precio_10t": 1300},
    "Huehuetenango": {"km": 229, "precio_5t": 3953, "precio_10t": 4900},
    "Jalapa": {"km": 129, "precio_5t": 1800, "precio_10t": 2200},
    "La Libertad Petén": {"km": 506, "precio_5t": 9100, "precio_10t": 11132},
    "Malacatán San Marcos": {"km": 295, "precio_5t": 4200, "precio_10t": 6900},
    "Mazatenango": {"km": 164, "precio_5t": 2700, "precio_10t": 3900},
    "Mixco": {"km": "Local", "precio_5t": 1200, "precio_10t": 1200},
    "Pajapita San Marcos": {"km": 263, "precio_5t": 3300, "precio_10t": 4148},
    "Poptún Petén": {"km": 389, "precio_5t": 6750, "precio_10t": 8400},
    "Puerto Barrios": {"km": 302, "precio_5t": 7800, "precio_10t": 6000},
    "Quetzaltenango": {"km": 202, "precio_5t": 2900, "precio_10t": 4800},
    "Quiché": {"km": 259, "precio_5t": 3300, "precio_10t": 3800},
    "Retalhuleu": {"km": 221, "precio_5t": 3300, "precio_10t": 4400},
    "Salamá": {"km": 154, "precio_5t": 2681, "precio_10t": 3388},
    "San Benito": {"km": 494, "precio_5t": 7400, "precio_10t": 10800},
    "San Marcos": {"km": 253, "precio_5t": 3100, "precio_10t": 4530},
    "San Miguel Petapa": {"km": 100, "precio_5t": 1200, "precio_10t": 1200},
    "Santa Lucía Cotzumalguapa": {"km": 100, "precio_5t": 1900, "precio_10t": 1900},
    "Sololá": {"km": 137, "precio_5t": 2740, "precio_10t": 2900},
    "Teculután, Zacapa": {"km": 132, "precio_5t": 2244, "precio_10t": 2904},
    "Totonicapán": {"km": 179, "precio_5t": 3540, "precio_10t": 3600},
    "Villa Nueva": {"km": "Local", "precio_5t": 1200, "precio_10t": 1200},
    "Zona 4 Canella": {"km": "Local", "precio_5t": 1200, "precio_10t": 1200}
}

st.title("Registrar nueva solicitud")

destino = st.selectbox("Destino final", list(tarifario.keys()))
tipo = st.radio("Tipo de camión", ["5T", "10T"])

if destino and tipo:
    datos = tarifario[destino]
    km_texto = "Local" if datos["km"] == "Local" else f"{datos['km']} km"
    precio = datos["precio_5t"] if tipo == "5T" else datos["precio_10t"]
    
    st.markdown(f"**KM estimado:** {km_texto}")
    st.markdown(f"**Precio cliente:** Q{precio}")
