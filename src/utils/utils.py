from src.exception import CustomException
from src.logger import logging
import pandas as pd
import os, sys


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
        logging.info(f"readung dataframe interrupted due to {CustomException(e,sys)}")
        raise CustomException(e, sys)
