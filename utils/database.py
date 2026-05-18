import pandas as pd
import pymongo
import urllib
import streamlit as st
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

@st.cache(allow_output_mutation=True)
def get_mongo_client(config):
    """Get the mongo client and store it in cache.

        Params
        ------
        config : Config
            Configuration object containing email details.
        
        Returns
        -------
        client
            The mongo client connected to the database.
        """
    db_mongo = config.get_config()['db_mongo']
    user = db_mongo["user"]
    password = db_mongo["password"]
    cluster = db_mongo["cluster"]
    client = pymongo.MongoClient(
        f"mongodb+srv://{user}:{password}@{cluster}/?retryWrites=true&w=majority"
    )
    return client

def get_mongo_client_debug(config):
    """Get the mongo client.

        Params
        ------
        config : Config
            Configuration object containing email details.
        
        Returns
        -------
        client
            The mongo client connected to the database.
        """
    db_mongo = config.get_config()['db_mongo']
    user = db_mongo["user"]
    password = db_mongo["password"]
    cluster = db_mongo["cluster"]
    client = pymongo.MongoClient(
        f"mongodb+srv://{user}:{password}@{cluster}/?retryWrites=true&w=majority"
    )
    return client

def create_dataframe_from_cursor(cursor):
    """Transform the cursor from mongo into a dataframe

        Params
        ------
        cursor : cursor
            Cursor pointing to a mongo collection.
        
        Returns
        -------
        df
            The dataframe made from the mongo cursor.
        """
    df = None
    for document in cursor:
        if df is not None:
            df = df.append(document, ignore_index=True)
        else:
            df = pd.DataFrame(document, index=[0])
    df.drop("_id", axis=1, inplace=True)
    return df

def get_centros_names(cursor):
    return [document["centro"] for document in cursor]

def get_centro_direccion(selected_center, locations_collection):
    direccion_cursor = locations_collection.find({
                                                    "centro" : selected_center
                                                })

    return direccion_cursor[0]

def update_centro_direccion(direcciones_collection, selected_center, updated_directions_dict):
    direcciones_collection.update_one(
        {
            "centro" : selected_center
        },
        {
            "$set" : {
                    "municipio" : updated_directions_dict["municipio"],
                    "calle" : updated_directions_dict["calle"],
                    "entre_calles" : updated_directions_dict["entre_calles"],
                    "colonia" : updated_directions_dict["colonia"],
                    "CP" : updated_directions_dict["CP"]
            }
        }
    )

# image upload and save to file
@st.cache
def load_image(imagen):
    img = Image.open(imagen)
    return img

def completar_centro(data_dict, collection, centro_id):
    collection.update_one(
        {
            "_id" : centro_id
        },
        {
            "$set" : data_dict
        }
    )

def change_to_categorical(diagnosticos_dataframe, rh_keys):

    categorical_df = pd.DataFrame(columns = ["centro","rol"])

    rh_df = diagnosticos_dataframe[rh_keys]
    rh_df = rh_df.set_index(diagnosticos_dataframe["centro"])
    rh_df = rh_df.loc[~rh_df["administrador"].isnull()]

    for row in rh_df.iterrows():
        for rh in rh_keys:
            categorical_df = categorical_df.append(
                {
                    "centro" : row[0], 
                    "rol" : rh, 
                    "cantidad" : row[1][rh]
                }, 
                ignore_index=True)
    
    return categorical_df