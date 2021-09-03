from django.urls import path, include, re_path
from django.views.generic import TemplateView

from items.views import ProductListView, DetailView, ProductDetailView, SupplierListView, SupplierDetailView, \
    actionview, CustomerListView, CustomerDetailView, objectsalesview, ProductCategoryListView, \
    ProductCategoryDetailView, ProductSubCategoryListView, objectforecastview, ProductSubCategoryDetailView, \
    ImportProducts, UpdateAttributes, SettingsView, \
    UpdateForecast, Optimize
from django.views import static

app_name = 'items'
urlpatterns = [
    path('items/', ProductListView.as_view(), name='Products'),
    path('items/<int:pk>/details/', ProductDetailView.as_view(), name='Product Details'),
    path('items/<int:pk>/', ProductDetailView.as_view()),
    path('suppliers/', SupplierListView.as_view(), name='Suppliers'),
    path('customers/', CustomerListView.as_view(), name='Customers'),
    path('action/', actionview, name='Action'),
    path('itemcategories/', ProductCategoryListView.as_view(), name='Product Categories'),
    path('itemcategories/<int:pk>/details/', ProductCategoryDetailView.as_view(), name='Product Categories Details'),
    path('itemcategories/<int:pk>/', ProductCategoryDetailView.as_view()),
    path('itemsubcategories/', ProductSubCategoryListView.as_view(), name='Product SubCategories'),
    path('itemsubcategories/<int:pk>/details/', ProductSubCategoryDetailView.as_view(), name='Product SubCategory Details'),
    path('itemsubcategories/<int:pk>/', ProductSubCategoryDetailView.as_view()),
    path('suppliers/<int:pk>/details/', SupplierDetailView.as_view(), name='Supplier Details'),
    path('suppliers/<int:pk>/', SupplierDetailView.as_view()),
    path('customers/<int:pk>/details/', CustomerDetailView.as_view(), name='Customer Details'),
    path('customers/<int:pk>/sales/', objectsalesview, name='Customer Sales Analysis'),
    path('suppliers/<int:pk>/sales/', objectsalesview, name='Supplier Sales Analysis'),
    path('itemsubcategories/<int:pk>/sales/', objectsalesview, name='Product SubCategory Sales Analysis'),
    path('items/<int:pk>/sales/', objectsalesview, name='Product Sales Analysis'),
    path('suppliers/<int:pk>/forecast/', objectforecastview, name='Supplier Forecast'),
    path('customers/<int:pk>/forecast/', objectforecastview, name='Customer Forecast'),
    path('itemsubcategories/<int:pk>/forecast/', objectforecastview, name='Product SubCategory Forecast'),
    path('items/<int:pk>/forecast/', objectforecastview, name='Product Forecast'),
    path('customers/<int:pk>/', CustomerDetailView.as_view()),
    path('settings/', SettingsView, name='Settings'),
    path('settings/importproducts/',ImportProducts, name='Import'),
    path('settings/updateattributes/',UpdateAttributes, name='Update'),
    path('settings/updateforecast/',UpdateForecast, name='updateforecast'),
    path('settings/optimize/',Optimize, name='Optimize'),
]

re_path(r'^celery-progress/', include('celery_progress.urls')),  # the endpoint is configurable
