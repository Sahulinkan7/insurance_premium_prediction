import os
from datetime import datetime

SCHEMA_FILEPATH = os.path.join("config","schema.yaml")
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%d_%m_%y_%H_%M_%S')}"
MODEL_TRAINER_CONFIG_FILEPATH = os.path.join("config","models_params.yaml")