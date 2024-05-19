from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy

from .models import *
from .forms import *

# from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.db.models import Count
import csv

# Create your views here.


def index(request):

    total_products = Product.objects.all().count()
    total_vendors = Vendor.objects.all().count()
    total_purchases = Purchase.objects.all().count()
    total_sales = Sale.objects.all().count()

    # low_stock = Stock.objects.filter(total_balance_quantity__lte=5).order_by('-id')[:2]
    low_stock = Stock.objects.filter(total_balance_quantity__lte=3).annotate(dcount=Count('product_id')).order_by('-id')[:3]
   
    context = {
            'products'  : total_products,
            'vendors'   : total_vendors,
            'sales'     : total_sales,
            'purchases' : total_purchases,
            'name'      : request.user.username,
            'low_stock' : low_stock
        }
    return render(request, "index.html", context)


# SIGNUP 

def signup(request):
    if request.method=="POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        myuser = User.objects.create_user(username,email,password)
        myuser.save()
        return redirect('login')
    return render(request,'authentication/signup.html')


# LOGIN


def user_login(request):
    if request.method == "POST":
        username1 = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username1, password=password)
        if user is not None:
            login(request,user)
            return redirect("index")
        else:
            return redirect("signup")
    return render(request, 'authentication/login.html')


# LOGOUT

def user_logout(request):
    logout(request)
    return redirect("login")



#  ------------ VENDOR ------------

# Used to add a new vendor
class VendorCreateView(CreateView):
    model = Vendor
    form_class = VendorForm
    success_url = reverse_lazy('vendors')
    # success_message = "Vendor has been created successfully"
    template_name = "vendors/update_vendor.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Vendor'
        context["savebtn"] = 'Add Vendor'
        return context 
    

# Shows list of all vendors
class VendorListView(ListView):
    model = Vendor
    template_name = "vendors/vendors.html"
    queryset = Vendor.objects.filter(is_deleted=False)
    

# Used to update a vendor's info
class VendorUpdateView(SuccessMessageMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    success_url = reverse_lazy('vendors')
    success_message = "Vendor details has been updated successfully"
    template_name = "vendors/update_vendor.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit'
        context["savebtn"] = 'Save'
        return context


# Used to delete a vendor
class VendorDeleteView(View):
    model = Vendor
    
    def get(self, request, pk):
        vendor = get_object_or_404(Vendor, pk=pk)
        return render(request, self.template_name, {'object' : vendor})

    def post(self, request, pk):  
        vendor = get_object_or_404(Vendor, pk=pk)
        vendor.is_deleted = True
        vendor.save()                                               
        return redirect('vendors')
    

# -------------- UNIT ----------------

# Used to add a new unit
class UnitCreateView(CreateView):
    model = Unit
    form_class = UnitForm
    success_url = reverse_lazy('units')
    template_name = "units/update_unit.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Unit'
        context["savebtn"] = 'Add Unit'
        return context 
    

# Shows list of all units
class UnitListView(ListView):
    model = Unit
    template_name = "units/units.html"
    # context_object_name = 'obj'
    queryset = Unit.objects.filter(is_deleted=False)
    

# Used to update a unit's info
class UnitUpdateView(UpdateView):
    model = Unit
    form_class = UnitForm
    success_url = reverse_lazy('units')
    template_name = "units/update_unit.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit'
        context["savebtn"] = 'Save'
        return context


# Used to delete a unit
class UnitDeleteView(View):
    model = Unit
    
    def get(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        return render(request, self.template_name, {'object' : unit})

    def post(self, request, pk):  
        unit = get_object_or_404(Unit, pk=pk)
        unit.is_deleted = True
        unit.save()                                               
        return redirect('units')
    


# -------------- PRODUCT ----------------

# Used to add a new product
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products')
    template_name = "products/update_product.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New product'
        context["savebtn"] = 'Add product'
        return context 
    

# Shows list of all products
class ProductListView(ListView):
    model = Product
    template_name = "products/products.html"
    queryset = Product.objects.filter(is_deleted=False)
    

# Used to update a product's info
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products')
    template_name = "products/update_product.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit'
        context["savebtn"] = 'Save'
        return context


# Used to delete a product
class ProductDeleteView(View):
    model = Product
    
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, self.template_name, {'object' : product})

    def post(self, request, pk):  
        product = get_object_or_404(Product, pk=pk)
        product.is_deleted = True
        product.save()                                               


# -------------- Purchases ----------------
        
# Shows list of all purchases 
class PurchaseView(ListView):
    model = Purchase
    template_name = "purchases/purchases_list.html"
    context_object_name = 'purchases'
    queryset = Purchase.objects.order_by('-purchase_date')

# New purchase order
class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    success_url = reverse_lazy('new-purchase')
    template_name = "purchases/new_purchase.html"

    def form_valid(self, form):
        messages.success(self.request, f" New Order Created Successfully!!")
        return super().form_valid(form)

# Purchase bill
class PurchaseBillView(ListView):
    model = Purchase
    template_name = "purchases/purchase_bill.html"
    # context_object_name = 'bill'

    def get(self, request, billno):
        context = {
            'bill' : Purchase.objects.get(billno=billno),
            'items': Purchase.objects.filter(billno=billno),
        }
        return render(request, self.template_name, context)



# -------------- Sales ----------------
        
# Shows list of all sales 
class SaleView(ListView):
    model = Sale
    template_name = "sales/sales_list.html"
    context_object_name = 'sales'
    queryset = Sale.objects.order_by('-sale_date')

# New sale order
class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    success_url = reverse_lazy('new-sale')
    template_name = "sales/new_sale.html"

    def form_valid(self, form):
        messages.success(self.request, f" New Order Created Successfully!!")
        return super().form_valid(form)

# Sale bill
class SaleBillView(ListView):
    model = Sale
    template_name = "sales/sale_bill.html"
    
    def get(self, request, billno):
        context = {
            'bill' : Sale.objects.get(billno=billno),
            'items': Sale.objects.filter(billno=billno),
        }
        return render(request, self.template_name, context)


# -------------- Inventory ----------------
        
# Shows list of all inventory 
class StockListView(ListView):
    model = Stock
    template_name = "inventory.html"
    context_object_name = 'stock'
    queryset = Stock.objects.order_by('-id')

# Generate Text File Inventory List 
def stock_csv(request):
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename=stock.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate the Model
    inventory = Stock.objects.all()

    # Add column headings to the csv file
    writer.writerow(['PRODUCT', 'STOCK','PURCHASE', 'SALE'])

    # Loop Thu and output 
    for i in inventory:
        writer.writerow([i.product, i.total_balance_quantity , i.purchase_quantity, i.sale_quantity])

    return response
