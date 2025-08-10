from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Product
from django.db.models import Q

# Create your views here.

def home_view(request: HttpRequest) -> HttpResponse:
    '''DashBoard of category vs products and supplies vs products and 
    total of products, categorys, stock and supplies,
    and have filters of category and suppliers 
    '''
    return render(request, 'product/home.html')



def product_list_view(request: HttpRequest) -> HttpResponse:
    """--- here search and disply all products ---"""
    search_query = request.GET.get('search', '')
    products = Product.objects.all()
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)

    context = {'products':products, 'search_query':search_query}
    return render(request, 'product/all_products.html',context)


def add_new_product(request: HttpRequest) -> HttpResponse:
    pass

def delete_product(request: HttpRequest) -> HttpResponse:
    pass

def update_product(request: HttpRequest) -> HttpResponse:
    pass

def show_details_product(request: HttpRequest) -> HttpResponse:
    pass
