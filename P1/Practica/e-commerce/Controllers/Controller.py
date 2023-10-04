from Models.Product import Product
import textwrap
from pymongo import MongoClient
import requests
from pprint import pprint


client = MongoClient('mongo', 27017)
tienda_db = client.tienda
productos_collection = tienda_db.productos

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

def insert(productos):
    for producto in productos:
        product = Product(**producto)
        productos_collection.insert_one(product.model_dump())

def find_between_price_range(min_price, max_price, category):
    products = productos_collection.find({
        "category": category,
        "price": {"$gte": min_price, "$lte": max_price}
    }).sort("price", 1)
    return list(products)

def find_products_with_keyword(keyword):
    products = productos_collection.find({
        "description": {"$regex": keyword, "$options": "i"}
    })
    return list(products)

def find_products_with_rating(min_rating):
    products = productos_collection.find({
        "rating.rate": {"$gt": min_rating}
    })
    return list(products)

def find_mens_clothing_sorted_by_rating():
    products = productos_collection.find({
        "category": "men's clothing",
    }).sort("rating.rate", -1)
    return list(products)

def calculate_total_revenue():
    total_revenue = productos_collection.aggregate([
        {"$group": {"_id": "_id", "total": {"$sum": "$price"}}}
    ])
    return list(total_revenue)[0]["total"]

def calculate_revenue_by_category():
    revenue_by_category = productos_collection.aggregate([
        {"$group": {"_id": "$category", "total": {"$sum": "$price"}}}
    ])
    return list(revenue_by_category)



