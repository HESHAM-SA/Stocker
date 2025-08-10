from django.urls import path
from . import views 

app_name = 'product'

urlpatterns = [
    path("all/", views.product_list_view, name='product_list_view'),
    path("add/", views.add_new_product, name='add_new_product'),
    path("delete/<int:product_id>", views.delete_product, name='delete_product'),
    path("update/<int:product_id>", views.update_product, name='update_product'),
    path("details/<int:product_id>", views.show_product_details, name='show_product_details'),
    
]