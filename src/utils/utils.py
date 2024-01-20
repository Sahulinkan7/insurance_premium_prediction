from src.exception import CustomException
from src.logger import logging
import pandas as pd
import os, sys
import yaml
import pickle
import numpy as np

def read_dataframe(file_path: str) -> pd.DataFrame:
    try:
        logging.info(f"reading dataframe from filepath")
        df = pd.read_csv(file_path)
        logging.info(
            f"dataframe shape is {df.shape} \n dataframe columns : {df.columns}"
        )
        logging.info(f"dataframe is as below \n {df.head(2).to_string()}")
        return df
    except Exception as e:
        logging.error(f"reading dataframe interrupted due to {CustomException(e,sys)}")
        raise CustomException(e, sys)
    
def read_yaml_file(file_path :str ) -> dict:
    try:
        logging.info(f"reading yaml file from file path : {file_path}")
        with open(file_path,'r') as file:
            content = yaml.safe_load(file)
            logging.info(f"content of the yaml file is {content}")
            return content
    except Exception as e:
        logging.error(f"reading yaml file interrupted due to {CustomException(e,sys)}")
        raise CustomException(e,sys)
    
def write_yaml_file(file_path : str ,content: dict):
    try:
        logging.info(f"writing yaml file in the filepath : {file_path}")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        logging.error(f"writing yaml file interrupted due to {CustomException(e,sys)}")
        raise CustomException(e,sys)
    
def save_object(file_path,obj):
    try:
        logging.info(f"saving object in file path : {file_path}")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file:
            pickle.dump(obj=obj,file=file)
            
    except Exception as e:
        logging.error(f"saving object interrupted due to {CustomException(e,sys)}")
        raise CustomException(e,sys)
    
def save_numpy_array_data(file_path,array):
    try:
        logging.info(f"saving numpy array data in {file_path}")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file:
            np.save(file=file,arr=array)
    except Exception as e:
        logging.error(f"saving numpy array data interrupted due to {CustomException(e,sys)}")
        raise CustomException(e,sys)
    
