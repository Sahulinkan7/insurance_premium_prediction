import os,sys
from src.exception import CustomException
from src.logger import logging
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from src.utils.utils import read_dataframe,read_yaml_file,load_numpy_array_data,load_object,save_object
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import importlib

class CustomModel:
    def __init__(self,preprocessing_object: object,
                 model_object: object) -> None:
        try:
            self.preprocessing_object = preprocessing_object
            self.model_object = model_object
        except Exception as e:
            logging.error(f"creating custom model object interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
    def predict(self,x_input):
        try:
            transformed_feature = self.preprocessing_object.transform(x_input)
            return self.model_object.predict(transformed_feature)
        except Exception as e:
            logging.error(f"making prediction interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifacts:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifacts = data_transformation_artifacts
        except Exception as e:
            logging.error(f"Model Trainer object creation interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
    def evaluate_models(self,x_train,y_train,x_test,y_test,models:dict):
        try:
            logging.info(f"starting model training and evaluation")
            models_report = {}
            for i in range(len(list(models))):
                model=list(models.values())[i]
                model.fit(x_train,y_train)
                y_test_pred = model.predict(x_test)
                
                test_score = r2_score(y_test,y_test_pred)
                models_report[list(models.keys())[i]] = test_score
            logging.info(f"models evaluation scores as \n {models_report}")
            return models_report
        except Exception as e:
            logging.error(f"Model Evaluation interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
    
    def get_class_object(self,module_name,class_name):
        try:
            module = importlib.import_module(module_name)
            class_ref= getattr(module,class_name)
            return class_ref()
        except Exception as e:
            logging.error(f"getting class reference interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
    def fine_tune_model(self,best_model_object,best_model_name,x_train,y_train):
        try:
            model_file_content = read_yaml_file(self.model_trainer_config.model_trainer_config_filepath)
            all_models = dict(model_file_content["model_selection"]['models'])
            model_param_grid = all_models[best_model_name]['search_params']
            
            grid_serach_obj = GridSearchCV(best_model_object,param_grid=model_param_grid,cv=5,verbose=3,n_jobs=-1)
            
            grid_serach_obj.fit(x_train,y_train)
            best_params = grid_serach_obj.best_params_
            logging.info(f"best params for {best_model_name} is {best_params}")
            finetuned_model = best_model_object.set_params(**best_params)
            
            return finetuned_model
        
        except Exception as e:
            logging.error(f"getting best tuned model interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
    def initiate_model_training(self)->ModelTrainerArtifact:
        try:
            logging.info(f"splitting train array and test array input and target feature ")
            train_array = load_numpy_array_data(file_path=self.data_transformation_artifacts.transformed_train_arr_filepath)
            test_array = load_numpy_array_data(file_path=self.data_transformation_artifacts.transformed_test_arr_filepath)
            
            logging.info(f"splitting train and test array data to input and target features ")
            
            x_train,y_train,x_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            
            preprocessor = load_object(file_path=self.data_transformation_artifacts.transformed_preprocessor_filepath)
            models_file_content= read_yaml_file(file_path=self.model_trainer_config.model_trainer_config_filepath)
            models=dict(models_file_content['model_selection']['models'])
            training_models = {}
            for key in models.keys():
                print(key,models[key]['class'],models[key]['module'])
                modelobj = self.get_class_object(module_name=models[key]['module'],class_name=models[key]['class'])
                training_models[key]=modelobj
            logging.info(f"training model is {training_models}")
            trained_model_reports: dict= self.evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=training_models)
            best_score = max(sorted(list(trained_model_reports.values())))
            
            best_model_name = list(trained_model_reports.keys())[list(trained_model_reports.values()).index(best_score)]
            best_model = training_models[best_model_name]
            
            fine_tuned_best_model = self.fine_tune_model(best_model_object=best_model,
                                                         best_model_name=best_model_name,
                                                         x_train=x_train,
                                                         y_train=y_train)
            fine_tuned_best_model.fit(x_train,y_train)
            y_test_predictions = fine_tuned_best_model.predict(x_test)
            test_accuracy = r2_score(y_test,y_test_predictions)
            logging.info(f"test accuracy score of best fine tuned model is {test_accuracy}")

            if test_accuracy < 0.7:
                model_accepted = False
            else:
                model_accepted = True
                logging.info(f"best model found ")
                
                os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_file_path),exist_ok=True)
                logging.info(f"saving model in file path : {self.model_trainer_config.trained_model_file_path}")
                
                custom_model_object = CustomModel(preprocessing_object=preprocessor,
                                                  model_object=fine_tuned_best_model)
                
                save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=custom_model_object)
            
            model_trainer_artifacts = ModelTrainerArtifact(
                trained_model_filepath=self.model_trainer_config.trained_model_file_path,
                model_accepted= model_accepted,
                model_accuracy= test_accuracy,
            )
            
            return model_trainer_artifacts
        
        except Exception as e:
            logging.error(f"inititating model trainer method of ModelTrainer component interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)