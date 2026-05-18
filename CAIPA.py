import streamlit as st
import pandas as pd
from utils.config import Config
from utils.database import get_mongo_client
from utils.dict_utils import caipa_rh_dict
from utils.dict_utils import caipa_val_servicios
from utils.dict_utils import servicios_dict
from utils.dict_utils import mantenimiento_dict

st.write('<style>label.css-qrbaxs.effi0qh0 > label{font-weight: bold}</style>', unsafe_allow_html=True)
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

config = Config()

client = get_mongo_client(config)
caipa_db = client.caipa
caipa_collection = caipa_db.registry

col1, col2 = st.columns(2)
col1.header("Gobierno del Estado de Nuevo León")

st.subheader('Centro de atención integral para adolescentes')

st.write("### Valoración de recursos humanos")

data = {}

st.markdown("___")

col3, col4 = st.columns(2)

for key, value in list(caipa_rh_dict.items()):
    data[key] = col3.selectbox(f'Cuánto(s) {value} tienen',[*range(0,11)])

data["manual_org"] = col4.selectbox("¿El centro cuenta con manual de organización publicado?", ["No", "Sí", "No Aplica"])
data["porcentaje_subsidiado"] = col4.text_input("¿Cuál es el porcentaje del personal del centro subsidiado?" "%")

if (len(data["porcentaje_subsidiado"]) != 3 or len(data["porcentaje_subsidiado"]) != 4):
    col4.warning("Inserte un porcentaje válido")

data["porcentaje_capacitado"] = col4.text_input("¿Cuál es el porcentaje del personal del centro capacitado en el nuevo modelo CAIPA 2.0?" "%")

if (len(data["porcentaje_subsidiado"]) != 3 or len(data["porcentaje_subsidiado"]) != 4):
    col4.warning("Inserte un porcentaje válido")

data["acciones_plan"] = col4.selectbox("¿Las acciones de CAIPA se encuentran en el plan municipal?", ["No", "Sí"])

data["centro_subsidio"] = col4.selectbox("¿El centro recibe subsidio del gobierno federal?", ["No", "Sí"])

if data["centro_subsidio"] == "Sí":
    col4.text_input("¿Cuál es el monto anual?", "mxn")

st.markdown("___")
st.write("### Valoración de servicios brindados (último año)")

col5, col6 = st.columns(2)

for key, value in list(caipa_val_servicios.items())[:7]:
    data[key] = col5.selectbox(f'Número de servicios brindados de {value}',["No Aplica", *range(0,11)])

for key, value in list(caipa_val_servicios.items())[7:]:
    data[key] = col6.selectbox(f'Número de servicios brindados de {value}',["No Aplica", *range(0,11)])

st.markdown("___")
st.write("### Valoración de servicios en las instalaciones")

col7, col8 = st.columns(2)

data["ubicacion_centro"] = col7.text_input("ubicación del centro")
data["direccion"] = col7.text_input("Dirección del centro")

data["presupuesto"] = col8.text_input("Presupuesto anual")
data["monto_servicios"] = col8.text_input("Monto mensual de servicios")

data["adscripcion"] = col7.text_input("Unidad administrativa municial de adscripción")

for key, value in list(servicios_dict.items()):
    data[key] = col7.selectbox(f'¿Cuenta con servicio de {value}?',["No Aplica", "Sí", "No"])

data["renta"] = col8.selectbox("¿El edificio donde se encuentra el centro es rentado?",["No Aplica", "Sí", "No"])

if data["renta"] == "Sí":
    col8.text_input("Monto de renta mensual")
    col8.text_input("Vigencia del contrato")

data["comodato"] = col8.selectbox("¿El edificio donde se encuentra el centro está en comodato?",["No Aplica", "Sí", "No"])

data["transporte"] = col8.selectbox("¿El edificio tiene fácil acceso al transporte Público?",["No", "Sí"])

data["estacionamiento_personal"] = col8.selectbox("¿El edificio cuenta con estacionamiento para el personal?",["No", "Sí"])

data["estacionamiento_usuarios"] = col8.selectbox("¿El edificio cuenta con estacionamiento para los usuarios?",["No", "Sí"])

st.markdown("___")
st.write("### Valoración de mantenimiento de instalaciones")

col9, col10 = st.columns(2)

for key, value in list(mantenimiento_dict.items())[:3]:
    data[key] = col9.selectbox(f'¿Cuenta con servicio de {value}?',["No Aplica", "Sí", "No"])

for key, value in list(mantenimiento_dict.items())[3:]:
    data[key] = col10.selectbox(f'¿Cuenta con servicio de {value}?',["No Aplica", "Sí", "No"])

sub = st.empty()

if sub.button('Enviar'):
    data_diagnostico=pd.DataFrame([data])
    emp = data_diagnostico.empty
    if (emp == True):
        st.warning('**Por favor verifique que se ingresaron todos los campos y se adjunto imagen del centro comunitario**')

    else:
        caipa_collection.insert_one(data)
        sub.info('**Muchas gracias por completar la encuesta.**')