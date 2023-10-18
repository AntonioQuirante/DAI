from django.http import HttpResponse
from models import Product
import textwrap
from pymongo import MongoClient
import requests
from pprint import pprint
import os


client = MongoClient('mongo', 27017)
tienda_db = client.tienda
productos_collection = tienda_db.productos

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def getProductos(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Lanza una excepción si la solicitud no es exitosa (código de estado no 2xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API: {e}")
        return None

def empty_database():
    productos_collection.drop()

def download_image(url, id):
    response = requests.get(url)
    if response.status_code == 200:

        file_name = f'img_{id}.jpg'
        file_path = os.path.join('images', file_name)

        with open(file_path, 'wb') as file:
            file.write(response.content)

        return file_path
    else:
        return None

def insert(productos):
    for producto in productos:
        product = Product(**producto)
        product.image = download_image(producto.get('image'), producto.get('id'))
        productos_collection.insert_one(product.model_dump())

def find_between_price_range(min_price, max_price, category):
    products = productos_collection.find({
        "category": category,
        "price": {"$gte": min_price, "$lte": max_price}
    }).sort("price", 1)
    return list(products)

def find_products(keyword):
    products = productos_collection.find({
        "description": {"$regex": keyword, "$options": "i"}
    })
    return list(products)

def products_rating(m_rating):
    products = productos_collection.find({
        "rating.rate": {"$gt": m_rating}
    })
    return list(products)

def mens_clothing_by_rating():
    products = productos_collection.find({
        "category": "men's clothing",
    }).sort("rating.rate", -1)
    return list(products)

def calculate_total():
    total = productos_collection.aggregate([
        {"$group": {"_id": "_id", "total": {"$sum": "$price"}}}
    ])
    return list(total)[0]["total"]

def calculate_by_category():
    revenue = productos_collection.aggregate([
        {"$group": {"_id": "$category", "total": {"$sum": "$price"}}}
    ])
    return list(revenue)



