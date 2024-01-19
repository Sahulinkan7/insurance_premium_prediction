import os, sys
from src.exception import CustomException
from src.logger import logging
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.constants import SCHEMA_FILEPATH
from src.utils.utils import read_yaml_file,read_dataframe,write_yaml_file

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifacts: DataIngestionArtifact):
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifacts = data_ingestion_artifacts
        os.makedirs(self.data_validation_config.root_dir, exist_ok=True)

    def validate_columns(self,current_data_filepath: str) ->bool:
        try:
            logging.info(f"starting dataframe column validation")
            schema_content = read_yaml_file(file_path=SCHEMA_FILEPATH)
            schema_columns=schema_content['COLUMNS'].keys()
            current_df = read_dataframe(file_path=current_data_filepath)
            current_df_columns = list(current_df.columns)
            validation_status = None
            
            column_status_dict = {}
            
            for column in schema_columns:
                if column not in current_df_columns:
                    logging.info(f"column {column} is missing in dataframe")
                    validation_status = False
                    column_status_dict[column] = "missing"
                    write_yaml_file(file_path=self.data_validation_config.validation_status_filepath,
                                    content={'validation_status': validation_status,
                                             'columns_attendance':column_status_dict})
                else:
                    validation_status = True
                    column_status_dict[column] = "present"
                    write_yaml_file(file_path=self.data_validation_config.validation_status_filepath,
                                    content={'validation_status': validation_status,
                                             'columns_attendance':column_status_dict})
            logging.info(f"validation status is {validation_status}")
            logging.info(f"column validation completed")
            return validation_status
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            logging.info(f"Entered Data validation component inititate data validation method")
            validation_status=self.validate_columns(current_data_filepath=self.data_ingestion_artifacts.extracted_data_filepath)
            validation_artifacts = DataValidationArtifact(
                validation_status=validation_status,
                validation_status_filepath=self.data_validation_config.validation_status_filepath,
                validated_train_filepath=self.data_ingestion_artifacts.training_data_filepath,
                validated_test_filepath=self.data_ingestion_artifacts.testing_data_filepath
            )
            logging.info(f"Exited data validation component initiation data validation method")
            return validation_artifacts
        except Exception as e:
            raise e
