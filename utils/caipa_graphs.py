import warnings
import pandas as pd

from utils.database import create_dataframe_from_cursor
from utils.dict_utils import caipa_rh_dict
from utils.dict_utils import caipa_val_servicios

warnings.filterwarnings('ignore')

def get_caipa_df(mongo_client):
    """
    Esta funcion crea el dataframe del cuestionario CAIPA con base
    en los registros almacenados en mongo.

        Params:
        ------
        mongo_cliente: mongo.client
        Cliente de mongo asociado a la cuenta donde se encuentren 
        los registros del cuestionario.

        Returns:
        ------
        caipa_df: pd.DataFrame
        Un dataframe de pandas conteniendo la informacion del 
        cuestionario CAIPA
    """
    caipa_db = mongo_client.caipa
    caipa_collection = caipa_db.registry
    caipa_cursor = caipa_collection.find({})
    caipa_df = create_dataframe_from_cursor(caipa_cursor)
    caipa_df = caipa_df.drop("id", axis=1)
    caipa_df = caipa_df.set_index(caipa_df["centro"])
    caipa_df = caipa_df.drop("centro", axis=1)

    return caipa_df

def get_rh_df(registry_dataframe):
    """
    Esta funcion obtiene un dataframe que contenga unicamente
    los datos relacionados a recursos humanos, formateado 
    de una manera amigable para usar con plotly.

        Params:
        ------
        registry_dataframe: pd.DataFrame
        El dataframe general que contenga la informacion de 
        todo el cuestionario.

        Returns:
        ------
        categorical_df: pd.DataFrame
        Un dataframe de pandas conteniendo solo la informacion
        relacionada a recursos humanos, en un formato de
        la forma
                | centro | rol | cantidad |
                ---------------------------
                | xxxxxx | y  | zzzzzzzz |
        para su facil manejo con la libreria plotly
    """

    rh_keys = list(caipa_rh_dict.keys())

    rh_df = registry_dataframe[rh_keys]

    categorical_df = pd.DataFrame(columns = ["centro","rol"])

    for row in rh_df.iterrows():
        for rh in rh_keys:
            categorical_df = categorical_df.append(
                {
                    "centro" : row[0], 
                    "rol" : rh, 
                    "cantidad" : row[1][rh]
                }, 
                ignore_index=True)

    categorical_df["rol"] = categorical_df["rol"].map(caipa_rh_dict)

    categorical_df["cantidad"] = categorical_df["cantidad"].astype(int)

    return categorical_df

def get_services_count(registry_dataframe):
    """
    Esta funcion obtiene un dataframe que contenga unicamente
    los datos relacionados a servicios, formateado 
    de una manera amigable para usar con plotly.

        Params:
        ------
        registry_dataframe: pd.DataFrame 
        El dataframe general que contenga la informacion de 
        todo el cuestionario.

        Returns:
        ------
        valoracion_categorical_df : pd.DataFrame
        Un dataframe de pandas conteniendo solo la informacion
        relacionada a servicios, en un formato de la forma
                | centro | servicio | cantidad |
                ---------------------------
                | xxxxxx |     y   | zzzzzzzz |
        para su facil manejo con la libreria plotly
    """

    valoracion_categorical_df = pd.DataFrame(columns = ["centro", "servicio", "cantidad"])

    columns = list(caipa_val_servicios.keys())

    columns.remove("jovenes_graduados")

    for row in registry_dataframe.iterrows():
        centro = row[0]
        for col in columns:
            valoracion_categorical_df = valoracion_categorical_df.append(
                {
                    "centro" : centro,
                    "servicio" : col,
                    "cantidad" : row[1][col]
                },
                ignore_index=True
            )

    return valoracion_categorical_df