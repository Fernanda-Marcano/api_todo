from fastapi import APIRouter
#from fastapi.response import JSONResponse
from uuid import uuid4 as uuid
from datetime import datetime
from src.models.taks_models import TaksModel, StatusEnum

taks_router = APIRouter()

@taks_router.post('/taks', tags=['Taks'])
def get_taks(title: str, description: str) -> TaksModel:
    now = datetime.now()
    
    return TaksModel(
        id=str(uuid()), 
        title=title, 
        description=description, 
        status=StatusEnum.pending, 
        created_at=now, 
        updated_at=now
    )

