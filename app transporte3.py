
import streamlit as st
import pandas as pd
from datetime import datetime

usuarios = {
    "admin": {"password": "admin123", "rol": "admin"},
    "cliente1": {"password": "cliente123", "rol": "cliente"},
    "piloto1": {"password": "piloto123", "rol": "piloto"},
    "piloto2": {"password": "piloto123", "rol": "piloto"}
}

archivo_csv = "solicitudes.csv"
estados = ["Pendiente de asignación", "Solicitud asignada", "Unidad cargada y en curso", "Carga entregada"]

def cargar_df():
    try:
        return pd.read_csv(archivo_csv)
    except:
        return pd.DataFrame()

def guardar_df(df):
    df.to_csv(archivo_csv, index=False)

def panel_admin():
    st.subheader("Panel del administrador")
    df = cargar_df()

    if df.empty:
        st.info("No hay solicitudes registradas.")
        return

    total_isr = 0
    total_utilidad = 0
    total_proveedor_con_descuentos = 0
    total_proveedor_sin_descuentos = 0

    for idx, row in df.iterrows():
        with st.expander(f"Solicitud #{idx + 1} - {row['Cliente']} → {row['Destino']}"):

            st.write(f"Tipo camión: {row['Tipo']}")
            st.write(f"Precio total: Q{row['Precio']}")
            subtotal = round(row['Precio'] / 1.12, 2)
            isr = round(subtotal * 0.05, 2)
            utilidad = round(row['Precio'] - isr - 1000, 2)
            proveedor_pago = round(1000 - row['Viáticos'] - row['Combustible'], 2)

            st.write(f"Subtotal: Q{subtotal}")
            st.write(f"ISR (5%): Q{isr}")
            st.write(f"Utilidad estimada: Q{utilidad}")
            st.write(f"Pago proveedor (neto): Q{proveedor_pago}")
            st.write(f"Pago proveedor (total sin descuentos): Q1000")

            df.at[idx, "Piloto1"] = st.selectbox(f"Piloto 1 (Solicitud #{idx + 1})", ["", "piloto1", "piloto2"], index=["", "piloto1", "piloto2"].index(row.get("Piloto1", "")), key=f"p1_{idx}")
            df.at[idx, "Piloto2"] = st.selectbox(f"Piloto 2 (Solicitud #{idx + 1})", ["", "piloto1", "piloto2"], index=["", "piloto1", "piloto2"].index(row.get("Piloto2", "")), key=f"p2_{idx}")
            df.at[idx, "Estado"] = st.selectbox(f"Estado (Solicitud #{idx + 1})", estados, index=estados.index(row.get("Estado", "Pendiente de asignación")), key=f"estado_{idx}")
            df.at[idx, "Fecha liquidación Piloto1"] = st.date_input("Fecha de liquidación Piloto 1", value=pd.to_datetime(row.get("Fecha liquidación Piloto1", datetime.today().date())), key=f"liq_{idx}")
            df.at[idx, "Fecha pago Canella"] = st.date_input("Fecha de pago Canella", value=pd.to_datetime(row.get("Fecha pago Canella", datetime.today().date())), key=f"canella_{idx}")

            if st.button(f"Guardar cambios #{idx}"):
                guardar_df(df)
                st.success("Cambios guardados.")

            total_isr += isr
            total_utilidad += utilidad
            total_proveedor_con_descuentos += proveedor_pago
            total_proveedor_sin_descuentos += 1000

    st.subheader("Resumen total")
    st.write(f"Total solicitudes: {len(df)}")
    st.write(f"Total ISR: Q{total_isr}")
    st.write(f"Total utilidad: Q{total_utilidad}")
    st.write(f"Total pago proveedor (neto): Q{total_proveedor_con_descuentos}")
    st.write(f"Total pago proveedor (sin descuentos): Q{total_proveedor_sin_descuentos}")

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
    if st.session_state["rol"] == "admin":
        panel_admin()
    else:
        st.warning("Este módulo es solo para el administrador.")
    if st.button("Cerrar sesión"):
        st.session_state.clear()
