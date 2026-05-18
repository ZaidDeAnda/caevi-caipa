import streamlit as st

import plotly.express as px

from utils.config import Config
from utils.database import get_mongo_client
from utils.dict_utils import servicios_dict
from utils.dict_utils import mantenimiento_dict
from utils.caipa_graphs import get_caipa_df
from utils.caipa_graphs import get_rh_df
from utils.caipa_graphs import get_services_count

st.set_page_config(layout="wide")

config = Config()

mongo_client = get_mongo_client(config)

caipa_df = get_caipa_df(mongo_client)

st.header("Panel de visualización sobre cuestionario CAIPA")

seleccion = st.selectbox("¿Qué panel quieres observar?", options=["Recursos humanos", "Conteo de servicios ofertados", "Servicios", "Mantenimiento"])

if seleccion == "Recursos humanos":

    st.header("Recursos humanos")

    rh_df = get_rh_df(caipa_df)

    promedio = rh_df.groupby("centro").sum().describe().loc["mean"]["cantidad"]

    fig = px.histogram(rh_df, x="centro", y="cantidad", color="rol")

    fig.add_hline(promedio, annotation_text=f"Promedio de personal = {promedio}")

    fig.update_layout(
        {
            "height" : 1000,
            "width" : 1400,
            "legend_title_text" : "Rol"
        }
    )

    st.plotly_chart(fig)

elif seleccion == "Conteo de servicios ofertados":

    st.header("Servicios ofertados")

    count_df = get_services_count(caipa_df)

    fig = px.histogram(count_df, x="centro", y="cantidad", color="servicio")

    fig.update_layout(
        {
            "height" : 1000,
            "width" : 1400,
            "legend_title_text" : "Servicio ofertado"
        }
    )

    st.plotly_chart(fig)

elif seleccion == "Servicios":

    st.header("Revisión de servicios por centro")

    servicios_keys = list(servicios_dict.keys())

    servicios_df = caipa_df[servicios_keys]

    ############

    st.subheader("Servicio de agua")

    fig = px.pie(servicios_df, names = servicios_df["agua"].value_counts().index, values = servicios_df["agua"].value_counts())

    fig.update_layout(
        {
            "height" : 400,
            "width" : 1000,
            "legend_title_text" : "¿El centro cuenta con servicio de agua?"
        }
    )

    st.plotly_chart(fig)

    ############

    st.subheader("Servicio de gas")

    fig = px.pie(servicios_df, names = servicios_df["gas"].value_counts().index, values = servicios_df["gas"].value_counts())

    fig.update_layout(
        {
            "height" : 400,
            "width" : 1000,
            "legend_title_text" : "¿El centro cuenta con servicio de gas?"
        }
    )

    st.plotly_chart(fig)

    ############

    st.subheader("Servicio de internet")

    fig = px.pie(servicios_df, names = servicios_df["internet"].value_counts().index, values = servicios_df["internet"].value_counts())

    fig.update_layout(
        {
            "height" : 400,
            "width" : 1000,
            "legend_title_text" : "¿El centro cuenta con servicio de internet?"
        }
    )

    st.plotly_chart(fig)

    ############

    st.subheader("Servicio de luz")

    fig = px.pie(servicios_df, names = servicios_df["luz"].value_counts().index, values = servicios_df["luz"].value_counts())

    fig.update_layout(
        {
            "height" : 400,
            "width" : 1000,
            "legend_title_text" : "¿El centro cuenta con servicio de luz?"
        }
    )

    st.plotly_chart(fig)

    ############

    st.subheader("Servicio de telefonia")

    fig = px.pie(servicios_df, names = servicios_df["telefonos"].value_counts().index, values = servicios_df["telefonos"].value_counts())

    fig.update_layout(
        {
            "height" : 400,
            "width" : 1000,
            "legend_title_text" : "¿El centro cuenta con servicio de telefonos?"
        }
    )

    st.plotly_chart(fig)

elif seleccion == "Mantenimiento":

    st.header("Revisión de servicios de mantenimiento")

    mantenimiento_keys = list(mantenimiento_dict.keys())

    mantenimiento_df = caipa_df[mantenimiento_keys]

    ############

    st.subheader("Mantenimiento al área de plomeria")

    fig = px.pie(mantenimiento_df, names = mantenimiento_df["plomeria"].value_counts().index, values = mantenimiento_df["plomeria"].value_counts())

    fig.update_layout(
        {
            "height" : 400,
            "width" : 1000,
            "legend_title_text" : "¿El centro cuenta con servicio de mantenimiento a la plomeria?"
        }
    )

    st.plotly_chart(fig)

    ###############

    st.subheader("Mantenimiento a las ventanas")

    fig = px.pie(mantenimiento_df, names = mantenimiento_df["ventanas"].value_counts().index, values = mantenimiento_df["ventanas"].value_counts())

    fig.update_layout(
        {
            "height" : 400,
            "width" : 1000,
            "legend_title_text" : "¿El centro cuenta con servicio de mantenimiento hacia las ventanas?"
        }
    )

    st.plotly_chart(fig)

    ##############

    st.subheader("Mantenimiento al apartado eléctrico")

    fig = px.pie(mantenimiento_df, names = mantenimiento_df["electricidad"].value_counts().index, values = mantenimiento_df["electricidad"].value_counts())

    fig.update_layout(
        {
            "height" : 400,
            "width" : 1000,
            "legend_title_text" : "¿El centro cuenta con servicio de mantenimiento para la electricidad?"
        }
    )

    st.plotly_chart(fig)

    #############

    st.subheader("Mantenimiento a los climas")

    fig = px.pie(mantenimiento_df, names = mantenimiento_df["climas"].value_counts().index, values = mantenimiento_df["climas"].value_counts())

    fig.update_layout(
        {
            "height" : 400,
            "width" : 1000,
            "legend_title_text" : "¿El centro cuenta con servicio de mantenimiento para los climas?"
        }
    )
    
    st.plotly_chart(fig)

    ################

    st.subheader("Mantenimiento al mobiliario")

    fig = px.pie(mantenimiento_df, names = mantenimiento_df["mobiliario"].value_counts().index, values = mantenimiento_df["mobiliario"].value_counts())

    fig.update_layout(
        {
            "height" : 400,
            "width" : 1000,
            "legend_title_text" : "¿El centro cuenta con servicio de mantenimiento para el mobiliario?"
        }
    )

    st.plotly_chart(fig)

    ################

    st.subheader("Mantenimiento a los elevadores")

    fig = px.pie(mantenimiento_df, names = mantenimiento_df["elevadores"].value_counts().index, values = mantenimiento_df["elevadores"].value_counts())

    fig.update_layout(
        {
            "height" : 400,
            "width" : 1000,
            "legend_title_text" : "¿El centro cuenta con servicio de mantenimiento para los elevadores?"
        }
    )