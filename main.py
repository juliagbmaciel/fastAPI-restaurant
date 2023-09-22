from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ["*"]  # "*" permite solicitações de qualquer origem. Você pode ajustar isso para permitir apenas origens específicas.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Isso permite todos os métodos HTTP (GET, POST, PUT, etc.).
    allow_headers=["*"],  # Isso permite todos os cabeçalhos HTTP.
)


restaurantes = [
    {
        "nome": "Jangada Restaurante",
        "descricao": "Restaurante bom da peste",
        "local": "Campinas - SP",
        "avaliacao": 5,
        "image": "https://www.restaurantejangada.com.br/wp-content/uploads/2019/06/campinas3-1024x683.jpg",
        "id": 1
    },
     {
        "nome": "Jangada Restaurante 2",
        "descricao": "Restaurante bom da peste",
        "local": "Campinas - SP",
        "avaliacao": 5,
        "image": "https://www.restaurantejangada.com.br/wp-content/uploads/2019/06/campinas3-1024x683.jpg",
         "id": 2
    }
]

pratos = [
    {
        "nome": "Prato tal",
        "descricao": "desc tal",
        "preco": 20.00,
        "id_restaurante": 1
    },
    {
        "nome": "Prato tal",
        "descricao": "desc tal",
        "preco": 20.00,
        "id_restaurante": 2
    }

]


@app.get('/restaurants')
async def get_restaurants():
    for rest in restaurantes:
        print(rest)
    return restaurantes


@app.get('/restaurant/{id}')
async def get_restaurant_by_id(id: int):
    restaurante = ''
    for rest in restaurantes.items():
        if rest[0] == id:
            restaurante = rest
    return restaurante



@app.get('/food/{id}')
async def get_food_by_restaurant(id: int):
    lista_pratos = []
    for prato in pratos.values():
        if prato['id_restaurante'] == id:
            lista_pratos.append(prato)
    return lista_pratos


@app.get('/restaurant/{id_restaurant}/food/{id_food}')
async def get_food_by_rest_by_idfood(id_restaurant: int, id_food: int):
    prato_correto = ''
    for prato in pratos.items():
        if prato[1]['id_restaurante'] == id_restaurant:
            if prato[0] == id_food:
                prato_correto = prato

    return prato_correto






if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host='127.0.0.1', port=8001, log_level="info", reload=True)
