import os, sys
from src.exception import CustomException
from src.logger import logging

from src.entity.config_entity import DataValidationConfig


class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig):
        self.data_validation_config = data_validation_config
        os.makedirs(self.data_validation_config.root_dir, exist_ok=True)

    def initiate_data_validation(Self):
        try:
            pass
        except Exception as e:
            raise e
