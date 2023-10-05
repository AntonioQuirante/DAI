# Main.py
from pydantic import BaseModel, FilePath, Field, EmailStr
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import Controllers.Controller as _client
import requests
import os

#Lo primero que voy a hacer es

api_url = 'https://fakestoreapi.com/products'
print("Borrando toda la tienda...")
_client.empty_database()

print("Obteniendo datos desde la API...")
productos = _client.getProductos(api_url) #obtenemos todos los productos de la api
print("Insertando datos a la base de datos...")
_client.insert(productos)

print("  ")
print("  ")
print("  ")
print("  ")
print("Electrónica entre 100 y 200€, ordenados por precio...")
print(_client.find_between_price_range(100,200,"electronics"))

print("  ")
print("  ")
print("  ")
print("  ")
print("Productos que contengan la palabra 'pocket' en la descripción")
print(_client.find_products("pocket"))

print("  ")
print("  ")
print("  ")
print("  ")
print("Productos con puntuación mayor de 4")
print(_client.products_rating(4))

print("  ")
print("  ")
print("  ")
print("  ")
print("Ropa de hombre ordenada por puntuación")
print(_client.mens_clothing_by_rating())

print("  ")
print("  ")
print("  ")
print("  ")
print("Facturación total")
print(_client.calculate_total())

print("  ")
print("  ")
print("  ")
print("  ")
print("Facturación por categoría de producto")
print(_client.calculate_by_category())