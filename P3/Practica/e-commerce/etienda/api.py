from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja import Schema
from bson.objectid import ObjectId

api = NinjaExtraAPI()


class Rate(Schema):
    rate: float
    count: int


class ProductSchema(Schema):  # sirve para validar y para documentación
    id: str
    title: str
    price: float
    description: str
    category: str
    image: str = None
    rating: Rate


class ProductSchemaIn(Schema):
    title: str
    price: float
    description: str
    category: str
    rating: Rate


class ErrorSchema(Schema):
    message: str









# function based definition
@api.get("/add", tags=['Math'])
def add(request, a: int, b: int):
    return {"result": a + b}


# class based definition
@api_controller('/', tags=['Math'], permissions=[])
class MathAPI:

    @http_get('/subtract', )
    def subtract(self, a: int, b: int):
        """Subtracts a from b"""
        return {"result": a - b}

    @http_get('/divide', )
    def divide(self, a: int, b: int):
        """Divides a by b"""
        return {"result": a / b}

    @http_get('/multiple', )
    def multiple(self, a: int, b: int):
        """Multiples a with b"""
        return {"result": a * b}


api.register_controllers(
    MathAPI
)
