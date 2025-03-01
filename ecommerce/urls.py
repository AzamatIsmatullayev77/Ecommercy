from .views import ProductListView,Grid,ProductDetailView,CustomerListView,CustomerDetailView,CustomerCreateView,ProductCreateView
from django.contrib import admin
from django.urls import path
from ecommerce import views
from config import settings
from django.conf.urls.static import static
app_name = 'ecommerce'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('grid/', Grid.as_view(), name='grid'),
    path('detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('customers/',CustomerListView.as_view(), name='customers'),
    path('customers-detail/<slug:slug>/',CustomerDetailView.as_view(), name='customers_detail'),
    path('create-customer/',CustomerCreateView.as_view(), name='create_customer'),
    path('create_product',ProductCreateView.as_view(),name='create_product'),
    # path('',views.index,name='index'),
]

# if settings.DEBUG:
#     urlpatterns
