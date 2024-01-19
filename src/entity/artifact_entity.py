from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    downloaded_data_filepath: str
    extracted_data_filepath: str
    training_data_filepath: str
    testing_data_filepath: str

@dataclass
class DataValidationArtifact:
    validation_status : bool 
    validation_status_filepath : str
    validated_train_filepath : str
    validated_test_filepath : str