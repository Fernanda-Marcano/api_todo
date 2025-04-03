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
    async for task_pend in collection.find(): #Filtrar todas las task
        task_pend['_id'] = str(task_pend['_id'])
        if task_pend['status'] == 'pending': #Buscar las task con 'status' = pending
            pendings.append(task_pend)
    if not pendings:
        raise HTTPException(status_code=404, detail='No existen tareas pendientes')
    return pendings


#Lista de tareas en proceso
@task_router.get('/tasks/process', tags=['Tasks'])
async def list_tasks_process():
    process = []
    async for task_proc in collection.find({'status':'process'}): #Filtra las task que cumplen con el 'status' = process
        task_proc['_id'] = str(task_proc['_id'])
        process.append(task_proc) #Se almacena en la lista 
    if process == []:
        raise HTTPException(status_code=404, detail='No existen tareas en proceso')
    return process


#Lista de tareas completadas
@task_router.get('/tasks/completed', tags=['Tasks'])
async def list_tasks_completed():
    completeds = []
    async for task_comp in collection.find({'status':'completed'}): #Filtra las task que cumplen con el 'status' = completed
        task_comp['_id'] = str(task_comp['_id'])
        completeds.append(task_comp)
    if not completeds:
        raise HTTPException(status_code=404, detail='No existen tareas completadas')
    return completeds


#Buscar una tarea
@task_router.get('/task', tags=['Tasks'])
async def get_task(id: str):
    if not ObjectId.is_valid(id): #Valida que el id que se paso se encuentre en la base de datos
        raise HTTPException(status_code=400, detail='ID no encontrado')
    task = await collection.find_one({'_id': ObjectId(id)}) #Busca el documento que coincide con el id y lo almacena en la variable
    task['_id'] = str(task['_id'])
    if task == 0:
        raise HTTPException(status_code=404, detail='Tarea no encontrada')
    return task


#Crear una tarea
@task_router.post('/create_task/', tags=['Tasks'])
async def create_task(title:str, description: str):
    try:
        now = datetime.now() #Obtiene la fecha actual
        new_task = TaskModel(
            id=str(uuid()), 
            title=title, 
            description=description, 
            status=StatusEnum.pending, 
            created_at=now,
            updated_at=now
        )
        document = new_task.model_dump() #Convertimos el objeto en un diccionario
        document["created_at"] = new_task.created_at.isoformat()
        document["updated_at"] = new_task.updated_at.isoformat()
        result = await collection.insert_one(document) #Inserta el documento en la collection correspondiente
        return JSONResponse(content={'id':str(result.inserted_id)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error al insertar en la base de datos: {str(e)}')


#Actualizar Tarea
@task_router.put('/update_task', tags=['Tasks'])
async def task_update(custom_id: str, task_update: TaskUpdate):
    if not ObjectId.is_valid(custom_id):
        raise HTTPException(status_code=400, detail='ID no encontrado')
    update_data = {key: value for key, value in task_update.dict().items() if value is not None}
    task = await collection.update_one({'_id': ObjectId(custom_id)}, {'$set':update_data})
    if task.matched_count == 0:
        raise HTTPException(status_code=404, detail='Tarea no encontrada')
    return {'message':'Tarea actualizada correctamente'}


#Eliminar una tarea
@task_router.delete('/delete_task/', tags=['Tasks'])
async def delete_task(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail='ID no encontrado')
    task = await collection.delete_one({'_id':ObjectId(id)}) #Busca el documento que corresponde con el id y lo elimina
    if task.deleted_count == 0:
        raise HTTPException(status_code=404, detail='Tarea no encontrada')
    return {'message':'Tarea eliminada correctamente'}