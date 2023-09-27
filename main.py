from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import Restaurantes
from db import Pratos
from models import RestaurantesModel
from db import engine
from sqlalchemy.orm import Session


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




#
# restaurantes = [
#     {
#         "nome": "Jangada Restaurante",
#         "descricao": "Restaurante bom da peste",
#         "local": "Campinas - SP",
#         "avaliacao": 5,
#         "image": "https://www.restaurantejangada.com.br/wp-content/uploads/2019/06/campinas3-1024x683.jpg",
#         "id": 1
#     },
#      {
#         "nome": "Jangada Restaurante 2",
#         "descricao": "Restaurante bom da peste",
#         "local": "Campinas - SP",
#         "avaliacao": 5,
#         "image": "https://www.restaurantejangada.com.br/wp-content/uploads/2019/06/campinas3-1024x683.jpg",
#          "id": 2
#     }
# ]

# pratos = [
#     {
#         "nome": "Prato tal",
#         "descricao": "desc tal",
#         "preco": 20.00,
#         "id_restaurante": 1
#     },
#     {
#         "nome": "Prato tal",
#         "descricao": "desc tal",
#         "preco": 20.00,
#         "id_restaurante": 2
#     }
#
# ]


@app.get('/restaurants')
async def get_restaurants():
    restaurantes = session.query(Restaurantes).all()
    return restaurantes


@app.get('/restaurant/{id}')
async def get_restaurant_by_id(id: int):
    print(id)
    restaurante = session.query(Restaurantes).filter_by(id = id).first()
    print(restaurante)
    return restaurante



# @app.get('/food')
# async def get_foods():
#     pratos = session.query(Pratos).all()
#     return pratos


# @app.get('/restaurant/{id_restaurant}/food/{id_food}')
# async def get_food_by_rest_by_idfood(id_restaurant: int, id_food: int):
#     prato_correto = ''
#     for prato in pratos.items():
#         if prato[1]['id_restaurante'] == id_restaurant:
#             if prato[0] == id_food:
#                 prato_correto = prato
#
#     return prato_correto



@app.post('/create_restaurant')
async def create_restaurant(restaurante: RestaurantesModel):
    try:
        novo_restaurante= Restaurantes(nome=restaurante.nome, descricao=restaurante.descricao, local=restaurante.local,
                                       imagem=restaurante.imagem, avaliacao=restaurante.avaliacao)

        session.add(novo_restaurante)
        session.commit()

        return restaurante
    except:
        return "Algo deu errado"






if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host='127.0.0.1', port=8001, log_level="info", reload=True)