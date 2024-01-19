import logging
from datetime import datetime
import os
log_file_name = f"log_{datetime.now().strftime('%d_%m_%y_%H_%M_%S')}.log"

log_file_dir = "logs"
log_file_path = os.path.join(log_file_dir,log_file_name)
os.makedirs(os.path.dirname(log_file_path),exist_ok=True)

logging.basicConfig(filename=log_file_path,format="[%(asctime)s - %(name)s - %(levelname)s] : %(message)s",
                    level=logging.INFO)