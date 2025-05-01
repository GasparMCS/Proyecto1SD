from fastapi import FastAPI, HTTPException
from app.database import events_collection,cache_collection
from app.models import EventoReal
from bson import ObjectId
from datetime import datetime
from pymongo.errors import OperationFailure

app = FastAPI()
# Elimina el índice si existe y luego lo vuelve a crear con nuevos valores
try:
    cache_collection.drop_index("created_at_1")
except OperationFailure:
    pass  # Si no existe, lo ignoramos

cache_collection.create_index("created_at", expireAfterSeconds=600)#TTL



@app.post("/eventos")
async def crear_evento(evento: EventoReal):
    # Convertimos a dict y añadimos fecha de creación
    evento_data = evento.dict()
    evento_data["created_at"] = datetime.utcnow()
    
    result = events_collection.insert_one(evento_data)
    return {"id": str(result.inserted_id)}


@app.get("/eventos/getall_ids")
async def get_all():
    try:
        # Obtener todos los documentos y extraer solo el campo "_id"
        eventos = events_collection.find({}, {"_id": 1}) # Proyección: solo el _id)
        
        # Convertir los ObjectId a strings (MongoDB devuelve ObjectId por defecto)
        eventos_ids = [str(evento["_id"]) for evento in eventos]
        
        return { "ids" : eventos_ids}
        print(eventos)
        # return {"lista": eventos}
    
    except Exception as e:
        print(f"Error: {e}")  # Para debug
        raise HTTPException(status_code=500, detail=f"Error al obtener eventos: {str(e)}")

lru_evictions = 0
@app.get("/eventos/lru_stats")
def get_lru_stats():
    return {"lru_evictions": lru_evictions}

        
@app.get("/eventos/{evento_id}")
async def leer_evento(evento_id: str):
    global lru_evictions

    try:
        obj_id = ObjectId(evento_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"ID inválido: {str(e)}")

    try:
        evento = cache_collection.find_one({"_id": obj_id})
        if evento:
            evento["_id"] = str(evento["_id"])
            return {"origen": "cache", "evento": evento}

        evento = events_collection.find_one({"_id": obj_id})
        if not evento:
            raise HTTPException(status_code=404, detail="Evento no encontrado")

        evento["created_at"] = datetime.utcnow()
        cache_collection.insert_one(evento)

        if cache_collection.estimated_document_count() > 3000: #LRU
            oldest = cache_collection.find_one(sort=[("created_at", 1)])
            if oldest:
                cache_collection.delete_one({"_id": oldest["_id"]})
                lru_evictions += 1

        evento["_id"] = str(evento["_id"])
        return {"origen": "mongo", "evento": evento}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
