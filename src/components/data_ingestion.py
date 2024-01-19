from src.entity.config_entity import DataIngestionConfig
import os,sys
import urllib.request as urllibrequest
import zipfile
from src.exception import CustomException

class DataIngestion:
    def __init__(self,data_ingestion_config : DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        os.makedirs(self.data_ingestion_config.root_dir,exist_ok=True)
    
    def download_data(self,download_url: str,download_dir_path: str):
        try:
            os.makedirs(os.path.dirname(download_dir_path),exist_ok=True)
            if not os.path.exists(download_dir_path):
                urllibrequest.urlretrieve(url=download_url,filename=download_dir_path)
            
            return download_dir_path
        except Exception as e:
            raise CustomException(e,sys)
        
    def extract_downloaded_data(self,downloaded_data_path):
        try:
            unzip_path = self.data_ingestion_config.extracted_data_file_path
            unzip_dir = os.path.dirname(self.data_ingestion_config.extracted_data_file_path)
            os.makedirs(unzip_dir,exist_ok=True)
            with zipfile.ZipFile(downloaded_data_path,"r") as zipreference:
                zipreference.extractall(unzip_dir)
                
            return unzip_path
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            downloaded_path = self.download_data(download_url=self.data_ingestion_config.dataset_download_url,
                               download_dir_path=self.data_ingestion_config.downloaded_data_dir)
            extracted_data_path = self.extract_downloaded_data(downloaded_data_path=downloaded_path)
            
        except Exception as e:
            raise CustomException(e,sys)