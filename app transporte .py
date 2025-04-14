
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

usuarios = {
    "admin": {"password": "admin123", "rol": "admin"},
    "cliente1": {"password": "cliente123", "rol": "cliente"},
    "piloto1": {"password": "piloto123", "rol": "piloto"},
    "piloto2": {"password": "piloto123", "rol": "piloto"}
}

# Tarifario completo simulado (más departamentos)
tarifario = {
    "Totonicapán": (144, 2300),
    "Santa Lucía Cotzumalguapa": (204, 3400),
    "San Marcos": (65, 1300),
    "Quetzaltenango": (263, 4148),
    "Huehuetenango": (275, 4200),
    "Escuintla": (111, 2150),
    "Jalapa": (157, 2700),
    "Zacapa": (190, 3100),
    "Chiquimula": (200, 3300),
    "Petén": (480, 6000),
    "Izabal": (350, 4900)
}

archivo_csv = "solicitudes.csv"

def cargar_df():
    try:
        return pd.read_csv(archivo_csv)
    except:
        return pd.DataFrame()

def guardar_df(df):
    df.to_csv(archivo_csv, index=False)

def calcular_viaticos(km):
    almuerzo = 60
    cena = 60 if km > 50 else 0
    hotel = 225 if km > 250 else 0
    total = almuerzo + cena + hotel
    return total

def registrar_solicitud(cliente):
    st.subheader("Nueva solicitud de transporte")
    destino = st.selectbox("Destino final", list(tarifario.keys()))
    tipo_camion = st.radio("Tipo de camión", ["5T", "10T"])
    fecha_servicio = st.date_input("Fecha para realizar el viaje")
    hora_carga = st.time_input("Hora de carga")
    fecha_hora_entrega = st.datetime_input("Fecha y hora máxima de entrega")

    km = tarifario[destino][0]
    precio = tarifario[destino][1] if tipo_camion == "5T" else tarifario[destino][1] + 500
    km_total = km * 2
    combustible = km_total / 10 * 30
    viaticos = calcular_viaticos(km)
    total_servicio = precio

    if st.button("Enviar solicitud"):
        df = cargar_df()
        nueva = {
            "Cliente": cliente,
            "Destino": destino,
            "Tipo": tipo_camion,
            "Fecha servicio": fecha_servicio,
            "Hora carga": hora_carga.strftime('%H:%M'),
            "Fecha y hora entrega": fecha_hora_entrega.strftime('%Y-%m-%d %H:%M'),
            "Precio": total_servicio,
            "Viáticos": viaticos,
            "Combustible": combustible,
            "Estado": "Solicitud en proceso"
        }
        df = pd.concat([df, pd.DataFrame([nueva])], ignore_index=True)
        guardar_df(df)
        st.success("Solicitud registrada correctamente.")

def historial_cliente(cliente):
    st.subheader("Mis solicitudes")
    df = cargar_df()
    df_cliente = df[df["Cliente"] == cliente]
    if df_cliente.empty:
        st.info("No tenés solicitudes registradas.")
    else:
        for idx, row in df_cliente.iterrows():
            with st.expander(f"{row['Destino']} - Estado: {row['Estado']}"):
                st.write(f"Destino: {row['Destino']}")
                st.write(f"Tipo camión: {row['Tipo']}")
                st.write(f"Fecha del viaje: {row['Fecha servicio']}")
                st.write(f"Hora carga: {row['Hora carga']}")
                st.write(f"Hora máxima de entrega: {row['Fecha y hora entrega']}")
                st.write(f"Precio total del viaje: Q{row['Precio']}")
                if row["Estado"] == "Solicitud en proceso":
                    if st.button(f"Eliminar solicitud #{idx}"):
                        df.drop(index=idx, inplace=True)
                        guardar_df(df)
                        st.success("Solicitud eliminada.")
                        st.experimental_rerun()
                else:
                    st.info("No se puede eliminar esta solicitud.")

def login():
    st.title("Login")
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if usuario in usuarios and usuarios[usuario]["password"] == password:
            st.session_state["logueado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["rol"] = usuarios[usuario]["rol"]
        else:
            st.error("Credenciales incorrectas.")

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

if not st.session_state["logueado"]:
    login()
else:
    rol = st.session_state["rol"]
    user = st.session_state["usuario"]
    if rol == "cliente":
        registrar_solicitud(user)
        historial_cliente(user)
    if st.button("Cerrar sesión"):
        st.session_state.clear()
