
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

usuarios = {
    "admin": {"password": "admin123", "rol": "admin"},
    "cliente1": {"password": "cliente123", "rol": "cliente"},
    "piloto1": {"password": "piloto123", "rol": "piloto"},
    "piloto2": {"password": "piloto123", "rol": "piloto"}
}

tarifario = {
    "Totonicapán": (144, 2300, 2900, 1584),
    "Santa Lucía Cotzumalguapa": (204, 3400, 4500, 2244),
    "San Marcos": (65, 1300, 1300, 715),
    "Quetzaltenango": (263, 4148, 4148, 2893)
}

archivo_csv = "solicitudes.csv"
archivo_estados = "historial_estados.csv"
estados_opciones = ["Solicitud en proceso", "Solicitud aceptada", "Solicitud en ejecución", "Solicitud completada y entregada"]

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

def calcular_fechas():
    hoy = datetime.today().date()
    prox_lunes = hoy + timedelta(days=(7 - hoy.weekday())) if hoy.weekday() != 0 else hoy
    pago_cliente = prox_lunes + timedelta(days=30)
    fin_de_mes = (datetime(hoy.year, hoy.month, 28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    return hoy, prox_lunes, pago_cliente, fin_de_mes.date()

def calcular_viaticos(km):
    almuerzo = 60
    cena = 60 if km > 50 else 0
    hotel = 225 if km > 250 else 0
    total = almuerzo + cena + hotel
    return almuerzo, cena, hotel, total

def registrar_solicitud(cliente):
    st.subheader("Nueva solicitud de transporte")
    destino = st.selectbox("Destino final", list(tarifario.keys()))
    tipo_camion = st.radio("Tipo de camión", ["5T", "10T"])
    hora_carga = st.time_input("Hora de carga")
    hora_entrega = st.time_input("Hora de entrega")

    km = tarifario[destino][0]
    precio = tarifario[destino][1] if tipo_camion == "5T" else tarifario[destino][2]
    costo_proveedor = tarifario[destino][3] * 0.7 if tipo_camion == "5T" else tarifario[destino][3]
    km_total = km * 2
    galones = km_total / 10
    combustible = galones * 30
    subtotal = precio / 1.12
    isr = subtotal * 0.05
    iva = precio * 0.12
    almuerzo, cena, hotel, viaticos = calcular_viaticos(km)
    utilidad = precio - isr - costo_proveedor
    iva_compensar = iva
    hoy, oc, pago_cliente, pago_prov = calcular_fechas()

    if st.button("Enviar solicitud"):
        df = cargar_df()
        nueva = {
            "Cliente": cliente,
            "Piloto1": "",
            "Piloto2": "",
            "Destino": destino,
            "Tipo": tipo_camion,
            "Hora carga": hora_carga.strftime('%H:%M'),
            "Hora entrega": hora_entrega.strftime('%H:%M'),
            "KM": km_total,
            "Precio": precio,
            "Subtotal": subtotal,
            "Costo Proveedor": costo_proveedor,
            "ISR": isr,
            "IVA": iva,
            "IVA a compensar": iva_compensar,
            "Viáticos": viaticos,
            "Almuerzo": almuerzo,
            "Cena": cena,
            "Hotel": hotel,
            "Combustible": combustible,
            "Utilidad": utilidad,
            "Fecha solicitud": hoy,
            "Fecha OC": oc,
            "Pago Cliente": pago_cliente,
            "Pago Proveedor": pago_prov,
            "Estado": "Solicitud en proceso"
        }
        df = pd.concat([df, pd.DataFrame([nueva])], ignore_index=True)
        guardar_df(df)
        st.success("Solicitud registrada.")

def historial_cliente(cliente):
    st.subheader("Mis solicitudes")
    df = cargar_df()
    df_cliente = df[df["Cliente"] == cliente]
    if df_cliente.empty:
        st.info("No tenés solicitudes registradas.")
    else:
        for idx, row in df_cliente.iterrows():
            with st.expander(f"{row['Destino']} - Estado: {row['Estado']}"):
                st.write(row)
                if row["Estado"] == "Solicitud en proceso":
                    if st.button(f"Modificar solicitud #{idx}"):
                        editar_solicitud_cliente(idx, df)
                elif row["Estado"] == "Solicitud aceptada":
                    st.warning("La solicitud ya fue aceptada. Si necesitás modificarla, comunicate con el administrador.")

def editar_solicitud_cliente(idx, df):
    row = df.loc[idx]
    destino = st.selectbox("Nuevo destino", list(tarifario.keys()), index=list(tarifario.keys()).index(row["Destino"]))
    tipo_camion = st.radio("Nuevo tipo de camión", ["5T", "10T"], index=0 if row["Tipo"] == "5T" else 1)
    km = tarifario[destino][0]
    precio = tarifario[destino][1] if tipo_camion == "5T" else tarifario[destino][2]
    costo_proveedor = tarifario[destino][3] * 0.7 if tipo_camion == "5T" else tarifario[destino][3]
    km_total = km * 2
    galones = km_total / 10
    combustible = galones * 30
    subtotal = precio / 1.12
    isr = subtotal * 0.05
    iva = precio * 0.12
    almuerzo, cena, hotel, viaticos = calcular_viaticos(km)
    utilidad = precio - isr - costo_proveedor
    iva_compensar = iva

    if st.button("Guardar cambios"):
        df.at[idx, "Destino"] = destino
        df.at[idx, "Tipo"] = tipo_camion
        df.at[idx, "KM"] = km_total
        df.at[idx, "Precio"] = precio
        df.at[idx, "Subtotal"] = subtotal
        df.at[idx, "Costo Proveedor"] = costo_proveedor
        df.at[idx, "ISR"] = isr
        df.at[idx, "IVA"] = iva
        df.at[idx, "IVA a compensar"] = iva_compensar
        df.at[idx, "Viáticos"] = viaticos
        df.at[idx, "Almuerzo"] = almuerzo
        df.at[idx, "Cena"] = cena
        df.at[idx, "Hotel"] = hotel
        df.at[idx, "Combustible"] = combustible
        df.at[idx, "Utilidad"] = utilidad
        guardar_df(df)
        st.success("Solicitud modificada correctamente.")

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
