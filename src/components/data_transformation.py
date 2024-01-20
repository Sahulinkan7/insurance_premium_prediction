import os,sys
from src.exception import CustomException
from src.logger import logging
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder
from src.utils.utils import read_dataframe,read_yaml_file
from src.constants import SCHEMA_FILEPATH
from src.utils.utils import save_numpy_array_data,save_object
import numpy as np 

class DataTransformation:
    def __init__(self,data_transformation_config : DataTransformationConfig,
                 data_validation_artifact : DataValidationArtifact):
        self.data_transformation_config = data_transformation_config
        self.data_validation_artifact = data_validation_artifact
        
    def get_data_transformation_object(self):
        try:
            logging.info(f"getting data transformation object process started ")
            
            numerical_columns = ['age','bmi','children']
            onehot_categories_columns = ["region","sex"]
            ordinal_categories_columns = ["smoker"]
            
            smoke_categories = ["no","yes"]
            
            numerical_pipeline = Pipeline(
                steps=[
                ("impute",SimpleImputer()),
                ("scaler",StandardScaler())
            ])
            
            onehot_categorical_pipeline = Pipeline(
                steps=[
                    ("impute",SimpleImputer(strategy="most_frequent")),
                    ("onehotencoder",OneHotEncoder())
                ]
            )
            
            ordinal_categorical_pipeline = Pipeline(
                steps=[
                    ("impute",SimpleImputer(strategy="most_frequent")),
                    ("ordinalencoder",OrdinalEncoder(categories=[smoke_categories])),
                    ("scaler",StandardScaler())
                ]
            )
            
            preprocessor = ColumnTransformer(
                [('num_pipeline',numerical_pipeline,numerical_columns),
                ('ordinal_cat_pipeline',ordinal_categorical_pipeline,ordinal_categories_columns),
                ('onehot_cat_pipeline',onehot_categorical_pipeline,onehot_categories_columns)]
            )
            
            logging.info(f"data transformerobject created successfully !")
            return preprocessor 
        
        except Exception as e:
            logging.error(f"getting data transformation object interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self):
        try:
            
            train_dataframe = read_dataframe(file_path=self.data_validation_artifact.validated_train_filepath)
            test_dataframe = read_dataframe(file_path=self.data_validation_artifact.validated_test_filepath)
            
            preprocessor = self.get_data_transformation_object()
            
            target_column = list(
                read_yaml_file(file_path=SCHEMA_FILEPATH)['TARGET_COLUMNS'].keys()
                )[0]
            
            # splitting training dataframe
            logging.info(f"droping target column from training dataframe")
            input_feature_train_df = train_dataframe.drop(columns=target_column,axis=1)
            target_feature_train_df = train_dataframe[target_column]
            logging.info(f"columns for model training are \n {input_feature_train_df.columns}")
            logging.info(f"target feature {target_column} droped from train dataframe")
            logging.info(f"input feature and target feature for training created successfully !")
            
            # splitting testing dataframe
            logging.info(f"droping target column from test dataframe")
            input_feature_test_df = test_dataframe.drop(columns=target_column)
            target_feature_test_df = test_dataframe[target_column]
            logging.info(f"columns for model testing are \n {input_feature_test_df.columns}")
            logging.info(f"target feature {target_column} droped from test dataframe")
            logging.info(f"input feature and target feature for testing created successfully !")
            
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            
            transformed_input_train_features = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_features = preprocessor_object.transform(input_feature_test_df)
            
            transformed_train_arr = np.c_[transformed_input_train_features,np.array(target_feature_train_df)]
            transformed_test_arr = np.c_[transformed_input_test_features,np.array(target_feature_test_df)]
            
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_arr_filepath,array=transformed_train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_arr_filepath,array=transformed_test_arr)
            
            logging.info(f"transformed train and test array got saved !")
            
            save_object(file_path=self.data_transformation_config.transformed_preprocessor_filepath,obj=preprocessor)
            
            logging.info(f"transformation preprocessor object saved ! ")
            
            logging.info(f"input features of train and test are created successfully ! ")
            
            data_transformation_artifacts = DataTransformationArtifact(
                transformed_preprocessor_filepath=self.data_transformation_config.transformed_preprocessor_filepath,
                transformed_train_arr_filepath = self.data_transformation_config.transformed_train_arr_filepath,
                transformed_test_arr_filepath = self.data_transformation_config.transformed_test_arr_filepath
            )
            
            return data_transformation_artifacts
            
        except Exception as e:
            logging.error(f"Data Transformation component initiation method interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        