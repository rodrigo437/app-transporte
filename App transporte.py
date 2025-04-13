
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Tarifario base (corto para ejemplo)
tarifario = {
    "Totonicapán": (144, 2300, 2900, 1584),
    "Santa Lucía Cotzumalguapa": (204, 3400, 4500, 2244),
    "San Marcos": (65, 1300, 1300, 715),
    "Quetzaltenango": (263, 4148, 4148, 2893)
}

usuarios = {
    "admin": {"password": "admin123", "rol": "admin"},
    "cliente1": {"password": "cliente123", "rol": "cliente"},
    "piloto1": {"password": "piloto123", "rol": "piloto"}
}

archivo_csv = "solicitudes.csv"
estados_opciones = ["Solicitud en proceso", "Solicitud aceptada", "Solicitud en ejecución", "Solicitud completada y entregada"]

def calcular_fechas():
    hoy = datetime.today().date()
    prox_lunes = hoy + timedelta(days=(7 - hoy.weekday())) if hoy.weekday() != 0 else hoy
    pago_cliente = prox_lunes + timedelta(days=30)
    fin_de_mes = (datetime(hoy.year, hoy.month, 28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    return hoy, prox_lunes, pago_cliente, fin_de_mes.date()

def guardar_df(df):
    df.to_csv(archivo_csv, index=False)

def cargar_df():
    try:
        return pd.read_csv(archivo_csv)
    except:
        return pd.DataFrame()

def registrar_solicitud(cliente):
    st.subheader("Nueva solicitud de transporte")
    destino = st.selectbox("Destino final", list(tarifario.keys()))
    tipo_camion = st.radio("Tipo de camión", ["5T", "10T"])

    km = tarifario[destino][0]
    precio = tarifario[destino][1] if tipo_camion == "5T" else tarifario[destino][2]
    costo_proveedor = tarifario[destino][3] * 0.7 if tipo_camion == "5T" else tarifario[destino][3]
    km_total = km * 2
    galones = km_total / 10
    combustible = galones * 30
    subtotal = precio / 1.12
    isr = subtotal * 0.05
    iva = precio * 0.12
    viaticos = 60
    utilidad = precio - iva - isr - costo_proveedor
    hoy, oc, pago_cliente, pago_prov = calcular_fechas()

    if st.button("Enviar solicitud"):
        df = cargar_df()
        nueva = {
            "Cliente": cliente,
            "Piloto": "",
            "Destino": destino,
            "Tipo": tipo_camion,
            "KM": km_total,
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
            "Pago Proveedor": pago_prov,
            "Estado": "Solicitud en proceso"
        }
        df = pd.concat([df, pd.DataFrame([nueva])], ignore_index=True)
        guardar_df(df)
        st.success("Solicitud registrada.")

def ver_historial_cliente(cliente):
    st.subheader("Historial de solicitudes")
    df = cargar_df()
    df_cliente = df[df["Cliente"] == cliente]
    if df_cliente.empty:
        st.info("Aún no has registrado solicitudes.")
    else:
        for idx, row in df_cliente.iterrows():
            with st.expander(f"{row['Destino']} - {row['Estado']}"):
                st.write(row)
                if row["Estado"] == "Solicitud en proceso":
                    if st.button(f"Editar solicitud #{idx}"):
                        editar_solicitud_cliente(idx, df)

def editar_solicitud_cliente(index, df):
    row = df.loc[index]
    nuevo_destino = st.selectbox("Nuevo destino", list(tarifario.keys()), index=list(tarifario.keys()).index(row["Destino"]))
    nuevo_tipo = st.radio("Nuevo tipo de camión", ["5T", "10T"], index=0 if row["Tipo"] == "5T" else 1)
    km = tarifario[nuevo_destino][0]
    precio = tarifario[nuevo_destino][1] if nuevo_tipo == "5T" else tarifario[nuevo_destino][2]
    costo_proveedor = tarifario[nuevo_destino][3] * 0.7 if nuevo_tipo == "5T" else tarifario[nuevo_destino][3]
    km_total = km * 2
    galones = km_total / 10
    combustible = galones * 30
    subtotal = precio / 1.12
    isr = subtotal * 0.05
    iva = precio * 0.12
    viaticos = 60
    utilidad = precio - iva - isr - costo_proveedor
    if st.button("Guardar cambios"):
        df.at[index, "Destino"] = nuevo_destino
        df.at[index, "Tipo"] = nuevo_tipo
        df.at[index, "KM"] = km_total
        df.at[index, "Precio"] = precio
        df.at[index, "Costo Proveedor"] = costo_proveedor
        df.at[index, "IVA"] = iva
        df.at[index, "ISR"] = isr
        df.at[index, "Viáticos"] = viaticos
        df.at[index, "Combustible"] = combustible
        df.at[index, "Utilidad"] = utilidad
        guardar_df(df)
        st.success("Solicitud actualizada.")

def panel_admin():
    st.subheader("Panel del administrador")
    df = cargar_df()
    pendientes = df[df["Piloto"] == ""]
    if not pendientes.empty:
        st.warning(f"Tienes {len(pendientes)} solicitudes sin asignar.")
    for idx, row in df.iterrows():
        with st.expander(f"{row['Cliente']} → {row['Destino']} [{row['Estado']}]"):
            st.write(row)
            nuevo_estado = st.selectbox(f"Estado solicitud #{idx}", estados_opciones, index=estados_opciones.index(row["Estado"]), key=f"estado{idx}")
            nuevo_piloto = st.selectbox(f"Asignar piloto #{idx}", ["", "piloto1"], index=0 if row["Piloto"] == "" else 1, key=f"piloto{idx}")
            if st.button(f"Actualizar solicitud #{idx}"):
                df.at[idx, "Estado"] = nuevo_estado
                df.at[idx, "Piloto"] = nuevo_piloto
                guardar_df(df)
                st.success("Solicitud actualizada.")

def panel_piloto(piloto):
    st.subheader("Mis asignaciones")
    df = cargar_df()
    asignadas = df[df["Piloto"] == piloto]
    if asignadas.empty:
        st.info("No tienes solicitudes asignadas.")
    else:
        nuevas = asignadas[asignadas["Estado"] == "Solicitud aceptada"]
        if not nuevas.empty:
            st.success(f"Tienes {len(nuevas)} nuevas asignaciones.")
        st.dataframe(asignadas)

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

# Inicio
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

if not st.session_state["logueado"]:
    login()
else:
    rol = st.session_state["rol"]
    user = st.session_state["usuario"]
    if rol == "admin":
        panel_admin()
    elif rol == "cliente":
        registrar_solicitud(user)
        ver_historial_cliente(user)
    elif rol == "piloto":
        panel_piloto(user)
    if st.button("Cerrar sesión"):
        st.session_state.clear()
