from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pydantic import BaseModel

cred = credentials.Certificate("cred.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)


class Restaurant(BaseModel):
    name: str
    description: str
    location: str


class Options(BaseModel):
    name: str
    description: str
    price: float
    restaurant_id: str


# Rota para criar um novo restaurante
@app.post("/restaurants/", response_model=Restaurant)
async def create_restaurant(restaurant: Restaurant):
    try:
        restaurant_data = restaurant.dict()
        restaurant_ref = db.collection("restaurantes").add(restaurant_data)
        return restaurant_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.get("/restaurants/")
async def get_all_restaurants():
    try:
        restaurantes_ref = db.collection("restaurantes")
        restaurantes = restaurantes_ref.stream()


        lista_de_restaurantes = []

        for restaurante in restaurantes:
            dados_do_restaurante = restaurante.to_dict()
            dados_do_restaurante['id'] = restaurante.id
            lista_de_restaurantes.append(dados_do_restaurante)

        return lista_de_restaurantes
    except Exception as e:
        return {"erro": str(e)}


@app.get("/restaurants/{restaurant_name}")
async def get_restaurant_by_name(restaurant_name: str):
    try:
        restaurantes_ref = db.collection("restaurantes")
        query = restaurantes_ref.where("name", "==", restaurant_name)
        resultados = query.stream()

        for resultado in resultados:
            return resultado.to_dict()

        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.post("/options/", response_model=Options)
async def create_food_option(option: Options):
    try:
        option_data = option.model_dump()
        option_ref = db.collection("opcoes_De_pratos").add(option_data)
        return option_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get('/food_for_restaurant/{id}')
async def get_foods_by_restaurant(id: str):
    try:
        foods_ref = db.collection('opcoes_De_pratos')
        query = foods_ref.where("restaurant_id", "==", id)
        resultados = query.stream()

        for resultado in resultados:
            return resultado.to_dict()


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))










