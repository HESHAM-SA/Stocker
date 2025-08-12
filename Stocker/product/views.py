from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Product, Category, Supplier
from .forms import ProductForm, CategoryForm, SupplierForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages



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





@login_required
def stock_management_view(request: HttpRequest) -> HttpResponse:
    """A view to display all products and update their stock levels."""

    # Handle the POST request when a user updates stock
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        product = get_object_or_404(Product, pk=product_id)

        if action == 'increase':
            product.stock_quantity += 1
            messages.success(request, f"Increased stock for {product.product_name}.")
        elif action == 'decrease':
            if product.stock_quantity > 0:
                product.stock_quantity -= 1
                messages.success(request, f"Decreased stock for {product.product_name}.")
            else:
                messages.error(request, f"{product.product_name} is already out of stock.")
        
        product.save()
        return redirect('product:stock_management_view')

    # Handle the GET request to display the page
    products = Product.objects.all().order_by('product_name')
    context = {'products': products}
    return render(request, 'product/stock_management.html', context)


@login_required
def inventory_report_view(request: HttpRequest) -> HttpResponse:
    """A view to display inventory reports."""
    
    # Define your low stock threshold
    LOW_STOCK_THRESHOLD = 10

    total_products = Product.objects.count()
    # Use Sum to get the total number of items across all products
    total_stock_items = Product.objects.aggregate(total=Sum('stock_quantity'))['total'] or 0

    # Get lists of products based on stock status
    low_stock_products = Product.objects.filter(stock_quantity__gt=0, stock_quantity__lte=LOW_STOCK_THRESHOLD)
    out_of_stock_products = Product.objects.filter(stock_quantity=0)

    context = {
        'total_products': total_products,
        'total_stock_items': total_stock_items,
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
    }
    return render(request, 'product/inventory_report.html', context)
