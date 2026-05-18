import warnings
import pandas as pd

from utils.database import create_dataframe_from_cursor
from utils.dict_utils import caipa_rh_dict
from utils.dict_utils import val_servicios

warnings.filterwarnings('ignore')

def get_diagnosticos_df(mongo_client):

    centros_db = mongo_client.centros_database
    diagnosticos_collection = centros_db.diagnosticos
    diagnosticos_cursor = diagnosticos_collection.find({})

    diagnosticos_dataframe = create_dataframe_from_cursor(diagnosticos_cursor)
    diagnosticos_dataframe = diagnosticos_dataframe.set_index(diagnosticos_dataframe["centro"])
    diagnosticos_dataframe = diagnosticos_dataframe.drop("centro", axis=1)
    diagnosticos_dataframe = diagnosticos_dataframe.loc[~diagnosticos_dataframe["administrador"].isnull()]

    return diagnosticos_dataframe

def get_rh_df(diagnosticos_dataframe):

    rh_keys = list(caipa_rh_dict.keys())

    rh_df = diagnosticos_dataframe[rh_keys]

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

def get_categorical_val_df(caipa_df):

    valoracion_keys = list(val_servicios.keys())

    val_servicios_df = caipa_df[valoracion_keys]

    valoracion_categorical_df = pd.DataFrame(columns = ["centro", "servicio", "cantidad"])

    columns = list(val_servicios_df.columns)

    for row in val_servicios_df.iterrows():
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