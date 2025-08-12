from django.urls import path
from . import views 

app_name = 'product'

urlpatterns = [
    path("all/", views.product_list_view, name='product_list_view'),
    path("add/", views.add_new_product, name='add_new_product'),
    path("delete/<int:product_id>", views.delete_product, name='delete_product'),
    path("update/<int:product_id>", views.update_product, name='update_product'),
    path("details/<int:product_id>", views.show_product_details, name='show_product_details'),

    # --- New Category URLs ---
    path("categories/", views.category_list_view, name='category_list_view'),
    path("category/add/", views.add_new_category, name='add_new_category'),
    path("category/update/<int:category_id>", views.update_category, name='update_category'),
    path("category/delete/<int:category_id>", views.delete_category, name='delete_category'),

    # --- New Supplier URLs ---
    path("suppliers/", views.supplier_list_view, name='supplier_list_view'),
    path("supplier/add/", views.add_new_supplier, name='add_new_supplier'),
    path("supplier/details/<int:supplier_id>", views.show_supplier_details, name='show_supplier_details'),
    path("supplier/update/<int:supplier_id>", views.update_supplier, name='update_supplier'),
    path("supplier/delete/<int:supplier_id>", views.delete_supplier, name='delete_supplier'),

    # ... stock 
    path("stock-management/", views.stock_management_view, name='stock_management_view'),
    # ... inventory 
    path("reports/inventory/", views.inventory_report_view, name='inventory_report_view'),
]
