from src.components.data_ingestion import DataIngestion
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from src.components.data_validation import DataValidation
from src.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)

import os, sys
from src.logger import logging
from src.exception import CustomException


class TrainingPipeline:
    is_pipeline_running = False
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        os.makedirs(
            self.training_pipeline_config.training_artifact_dirpath, exist_ok=True
        )
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()

    def start_data_ingestion(self, data_ingestion_config)->DataIngestionArtifact:
        try:
            logging.info(f"{'+'*20} Data Ingestion started {'+'*20}")
            dt = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifacts = dt.initiate_data_ingestion()
            logging.info(f"data ingestion artifacts : {data_ingestion_artifacts}")
            logging.info(f"{'+'*20} Data Ingestion completed {'+'*20}")
            return data_ingestion_artifacts
        except Exception as e:
            logging.info(f"Training pipeline : start data ingestion method interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)

    def start_data_validation(self, data_validation_config: DataValidationConfig,
                              data_ingestion_artifacts: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info(f"{'+'*20} Data Validation started {'+'*20}")
            dv = DataValidation(data_validation_config=data_validation_config,
                                data_ingestion_artifacts=data_ingestion_artifacts)
            data_validation_artifacts = dv.initiate_data_validation()
            logging.info(f"data validation artifact : {data_validation_artifacts}")
            logging.info(f"{'+'*20} Data Validation completed {'+'*20}")
            return data_validation_artifacts
        except Exception as e:
            logging.info(f"Training pipeline start data validation interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)

    def start_data_transformation(
        self,
        data_transformation_config: DataTransformationConfig,
        data_validation_artifact,
    ):
        try:
            pass
        except Exception as e:
            raise e

    def start_model_training(self, model_trainer_config, data_transformation_artifact):
        try:
            pass
        except Exception as e:
            raise e

    def start_training(self):
        try:
            TrainingPipeline.is_pipeline_running=True
            logging.info(f"{'*'*30} starting Model training {'*'*30}")
            data_ingestion_artifacts=self.start_data_ingestion(data_ingestion_config=self.data_ingestion_config)
            data_validation_artifacts = self.start_data_validation(
                data_validation_config=self.data_validation_config,
                data_ingestion_artifacts=data_ingestion_artifacts
            )
            TrainingPipeline.is_pipeline_running=True
            logging.info(f"{'*'*30} Model training completed {'*'*30}")
        except Exception as e:
            logging.info(f"Training pipeline start Training interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
