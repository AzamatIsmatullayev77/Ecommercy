from django import forms

from ecommerce.models import Customer, Product


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
