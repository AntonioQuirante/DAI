from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('get-productos/', views.getProductos, name='get_productos'),
    path('empty-database/', views.empty_database, name='empty_database'),
    path('find-products/<str:keyword>/', views.find_products, name='find_products'),
    # Add more URL patterns for other views as needed
]