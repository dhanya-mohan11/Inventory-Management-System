from django import forms
from django.forms import formset_factory
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# form used for User
class UserRegistry(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

# form used for Vendor
class VendorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = Vendor
        fields = ['name', 'phone', 'address', 'email']
        widgets = {
            'address' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4'
                }
            )
        }

# form used for Unit
class UnitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['short_name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
    class Meta:
        model = Unit
        fields = '__all__'
        

# form used for Products
class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].queryset = Unit.objects.filter(is_deleted=False)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
    class Meta:
        model = Product
        fields = ['name', 'unit', 'description']

        error_messages = {
			'unit': {'required': 'Please add at least one unit'}
		}

        widgets = {
            'description' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4'
                }
            ),
            'unit': forms.Select(
                attrs = {
                    'class' : 'select form-control',
                    'style': 'width:1290px'
                } 
            )
        }



# New purchase order form
class PurchaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_deleted=False)
        self.fields['vendor'].queryset = Vendor.objects.filter(is_deleted=False)
        
        self.fields['product'].widget.attrs.update({'class': 'select form-control','style': 'width:1290px', 'required': 'true'})
        self.fields['vendor'].widget.attrs.update({'class': 'select form-control','style': 'width:1290px', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['price'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})
    
    class Meta:
        model = Purchase
        fields = ['product', 'vendor', 'quantity', 'price']

        # widgets = {
                
        #     'vendor': forms.Select(
        #         attrs = {
        #             'class' : 'select form-control',
        #             'style': 'width:1290px'
        #         } 
        #     )
        # }


# New sale order form
class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_deleted=False)

        # self.fields['product'].queryset = Purchase.objects.all().annotate(product_id=Product.name)
        # self.fields['product'].queryset = Product.objects.filter(is_deleted=False).annotate(purchase__product=F('purchase__product'))

        self.fields['product'].widget.attrs.update({'class': 'select form-control','style': 'width:1290px', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['price'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})
        self.fields['customer_name'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['customer_phone'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
       
    class Meta:
        model = Sale
        fields = ['product', 'quantity', 'price', 'customer_name', 'customer_phone', 'customer_address']

        widgets = {
            'customer_address' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4'
                }
            )
        }

