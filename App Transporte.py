
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Usuarios fijos
usuarios = {
    "admin": {"password": "admin123", "rol": "admin"},
    "cliente1": {"password": "cliente123", "rol": "cliente"},
    "piloto1": {"password": "piloto123", "rol": "piloto"}
}

archivo_csv = "solicitudes.csv"

def calcular_fechas():
    hoy = datetime.today().date()
    prox_lunes = hoy + timedelta(days=(7 - hoy.weekday())) if hoy.weekday() != 0 else hoy
    pago_cliente = prox_lunes + timedelta(days=30)
    fin_de_mes = (datetime(hoy.year, hoy.month, 28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    return hoy, prox_lunes, pago_cliente, fin_de_mes.date()

def mostrar_admin():
    st.title("Panel del Administrador")
    try:
        df = pd.read_csv(archivo_csv)
        st.dataframe(df)
        st.metric("Total facturado", f"Q{df['Precio'].sum():,.2f}")
        st.metric("Utilidad neta total", f"Q{df['Utilidad'].sum():,.2f}")
    except:
        st.info("No hay solicitudes registradas aún.")

def mostrar_piloto():
    st.title("Panel del Piloto")
    try:
        df = pd.read_csv(archivo_csv)
        asignadas = df[df["Piloto"] == st.session_state["usuario"]]
        if asignadas.empty:
            st.info("No hay rutas asignadas por ahora.")
        else:
            st.dataframe(asignadas[["Cliente", "Destino", "Fecha solicitud"]])
    except:
        st.info("No hay solicitudes registradas.")

def registrar_solicitud():
    st.title("Formulario de Solicitud de Transporte")
    cliente = st.text_input("Nombre del cliente", st.session_state["usuario"])
    destino = st.selectbox("Destino final", ["Totonicapán", "Santa Lucía Cotzumalguapa", "San Marcos", "Quetzaltenango"])
    tipo_camion = st.radio("Tipo de camión", ["5T", "10T"])
    km = st.number_input("Kilómetros estimados (solo ida)", min_value=1)
    galones = km * 2 / 10
    combustible = galones * 30
    precio = 2900 if tipo_camion == "10T" else 2300
    costo_proveedor = 1584 if tipo_camion == "10T" else 1109
    subtotal = precio / 1.12
    isr = subtotal * 0.05
    iva = precio * 0.12
    viaticos = 60
    utilidad = precio - iva - isr - costo_proveedor
    hoy, oc, pago_cliente, pago_prov = calcular_fechas()

    if st.button("Enviar solicitud"):
        nueva = pd.DataFrame([{
            "Cliente": cliente,
            "Piloto": "",
            "Destino": destino,
            "Tipo": tipo_camion,
            "KM ida": km,
            "Precio": precio,
            "Costo Proveedor": costo_proveedor,
            "IVA": iva,
            "ISR": isr,
            "Viáticos": viaticos,
            "Combustible": combustible,
            "Utilidad": utilidad,
            "Fecha solicitud": hoy,
            "Fecha OC": oc,
            "Pago Cliente": pago_cliente,
            "Pago Proveedor": pago_prov
        }])
        try:
            df = pd.read_csv(archivo_csv)
            df = pd.concat([df, nueva], ignore_index=True)
        except:
            df = nueva
        df.to_csv(archivo_csv, index=False)
        st.success("Solicitud registrada exitosamente.")

def login():
    st.title("Login de Usuario")
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if usuario in usuarios and usuarios[usuario]["password"] == password:
            st.session_state["logueado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["rol"] = usuarios[usuario]["rol"]
        else:
            st.error("Usuario o contraseña incorrectos.")

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

if not st.session_state["logueado"]:
    login()
else:
    rol = st.session_state["rol"]
    if rol == "admin":
        mostrar_admin()
    elif rol == "cliente":
        registrar_solicitud()
    elif rol == "piloto":
        mostrar_piloto()
    if st.button("Cerrar sesión"):
        st.session_state.clear()
