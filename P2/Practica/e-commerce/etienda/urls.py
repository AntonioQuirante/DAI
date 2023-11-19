from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('upload/', views.upload_product, name='upload_product'),
    path('category/<str:category>/', views.category_index, name='category_index'),
    path('search/', views.search, name='search_results'),


    #path('get-productos/', views.insert, name='get_productos'),
    #path('empty-database/', views.empty_database, name='empty_database'),
    #path('find-products/<str:keyword>/', views.find_products, name='find_products'),
    #path('find-between-price-range/<int:min_price>/<int:max_price>/<str:category>/', views.find_between_price_range, name='find_between_price_range'),
    #path('products-rating/<int:m_rating>/', views.products_rating, name='products_rating'),
    #path('mens-clothing-by-rating/', views.mens_clothing_by_rating, name='mens_clothing_by_rating'),
    #path('calculate-total/', views.calculate_total, name='calculate_total'),
    #path('calculate-by-category/', views.calculate_by_category, name='calculate_by_category'),
]