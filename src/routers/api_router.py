from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4 as uuid
from datetime import datetime
from bson import ObjectId
from src.server.database.database import collection
from src.models.taks_models import TaskModel, StatusEnum, TaskUpdate

task_router = APIRouter()


#Listar todas las tareas
@task_router.get('/tasks/all', tags=['Tasks'])
async def list_tasks():
    tasks = []
    async for task in collection.find(): #Accede a la coleccion e itera sobre los documentos
        task['_id'] = str(task['_id']) #Convierte el '_id' que da mongo por defecto en str ya que es un objeto
        tasks.append(task) #Agrega cada documento en la lista 
    return tasks


#Lista tareas pendientes
@task_router.get('/tasks/pending', tags=['Tasks'])
async def list_tasks_pending():
    pendings = []
    async for task_pend in collection.find():
        task_pend['_id'] = str(task_pend['_id'])
        if task_pend['status'] == 'pending':
            pendings.append(task_pend)
    return pendings


#Crear una tarea
@task_router.post('/create_task/', tags=['Tasks'])
async def create_task(title:str, description: str):
    try:
        now = datetime.now()
        new_task = TaskModel(
            id=str(uuid()), 
            title=title, 
            description=description, 
            status=StatusEnum.pending, 
            created_at=now,
            updated_at=now
        )
        document = new_task.model_dump()
        document["created_at"] = new_task.created_at.isoformat()
        document["updated_at"] = new_task.updated_at.isoformat()
        result = await collection.insert_one(document)
        return JSONResponse(content={'id':str(result.inserted_id)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error al insertar en la base de datos: {str(e)}')


#Actualizar Tarea
@task_router.put('/tasks/', tags=['Tasks'])
async def task_update(custom_id: str, task_update: TaskUpdate):
    if not ObjectId.is_valid(custom_id):
        raise HTTPException(status_code=400, detail='ID no encontrado')
    update_data = {key: value for key, value in task_update.dict().items() if value is not None}
    task = await collection.update_one({'_id': ObjectId(custom_id)}, {'$set':update_data})
    if task.matched_count == 0:
        raise HTTPException(status_code=404, detail='Tarea no encontrada')
    return {'message':'Tarea actualizada correctamente'}