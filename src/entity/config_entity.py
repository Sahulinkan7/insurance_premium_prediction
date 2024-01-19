from dataclasses import dataclass
import os, sys
from src.constants import CURRENT_TIME_STAMP


@dataclass
class TrainingPipelineConfig:
    training_artifact_dirpath: str = os.path.join("artifacts", f"{CURRENT_TIME_STAMP}")


@dataclass
class DataIngestionConfig:
    root_dir = os.path.join(
        TrainingPipelineConfig.training_artifact_dirpath, "data_ingestion"
    )
    dataset_download_url = f"https://github.com/Sahulinkan7/dataset_repo/raw/main/insurance_premium_prediction.zip"
    downloaded_data_dir = os.path.join(root_dir, "downloaded_data", "insurance.zip")
    extracted_data_file_path = os.path.join(root_dir, "extracted_data", "insurance.csv")
    train_data_filepath = os.path.join(root_dir, "training_data", "train.csv")
    test_data_filepath = os.path.join(root_dir, "testing_data", "test.csv")


@dataclass
class DataValidationConfig:
    root_dir = os.path.join(
        TrainingPipelineConfig.training_artifact_dirpath, "data_validation"
    )
    validation_status_filepath=os.path.join(root_dir,"validation_status","validation_status.yaml")


@dataclass
class DataTransformationConfig:
    root_dir = os.path.join(
        TrainingPipelineConfig.training_artifact_dirpath, "data_transforamtion"
    )


@dataclass
class ModelTrainerConfig:
    root_dir = os.path.join(
        TrainingPipelineConfig.training_artifact_dirpath, "model_trainer"
    )
