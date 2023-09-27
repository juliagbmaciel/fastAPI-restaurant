from pydantic import BaseModel

class RestaurantesModel(BaseModel):
    nome: str
    descricao: str
    local: str
    imagem: str
    avaliacao: int