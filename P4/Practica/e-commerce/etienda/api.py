from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja.files import UploadedFile
from ninja import Schema
from bson.objectid import ObjectId
from django.shortcuts import get_object_or_404
from .models import Product
import textwrap
from pymongo import MongoClient
import requests
import logging
from typing import Optional, Any, List

api = NinjaExtraAPI()
client = MongoClient('mongo', 27017)
tienda_db = client.tienda
productos_collection = tienda_db.productos

logger = logging.getLogger(__name__)


class Rate(Schema):
    rate: float
    count: int


class ProductSchema(Schema):  # sirve para validar y para documentación
    _id: str
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

class ProductSchemaNew(Schema):
    id: Optional[str]
    title: str
    price: float
    description: str
    category: str
    rating: Rate


class PaginatedProductListResponse(Schema):
    items: list[ProductSchema]
    total_items: int
    total_pages: int
    page: int

class AllProductsResponse(Schema):
    items: List[ProductSchema]

class ErrorSchema(Schema):
    message: str

def busca_prod(product_id):

    product_object_id = ObjectId(product_id)
    product = productos_collection.find_one({'_id': product_object_id})
    logger.debug(f"Product details before update: {product}")
    return product

def generate_random_id(length=12):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

@api.put("/productos/rate/{id}", tags=['TIENDA DAI'], response={200: Rate, 404: ErrorSchema}) #cambia la base de datos aunque devuelva error
def mod_product(request, id: str, payload: Rate):
    try:
        logger.info(f"Received PUT request for product with ID: {id}")

        # Retrieve the product
        product = busca_prod(id)

        logger.debug(f"Product details before update: {product}")
        logger.debug(payload.dict())

        # Specify allowed fields to update
        allowed_fields = ['rate', 'count']
        rating = {'rate': 0, 'count': 0}
        # Update allowed fields from the payload
        for field, value in payload.dict().items():
            if field in allowed_fields:
                try:
                    rating[field] = type(rating[field])(value)
                except Exception as e:
                    logger.error(f"Error setting attribute {field}: {e}")

        product['rating'] = rating
        logger.debug(f"Product details after update: {product}")

        # Replace the product in the database
        productos_collection.replace_one({'_id': product['_id']}, product)

        logger.info(f"Product with ID {id} successfully updated")

        return 200
    except Exception as e:
        logger.error(f"Error updating product: {str(e)}")
        return 404, {'message': 'no encontrado'}

@api.post("/productos", tags=['TIENDA DAI'], response={201: ProductSchema, 400: ErrorSchema})
def add_product(request, payload: ProductSchemaNew):
    try:
        logger.info("Received POST request to add a product")

        # Create a new Product instance using the payload
        new_product = Product(**payload.dict())

        # Save the new product to the database
        result = productos_collection.insert_one(new_product.dict())

        # Get the inserted product ID
        new_product_id = result.inserted_id

        # Add the product ID to the response
        payload.id = str(new_product_id)

        logger.info(f"Product added with ID: {new_product_id}")

        return 201, payload
    except Exception as e:
        logger.error(f"Error adding product: {e}")
        return 400, {'message': 'Error al intentar añadir el producto'}

@api.get("/productos", tags=['TIENDA DAI'], response={200: PaginatedProductListResponse})
def get_product_list(request, desde: int = 0, hasta: int = 10):
    try:
        logger.info(f"Received GET request for products with pagination: desde={desde}, hasta={hasta}")

        # Retrieve the paginated list of products
        products = productos_collection.find().skip(desde).limit(hasta - desde)

        # Convert the MongoDB documents to a list of ProductSchema
        product_list = [ProductSchema(**product) for product in products]

        # Get the total number of items and calculate total pages
        total_items = productos_collection.count_documents({})
        total_pages = (total_items + hasta - 1) // hasta

        # Create the paginated response
        response = PaginatedProductListResponse(
            items=product_list,
            total_items=total_items,
            total_pages=total_pages,
            page=(desde // hasta) + 1
        )

        return 200, response
    except:
        return 500, {'message': 'Error al intentar obtener la lista de productos paginada'}


@api.get("/products", tags=['TIENDA DAI'], response=List[ProductSchema])
def get_all_products(request):
        try:
            logger.info(f"Received GET request for products")
            products = productos_collection.find()
            product_list = [ProductSchema(**product) for product in products]

            return 200, product_list
        except:
            return 500, {'message': 'Error al intentar obtener la lista de productos'}


@api.get("/productos/{id}", tags=['TIENDA DAI'], response={200: ProductSchema, 404: ErrorSchema}) #funciona perfe
def get_product(request, id: str):
    try:
        # Log the request information
        logger.info(f"Received GET request for product with ID: {id}")
        # Retrieve the product
        product = busca_prod(id)
        # Log the product details
        logger.debug(f"Product details: {product}")

        return 200, product
    except:
        return 404, {'message': 'No encontrado'}


@api.put("/productos/{id}", tags=['TIENDA DAI'], response={200: ProductSchema, 404: ErrorSchema}) #cambia la base de datos aunque devuelva error
def mod_product(request, id: str, payload: ProductSchemaIn):
    try:
        logger.info(f"Received PUT request for product with ID: {id}")

        # Retrieve the product
        product = busca_prod(id)

        logger.debug(f"Product details before update: {product}")
        logger.debug(payload.dict())
        # Specify allowed fields to update
        allowed_fields = ['title', 'price', 'description', 'category', 'rating']

        # Update allowed fields from the payload
        for field, value in payload.dict().items():
            if field in allowed_fields:
                try:
                    product[field] = value
                    logger.debug(f'{field} -> {value}')
                except Exception as e:
                    logger.error(f"Error setting attribute {field}: {e}")

        logger.debug(f"Product details after update: {product}")

        # Replace the product in the database
        productos_collection.replace_one({'_id': product['_id']}, product)

        logger.info(f"Product with ID {id} successfully updated")

        return 200
    except Exception as e:
        logger.error(f"Error updating product: {str(e)}")
        return 404, {'message': 'no encontrado'}


# function based definition
@api.get("/add", tags=['Math'])
def add(request, a: int, b: int):
    return {"result": a + b}


@api.delete("/productos/{id}", tags=['TIENDA DAI'], response={200: None, 404: ErrorSchema}) #Funciona
def delete_product(request, id: str):
    try:
        logger.info(f"Received DELETE request for product with ID: {id}")

        product_object_id = ObjectId(id)
        product = productos_collection.find_one({'_id': product_object_id})
        if not product:
            return 404, {'message': 'Producto no encontrado'}

        # Delete the product from the collection
        productos_collection.delete_one({'_id': product_object_id})

        logger.info(f"Product with ID {id} successfully deleted")

        return 200  # No content response for successful deletion
    except:
        return 404, {'message': 'Error al intentar eliminar el producto'}



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
