from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from bson import json_util
from .models import Product
import textwrap
from pymongo import MongoClient
import requests
from pprint import pprint
import os
import logging

from .forms import ProductoForm

client = MongoClient('mongo', 27017)
tienda_db = client.tienda
productos_collection = tienda_db.productos

logger = logging.getLogger(__name__)


def get_last_object_id():
    # Ordenar los objetos por _id en orden descendente y obtener el ID del primer documento
    last_object = productos_collection.find_one({}, sort=[('_id', -1)])
    if last_object:
        return int(last_object['_id'].generation_time.timestamp())
    return None  # Manejar el caso en el que no haya documentos en la colección


def upload_product(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = ProductoForm(request.POST, request.FILES)

            if form.is_valid():
                title = form.cleaned_data['nombre']
                price = form.cleaned_data['precio']
                description = form.cleaned_data['descripcion']
                category = form.cleaned_data['categoria']
                # image = form.cleaned_data['imagen']
                logger.debug(title, price, description, category)
                # Create JSON to upload to the database
                product_data = {
                    'title': title,
                    'price': price,
                    'description': description,
                    'category': category,
                    'rating': {
                        'rate': 0,
                        'count': 1
                    }
                }

                # You mentioned getting the last ID from the database for an incremented ID.
                # Here, use your logic to fetch the last ID.
                # last_id = 22

                product = Product(**product_data)
                # product.image = insert_image(image, last_id)  # Assuming insert_image is a function you've defined elsewhere
                productos_collection.insert_one(
                    product.model_dump())  # Assuming productos_collection is your database collection
                # Redirect to the homepage
                categories = productos_collection.distinct('category')
                return render(request, "index.html", {'categories': categories})
        else:
            form = ProductoForm()

        return render(request, 'upload_product.html', {'form': form})
    else:
        return HttpResponse("No tienes permisos para acceder a esta página.")


def index(request):
    categories = productos_collection.distinct('category')
    return render(request, "index.html", {'categories': categories})


def category_index(request, category):
    categories = productos_collection.distinct('category')
    products = productos_collection.find({
        "category": {"$regex": category}
    })
    return render(request, "category.html", {'products': products, 'categories': categories})


def search(request):
    categories = productos_collection.distinct('category')
    query = request.GET.get('q')
    if query:
        results = productos_collection.find({
            "title": {"$regex": query}
        })
    else:
        results = None
    return render(request, 'search.html', {'results': results, 'categories': categories})


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

        os.makedirs('static/images', exist_ok=True)

        file_name = f'img_{id}.jpg'
        file_path = os.path.join('static/images', file_name)

        with open(file_path, 'wb') as file:
            file.write(response.content)

        return file_path
    else:
        return None


def insert_image(image, id):
    if image:
        os.makedirs('static/images', exist_ok=True)

        file_name = f'img_{id}.jpg'
        file_path = os.path.join('static/images', file_name)

        with open(file_path, 'wb') as file:
            file.write(image)

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
