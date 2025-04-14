
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

archivo_csv = "solicitudes.csv"
archivo_estados = "historial_estados.csv"

usuarios = {
    "admin": {"password": "admin123", "rol": "admin"},
    "cliente1": {"password": "cliente123", "rol": "cliente"},
    "piloto1": {"password": "piloto123", "rol": "piloto"}
}

def cargar_df():
    try:
        return pd.read_csv(archivo_csv)
    except:
        return pd.DataFrame()

def guardar_df(df):
    df.to_csv(archivo_csv, index=False)

def cargar_historial():
    try:
        return pd.read_csv(archivo_estados)
    except:
        return pd.DataFrame(columns=["Piloto", "SolicitudID", "Estado", "FechaHora"])

def guardar_historial(df):
    df.to_csv(archivo_estados, index=False)

def calcular_viaticos(km):
    almuerzo = 60
    cena = 60 if km > 50 else 0
    hotel = 225 if km > 250 else 0
    total = almuerzo + cena + hotel
    return almuerzo, cena, hotel, total

def actualizar_estado_piloto(piloto):
    st.title("Panel del Piloto")
    df = cargar_df()
    historial = cargar_historial()
    asignadas = df[df["Piloto"] == piloto]

    if asignadas.empty:
        st.info("No tenés solicitudes asignadas.")
        return

    for idx, row in asignadas.iterrows():
        with st.expander(f"Entrega para {row['Destino']} - Estado: {row['Estado']}"):
            st.write(f"**Bodega de carga:** {row['Cliente']}")
            st.write(f"**Hora de carga:** {row['Hora carga']}")
            st.write(f"**Departamento de entrega:** {row['Destino']}")
            st.write(f"**Cliente de entrega:** {row['Cliente']}")
            st.write(f"**Hora máxima de recepción:** {row['Hora entrega']}")

            # Viáticos
            almuerzo, cena, hotel, total_viaticos = calcular_viaticos(row["KM"])
            st.write(f"**Viáticos asignados:** Q{total_viaticos}")
            st.write(f"- Almuerzo: Q{almuerzo}")
            st.write(f"- Cena: Q{cena}")
            st.write(f"- Hotel: Q{hotel}")

            nuevo_estado = st.radio("Actualizar estado:", ["Cargando", "En ruta", "Producto entregado"], key=f"estado{idx}")
            if st.button(f"Guardar estado #{idx}"):
                df.at[idx, "Estado"] = nuevo_estado
                guardar_df(df)

                nueva_entrada = pd.DataFrame([{
                    "Piloto": piloto,
                    "SolicitudID": idx,
                    "Estado": nuevo_estado,
                    "FechaHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                historial = pd.concat([historial, nueva_entrada], ignore_index=True)
                guardar_historial(historial)
                st.success("Estado actualizado y guardado en cronología.")

def historial_entregas_piloto(piloto):
    st.subheader("Historial de Entregas Finalizadas")
    df = cargar_df()
    finalizadas = df[(df["Piloto"] == piloto) & (df["Estado"] == "Solicitud completada y entregada")]
    if finalizadas.empty:
        st.info("Aún no tenés entregas completadas.")
    else:
        st.dataframe(finalizadas[["Cliente", "Destino", "Hora carga", "Hora entrega", "Fecha solicitud"]])

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
    if st.session_state["rol"] == "piloto":
        actualizar_estado_piloto(st.session_state["usuario"])
        historial_entregas_piloto(st.session_state["usuario"])
    else:
        st.warning("Este módulo está enfocado solo para el piloto.")
    if st.button("Cerrar sesión"):
        st.session_state.clear()
