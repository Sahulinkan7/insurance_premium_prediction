from src.pipeline.training_pipeline import TrainingPipeline
from src.exception import CustomException
import sys
from src.logger import logging

try:
    tp = TrainingPipeline()
    tp.start_training()
except Exception as e:
    logging.info(f"{CustomException(e,sys)}")
    raise CustomException(e, sys) from e
