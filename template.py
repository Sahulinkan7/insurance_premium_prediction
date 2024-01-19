import os
from pathlib import Path
import logging 
logging.basicConfig(level=logging.INFO,format="[%(asctime)s] : %(message)s")

list_of_files=[
    f"src/__init__.py",
    f"src/components/__init__.py",
    f"src/components/data_ingestion.py",
    f"src/components/data_validation.py",
    f"src/components/data_transformation.py",
    f"src/components/model_trainer.py",
    f"src/entity/__init__.py",
    f"src/entity/config_entity.py",
    f"src/entity/artifact_entity.py",
    f"src/pipeline/__init__.py",
    f"src/pipeline/training_pipeline.py",
    f"src/pipeline/prediction_pipeline.py",
    f"src/logger.py",
    f"src/exception.py",
    f"requirements.txt",
    f"setup.py",
    f"main.py",
    f"schema.yaml",
    f"params.yaml"
]

for file in list_of_files:
    filepath=Path(file)
    filedir,filename=os.path.split(filepath)
    
    if filedir !="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"creating directory : {filedir} for {filename}")
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,"w") as f:
            pass 
            logging.info(f"creating empty file : {filepath}")
    
    else:
        logging.info("filepath exists")