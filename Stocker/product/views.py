from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Product, Category, Supplier
from django.db.models import Q
from .forms import ProductForm, CategoryForm, SupplierForm
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





# ========================================================
# CATEGORY VIEWS (Following your existing simple style)
# ========================================================

@login_required
def category_list_view(request: HttpRequest) -> HttpResponse:
    """Displays a list of all categories."""
    categories = Category.objects.all()
    return render(request, 'product/category_list.html', {'categories': categories})

@login_required
def add_new_category(request: HttpRequest) -> HttpResponse:
    """Handles creating a new category, same as add_new_product."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product:category_list_view')
    else:
        form = CategoryForm()
    return render(request, 'product/category_form.html', {'form': form})

@login_required
def update_category(request: HttpRequest, category_id: int) -> HttpResponse:
    """Handles updating a category, same as update_product."""
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('product:category_list_view')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'product/category_form.html', {'form': form, 'category': category})

@login_required
def delete_category(request: HttpRequest, category_id: int) -> HttpResponse:
    """Handles deleting a category, same as delete_product."""
    # WARNING: If a product is using this category, this will cause an error
    # because of 'on_delete=models.PROTECT'. You must handle this error.
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    return redirect('product:category_list_view')


# =========================================================
# SUPPLIER VIEWS (Following your existing simple style)
# =========================================================

@login_required
def supplier_list_view(request: HttpRequest) -> HttpResponse:
    """Displays a list of all suppliers."""
    suppliers = Supplier.objects.all()
    return render(request, 'product/supplier_list.html', {'suppliers': suppliers})

@login_required
def show_supplier_details(request: HttpRequest, supplier_id: int) -> HttpResponse:
    """Shows details for one supplier and the products they supply."""
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    products = supplier.product_set.all()  # Gets all products linked to this supplier
    return render(request, 'product/supplier_detail.html', {'supplier': supplier, 'products': products})

@login_required
def add_new_supplier(request: HttpRequest) -> HttpResponse:
    """Handles creating a new supplier."""
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product:supplier_list_view')
    else:
        form = SupplierForm()
    return render(request, 'product/supplier_form.html', {'form': form})

@login_required
def update_supplier(request: HttpRequest, supplier_id: int) -> HttpResponse:
    """Handles updating a supplier."""
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('product:supplier_detail_view', supplier_id=supplier.id)
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'product/supplier_form.html', {'form': form, 'supplier': supplier})

@login_required
def delete_supplier(request: HttpRequest, supplier_id: int) -> HttpResponse:
    """Handles deleting a supplier."""
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    supplier.delete()
    return redirect('product:supplier_list_view')