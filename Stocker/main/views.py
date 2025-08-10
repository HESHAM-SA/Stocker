from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.

def home_view(request: HttpRequest) -> HttpResponse:
    '''DashBoard of category vs products and supplies vs products and 
    total of products, categorys, stock and supplies,
    and have filters of category and suppliers 
    '''
    return render(request, 'main/home.html')