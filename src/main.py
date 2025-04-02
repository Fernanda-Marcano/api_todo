from fastapi import FastAPI
from src.routers.api_router import task_router


app = FastAPI()
app.title = 'To-Do API with FastAPI'
app.version = '1.0.0'


@app.get('/', tags=['Home'])
def home():
    return 'Hola'

app.include_router(router=task_router)
