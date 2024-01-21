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
    
@dataclass
class DataTransformationArtifact:
    transformed_preprocessor_filepath : str
    transformed_train_arr_filepath : str
    transformed_test_arr_filepath : str
    
@dataclass
class ModelTrainerArtifact:
    trained_model_filepath : str
    model_accepted : bool
    model_accuracy : float
    