from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
import os, sys
import urllib.request as urllibrequest
import zipfile
from src.exception import CustomException
from sklearn.model_selection import train_test_split
from src.logger import logging
import pandas as pd
from src.utils.utils import read_dataframe


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        os.makedirs(self.data_ingestion_config.root_dir, exist_ok=True)

    def download_data(self, download_url: str, download_dir_path: str):
        try:
            logging.info(f"starting downloading dataset ")
            logging.info(f"creating download data directory to keep downloaded data")
            os.makedirs(os.path.dirname(download_dir_path), exist_ok=True)
            if not os.path.exists(download_dir_path):
                urllibrequest.urlretrieve(url=download_url, filename=download_dir_path)
            logging.info(f"data downloaded successfully !")
            logging.info(f"data downloaded to path : {download_dir_path}")
            return download_dir_path
        except Exception as e:
            raise CustomException(e, sys)

    def extract_downloaded_data(self, downloaded_data_path):
        try:
            logging.info(f"starting unzipping downloaded data ")
            unzip_path = self.data_ingestion_config.extracted_data_file_path

            logging.info(f"unzipped path : {unzip_path}")
            unzip_dir = os.path.dirname(
                self.data_ingestion_config.extracted_data_file_path
            )
            logging.info(f"creating unzip folder to keep extracted data ")
            os.makedirs(unzip_dir, exist_ok=True)
            with zipfile.ZipFile(downloaded_data_path, "r") as zipreference:
                zipreference.extractall(unzip_dir)

            logging.info(f"data extracted successfully !")
            logging.info(f"data extracted to path {unzip_path}")
            return unzip_path
        except Exception as e:
            raise CustomException(e, sys)

    def split_data(self, extracted_data_path):
        try:
            logging.info(
                f"starting splitting downloaded data to train and test dataset"
            )
            df = read_dataframe(file_path=extracted_data_path)
            traindf, testdf = train_test_split(df, test_size=0.2, random_state=48)

            train_data_filepath = self.data_ingestion_config.train_data_filepath
            test_data_filepath = self.data_ingestion_config.test_data_filepath

            os.makedirs(os.path.dirname(train_data_filepath), exist_ok=True)
            os.makedirs(os.path.dirname(test_data_filepath), exist_ok=True)

            logging.info(f"saving train dataframe to filepath : {train_data_filepath}")
            traindf.to_csv(train_data_filepath, index=False, header=True)

            logging.info(f"saving test dataframe to filepath : {test_data_filepath}")
            testdf.to_csv(test_data_filepath, index=False, header=True)

            logging.info(f"Data splitting completed")
            return (train_data_filepath, test_data_filepath)

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(f"Entered DataIngestion component and initiating Data Ingestion method ")
            downloaded_path = self.download_data(
                download_url=self.data_ingestion_config.dataset_download_url,
                download_dir_path=self.data_ingestion_config.downloaded_data_dir,
            )
            extracted_data_path = self.extract_downloaded_data(
                downloaded_data_path=downloaded_path
            )
            train_data_filepath, test_data_filepath = self.split_data(
                extracted_data_path=extracted_data_path
            )
            data_ingestion_artifacts = DataIngestionArtifact(
                downloaded_data_filepath=downloaded_path,
                extracted_data_filepath=extracted_data_path,
                trained_data_filepath=train_data_filepath,
                test_data_filepath=test_data_filepath,
            )
            logging.info(f"Exiting Data Ingestion component's initate data ingestion method ")
            return data_ingestion_artifacts
        
        except Exception as e:
            raise CustomException(e, sys)
