from src.components.data_ingestion import DataIngestion
from src.entity.config_entity import (TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,
                                      DataTransformationConfig,ModelTrainerConfig)

import os,sys 
from src.logger import logging

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        os.makedirs(self.training_pipeline_config.training_artifact_dirpath,exist_ok=True)
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        
    def start_data_ingestion(self,data_ingestion_config):
        try:
            logging.info(f"{'+'*20} Data Ingestion started {'+'*20}")
            dt = DataIngestion(data_ingestion_config=data_ingestion_config)
            dt.initiate_data_ingestion()
            logging.info(f"{'+'*20} Data Ingestion completed {'+'*20}")
        except Exception as e:
            raise e
        
    def start_data_validation(self,data_validation_config: DataValidationConfig,
                              data_ingestion_artifact):
        try:
            pass
        except Exception as e:
            raise e
        
    def start_data_transformation(self,data_transformation_config: DataTransformationConfig,
                                  data_validation_artifact):
        try:
            pass
        except Exception as e:
            raise e
    def start_model_training(self,model_trainer_config,
                             data_transformation_artifact):
        try:
            pass
        except Exception as e:
            raise e
        
    def start_training(self):
        try:
            logging.info(f"{'*'*30} starting Model training {'*'*30}")
            self.start_data_ingestion(data_ingestion_config=self.data_ingestion_config)
        except Exception as e:
            raise e
        
        