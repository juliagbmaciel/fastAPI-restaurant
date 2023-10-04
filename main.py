from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Restaurantes
from models import Pratos
from schemas import RestaurantesModel, PratosModel
from models import engine
from sqlalchemy.orm import Session
import requests

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session = Session(bind=engine)


@app.get('/')
async def initial():
    return "Bem vindo a minha API :)"

@app.get('/api/restaurants')
async def get_restaurants():
    restaurantes = session.query(Restaurantes).all()
    return restaurantes


@app.get('/api/restaurants/restaurant/{id}')
async def get_restaurant_by_id(id: int):
    restaurante = session.query(Restaurantes).filter_by(id = id).first()

    if not restaurante:
        raise HTTPException(status_code=404, detail=f"Restaurante com o id {id} não foi encontrado!")
    
    return restaurante


@app.post('/api/restaurants/restaurant')
async def create_restaurant(restaurante: RestaurantesModel):
    novo_restaurante= Restaurantes(nome=restaurante.nome, descricao=restaurante.descricao, local=restaurante.local,
                                    imagem=restaurante.imagem, avaliacao=restaurante.avaliacao)

    session.add(novo_restaurante)
    session.commit()
    session.refresh(novo_restaurante)

    return restaurante



@app.put('/api/restaurants/restaurant/{id}')
async def update_restaurant(id: int, restaurante: RestaurantesModel):
    global restaurante_atualizado
    restaurante_banco = session.query(Restaurantes).get(id)
    
    if restaurante_banco:
        atributos_para_atualizar = ['nome', 'descricao', 'avaliacao', 'local', 'imagem']
        for atributo in atributos_para_atualizar:
            setattr(restaurante_banco, atributo, getattr(restaurante, atributo))
        
        session.commit()

        restaurante_atualizado = session.query(Restaurantes).get(id)
    
    if not restaurante_banco:
        raise HTTPException(status_code=404, detail=f"restaurante com o id {id} não encontrado")


    return restaurante_atualizado



@app.get('api/foods/food')
async def get_all_foods():
    pratos = session.query(Pratos).all()
    return pratos


@app.get('api/foods/food/{id}')
async def get_foods(id: int):
    prato = session.query(Pratos).filter_by(id = id).first()

    if not prato:
        raise HTTPException(status_code=404, detail=f"Prato com o id {id} não foi encontrado!")
    
    return prato
    

@app.post('api/foods/food')
async def create_food(prato: PratosModel):
    novo_prato= Pratos(nome=prato.nome, descricao=prato.descricao, preco=prato.preco,
                                    id_restaurante=prato.id_restaurante)

    session.add(novo_prato)
    session.commit()
    session.refresh(novo_prato)

    return novo_prato

@app.get('api/foods/food_by_restaurant/{id}')
async def food_by_restaurant(id: int):
    prato = session.query(Pratos).filter_by(id_restaurante = id).all()

    if not prato:
        raise HTTPException(status_code=404, detail=f"Restaurante com o id {id} não foi encontrado!")

    return prato

@app.get('api/foods/calorie_per_food/{food}')
async def calorie_per_food(food: str):
    url = f"https://caloriasporalimentoapi.herokuapp.com/api/calorias/?descricao={food}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "A requisição falhou com o código de status:", response.status_code

@app.get('api/quiz/{num}')
async def get_one_question(num: int):
    url = f"http://192.168.88.114:8000/questions/{num}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "A requisição falhou com o código de status:", response.status_code



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="info", reload=True)