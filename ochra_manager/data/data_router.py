import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)
COLLECTION = "data"

class DataRouter(APIRouter):
    def __init__(self):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)

        #TODO: add routes here
    
    #TODO: add route functions here