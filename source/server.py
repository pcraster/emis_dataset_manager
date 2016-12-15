import os
from dataset_manager import create_app


app = create_app(os.getenv("EMIS_DATA_MANAGER_CONFIGURATION"))
