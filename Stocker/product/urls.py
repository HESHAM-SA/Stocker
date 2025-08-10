from django.urls import path
from . import views 

app_name = 'product'

urlpatterns = [
    path("",views.home_view, name='home_view'),
    path("products/", views.product_list_view, name='product_list_view'),
]