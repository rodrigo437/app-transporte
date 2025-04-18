
import streamlit as st

# Login único
usuarios = {
    "Canella1": {"password": "Canella123"}
}

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

if not st.session_state["logueado"]:
    st.title("Login")
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if user in usuarios and usuarios[user]["password"] == password:
            st.session_state["logueado"] = True
        else:
            st.error("Credenciales incorrectas")
else:
    st.title("Solicitud de transporte")

    # Tarifario limpio
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

    destino = st.selectbox("Selecciona el destino", list(tarifario.keys()))
    tipo_camion = st.radio("Tipo de camión", ["5T", "10T"])

    if destino and tipo_camion:
        datos = tarifario[destino]
        precio = datos["precio_5t"] if tipo_camion == "5T" else datos["precio_10t"]
        km = datos["km"]

        st.subheader("Resumen")
        st.write(f"**Destino:** {destino}")
        st.write(f"**Camión:** {tipo_camion}")
        st.write(f"**Kilometraje estimado:** {km}")
        st.write(f"**Precio estimado:** Q{precio:,.2f}")
