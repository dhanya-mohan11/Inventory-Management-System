from django.urls import path
from .views import *

urlpatterns = [

    path('',user_login,name="login"),
    path('signup/', signup, name="signup"),
    path('logout/',user_logout,name="logout"),

    path('index/', index, name="index"),

    path('vendors/',VendorListView.as_view(),name="vendors"),
    path('vendors/new', VendorCreateView.as_view(), name="new-vendor"),
    path('vendors/<pk>/edit', VendorUpdateView.as_view(), name="update-vendor"),
    path('vendors/<pk>/delete', VendorDeleteView.as_view(), name="delete-vendor"),
    
    path('units/',UnitListView.as_view(),name="units"),
    path('units/new', UnitCreateView.as_view(), name="new-unit"),
    path('units/<pk>/edit', UnitUpdateView.as_view(), name="update-unit"),
    path('units/<pk>/delete', UnitDeleteView.as_view(), name="delete-unit"),
    
    path('products/', ProductListView.as_view(), name="products"),
    path('products/new', ProductCreateView.as_view(), name="new-product"),
    path('products/<pk>/edit', ProductUpdateView.as_view(), name="update-product"),
    path('products/<pk>/delete', ProductDeleteView.as_view(), name="delete-product"),

    path('purchases/', PurchaseView.as_view(), name='purchases'), 
    path('purchases/new', PurchaseCreateView.as_view(), name='new-purchase'),    
    path("purchases/<billno>", PurchaseBillView.as_view(), name="purchase-bill"),
    
    path('sales/', SaleView.as_view(), name='sales'), 
    path('sales/new', SaleCreateView.as_view(), name='new-sale'),    
    path("sales/<billno>", SaleBillView.as_view(), name="sale-bill"),
    
    path('inventory/', StockListView.as_view(), name='inventory'),
    path('stock_csv/', stock_csv, name="stock_csv"),
   
]