from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Product, Category
from django.db.models import Q
from .forms import ProductForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required 
def product_list_view(request: HttpRequest) -> HttpResponse:
    """--- here search and disply all products ---"""
    search_query = request.GET.get('search', '')
    products = Product.objects.all()
    if search_query:
        products = Product.objects.filter(product_name__icontains=search_query)

    context = {'products':products, 'search_query':search_query}
    return render(request, 'product/all_products.html',context)




def add_new_product(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product:product_list_view')
    else:
        form = ProductForm()
    context = {'form':form}
    return render(request, 'product/form_add_new_product.html', context)



def delete_product(request: HttpRequest, product_id) -> HttpResponse:
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect('product:product_list_view')




def update_product(request: HttpRequest, product_id) -> HttpResponse:
    """update values of this product"""
    product = get_object_or_404(Product ,pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product:product_list_view')
    else:
        form = ProductForm(instance=product)
    context = {'form':form, 'product':product}
    return render(request, 'product/update_product.html', context)



def show_product_details(request: HttpRequest, product_id) -> HttpResponse:
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product/product_details.html',{'product':product})