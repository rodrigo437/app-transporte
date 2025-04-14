tarifario = {
    "Destino 1": {'km': 144, 'precio_5t': 2300.0, 'precio_10t': 2900.0, 'proveedor': 1584.0},
    "Destino 2": {'km': 55, 'precio_5t': 1200.0, 'precio_10t': 1400.0, 'proveedor': 605.0},
    "Destino 3": {'km': 204, 'precio_5t': 3400.0, 'precio_10t': 4500.0, 'proveedor': 2244.0},
    "Destino 4": {'km': 223, 'precio_5t': 4400.0, 'precio_10t': 4400.0, 'proveedor': 2453.0},
    "Destino 5": {'km': 508, 'precio_5t': 7500.0, 'precio_10t': 11300.0, 'proveedor': 5588.0},
    "Destino 6": {'km': 65, 'precio_5t': 1300.0, 'precio_10t': 1300.0, 'proveedor': 715.0},
    "Destino 7": {'km': 229, 'precio_5t': 3893.0, 'precio_10t': 4900.0, 'proveedor': 2519.0},
    "Destino 8": {'km': 109, 'precio_5t': 1853.0, 'precio_10t': 1853.0, 'proveedor': 1199.0},
    "Destino 9": {'km': 506, 'precio_5t': 10120.0, 'precio_10t': 11132.0, 'proveedor': 5566.0},
    "Destino 10": {'km': 295, 'precio_5t': 4500.0, 'precio_10t': 4500.0, 'proveedor': 3245.0},
    "Destino 11": {'km': 164, 'precio_5t': 2400.0, 'precio_10t': 2400.0, 'proveedor': 1804.0},
    "Destino 12": {'km': 263, 'precio_5t': 4148.0, 'precio_10t': 4148.0, 'proveedor': 2893.0},
    "Destino 13": {'km': 389, 'precio_5t': 7780.0, 'precio_10t': 8000.0, 'proveedor': 4279.0},
    "Destino 14": {'km': 302, 'precio_5t': 5085.0, 'precio_10t': 6000.0, 'proveedor': 3322.0},
    "Destino 15": {'km': 203, 'precio_5t': 3400.0, 'precio_10t': 3500.0, 'proveedor': 2233.0},
    "Destino 16": {'km': 259, 'precio_5t': 3300.0, 'precio_10t': 3800.0, 'proveedor': 2849.0},
    "Destino 17": {'km': 211, 'precio_5t': 3281.0, 'precio_10t': 4100.0, 'proveedor': 2321.0},
    "Destino 18": {'km': 154, 'precio_5t': 2681.0, 'precio_10t': 3388.0, 'proveedor': 1694.0},
    "Destino 19": {'km': 494, 'precio_5t': 10000.0, 'precio_10t': 10800.0, 'proveedor': 5434.0},
    "Destino 20": {'km': 253, 'precio_5t': 4301.0, 'precio_10t': 4800.0, 'proveedor': 2783.0},
    "Destino 21": {'km': 100, 'precio_5t': 1900.0, 'precio_10t': 1900.0, 'proveedor': 1100.0},
    "Destino 22": {'km': 137, 'precio_5t': 2740.0, 'precio_10t': 2900.0, 'proveedor': 1507.0},
    "Destino 23": {'km': 132, 'precio_5t': 2244.0, 'precio_10t': 2904.0, 'proveedor': 1452.0},
    "Destino 24": {'km': 179, 'precio_5t': 3540.0, 'precio_10t': 3600.0, 'proveedor': 1969.0},
}


import streamlit as st
import pandas as pd
from datetime import datetime, date

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
            df.at[idx, "Fecha liquidación Piloto1"] = st.date_input("Fecha de liquidación Piloto 1", value=pd.to_datetime(row.get("Fecha liquidación Piloto1", date.today())), key=f"liq_{idx}")
            df.at[idx, "Fecha pago Canella"] = st.date_input("Fecha de pago Canella", value=pd.to_datetime(row.get("Fecha pago Canella", date.today())), key=f"canella_{idx}")
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

def panel_cliente(usuario):
    st.subheader("Registrar nueva solicitud")
    destino = st.selectbox("Destino final", ["Totonicapán", "Escuintla", "Huehuetenango", "Petén"])
    tipo = st.radio("Tipo de camión", ["5T", "10T"])
    precio = 2300 if tipo == "5T" else 2900
    km = 200
    fecha_servicio = st.date_input("Fecha del viaje", min_value=date.today())
    hora_carga = st.time_input("Hora de carga")
    cliente_entrega = st.text_input("Cliente de entrega")
    fecha_entrega = st.date_input("Fecha máxima de entrega", min_value=fecha_servicio)
    hora_entrega = st.time_input("Hora máxima de entrega")
    combustible = (km * 2 / 10) * 30
    viaticos = 60 + (60 if km > 50 else 0) + (225 if km > 250 else 0)
    if st.button("Enviar solicitud"):
        df = cargar_df()
        nueva = {
            "Cliente": usuario,
            "Destino": destino,
            "Tipo": tipo,
            "Precio": precio,
            "KM": km * 2,
            "Viáticos": viaticos,
            "Combustible": combustible,
            "Cliente entrega": cliente_entrega,
            "Fecha servicio": fecha_servicio,
            "Hora carga": hora_carga.strftime("%H:%M"),
            "Fecha y hora entrega": f"{fecha_entrega} {hora_entrega}",
            "Piloto1": "",
            "Piloto2": "",
            "Estado": "Pendiente de asignación",
            "Fecha liquidación Piloto1": "",
            "Fecha pago Canella": ""
        }
        df = pd.concat([df, pd.DataFrame([nueva])], ignore_index=True)
        guardar_df(df)
        st.success("Solicitud registrada.")
    st.subheader("Mis solicitudes")
    df = cargar_df()
    df_usuario = df[df["Cliente"] == usuario]
    for idx, row in df_usuario.iterrows():
        with st.expander(f"{row['Destino']} - Estado: {row['Estado']}"):
            st.write(row)
            if row["Estado"] == "Pendiente de asignación":
                if st.button(f"Eliminar #{idx}"):
                    df.drop(index=idx, inplace=True)
                    guardar_df(df)
                    st.experimental_rerun()

def panel_piloto(usuario):
    st.subheader("Solicitudes asignadas")
    df = cargar_df()
    asignadas = df[(df["Piloto1"] == usuario) | (df["Piloto2"] == usuario)]
    if asignadas.empty:
        st.info("No tenés solicitudes asignadas.")
        return
    for idx, row in asignadas.iterrows():
        with st.expander(f"{row['Cliente']} → {row['Destino']} - Estado: {row['Estado']}"):
            st.write(f"Bodega de carga: {row['Cliente']}")
            st.write(f"Hora de carga: {row['Hora carga']}")
            st.write(f"Departamento de entrega: {row['Destino']}")
            st.write(f"Cliente de entrega: {row['Cliente entrega']}")
            st.write(f"Hora máxima de recepción: {row['Fecha y hora entrega']}")
            st.write(f"Viáticos: Q{row['Viáticos']}")
            nuevo_estado = st.radio("Actualizar estado", ["Cargando", "En ruta", "Producto entregado"], key=f"estado_{idx}")
            if st.button(f"Guardar estado #{idx}"):
                df.at[idx, "Estado"] = nuevo_estado
                guardar_df(df)
                st.success("Estado actualizado.")

# Login y redirección por rol
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
    elif st.session_state["rol"] == "cliente":
        panel_cliente(st.session_state["usuario"])
    elif st.session_state["rol"] == "piloto":
        panel_piloto(st.session_state["usuario"])
    if st.button("Cerrar sesión"):
        st.session_state.clear()
