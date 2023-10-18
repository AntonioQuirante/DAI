from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from bson import json_util
from .models import Product
import textwrap
from pymongo import MongoClient
import requests
from pprint import pprint
import os

client = MongoClient('mongo', 27017)
tienda_db = client.tienda
productos_collection = tienda_db.productos


def index(request):
    return render(request, "index.html", context=None, content_type=None, status=None, using=None)


def getProducts(api_url='https://fakestoreapi.com/products'):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Lanza una excepción si la solicitud no es exitosa (código de estado no 2xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API: {e}")
        return None


def empty_database(request):
    productos_collection.drop()
    response_data = {
        'message': 'Base de datos borrada'
    }
    return JsonResponse(response_data)


def download_image(url, id):
    response = requests.get(url)
    if response.status_code == 200:

        os.makedirs('images', exist_ok=True)

        file_name = f'img_{id}.jpg'
        file_path = os.path.join('images', file_name)

        with open(file_path, 'wb') as file:
            file.write(response.content)

        return file_path
    else:
        return None


def insert(request):
    products = getProducts()
    for producto in products:
        product = Product(**producto)
        product.image = download_image(producto.get('image'), producto.get('id'))
        productos_collection.insert_one(product.model_dump())
    response_data = {
        'message': 'Datos Insertados'
    }
    return JsonResponse(response_data)


def find_between_price_range(request, min_price, max_price, category):
    products = productos_collection.find({
        "category": category,
        "price": {"$gte": min_price, "$lte": max_price}
    }).sort("price", 1)

    product_list = list(products)
    response_data = {
        'message': json_util.dumps(product_list)
    }
    return JsonResponse(response_data, safe=False)


def find_products(request, keyword):
    products = productos_collection.find({
        "description": {"$regex": keyword, "$options": "i"}
    })

    product_list = list(products)
    response_data = {
        'message': json_util.dumps(product_list)
    }
    return JsonResponse(response_data, safe=False)


def products_rating(request, m_rating):
    products = productos_collection.find({
        "rating.rate": {"$gt": m_rating}
    })
    product_list = list(products)
    response_data = {
        'message': json_util.dumps(product_list)
    }
    return JsonResponse(response_data, safe=False)


def mens_clothing_by_rating(request):
    products = productos_collection.find({
        "category": "men's clothing",
    }).sort("rating.rate", -1)

    product_list = list(products)
    response_data = {
        'message': json_util.dumps(product_list)
    }
    return JsonResponse(response_data, safe=False)


def calculate_total(request):
    total = productos_collection.aggregate([
        {"$group": {"_id": "_id", "total": {"$sum": "$price"}}}
    ])
    product_list = list(total)
    response_data = {
        'message': json_util.dumps(product_list)
    }
    return JsonResponse(response_data, safe=False)


def calculate_by_category(request):
    revenue = productos_collection.aggregate([
        {"$group": {"_id": "$category", "total": {"$sum": "$price"}}}
    ])

    product_list = list(revenue)
    response_data = {
        'message': json_util.dumps(product_list)
    }
    return JsonResponse(response_data, safe=False)
