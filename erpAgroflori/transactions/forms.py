from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from .models import Transaction, TicketSale, TicketSaleDetail, SouvenirSale, SouvenirSaleDetail, FoodSale, FoodSaleDetail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div,  Submit, Reset
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, formset_factory
from .models import SystemType, SystemTypeCategory

class TransactionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user_user:
            self.fields['user'].required = False 
            self.fields['user'].initial = self.user_user

        self.helper = FormHelper()
        self.helper.form_id = 'id-transaction_form'
        self.helper.form_class = 'transaction_form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Field('user', type='hidden'),
                Field('date', css_class='col-md-6'),
                Field('currency', css_class='col-md-6'),
                Field('method_of_payment', css_class='col-md-6'),
                Field('category', css_class='col-md-6'),
                Field('description', css_class='col-md-6'),
                Field('amount', css_class='col-md-6'),
                style="display: grid; grid-template-columns: repeat(2, 1fr);gap: 16px;"
            ),
        )
        self.helper.add_input(Submit('submit', 'Guardar'))
        self.helper.add_input(Reset('Reset This Form', 'Borrar'))

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['user'] = self.user_user

        if cleaned_data['category'] == 'EX':
            cleaned_data['category'] = - cleaned_data['category']
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
  
        if self.user_user is not None:
            instance.user = self.user_user
            instance.save()
            return instance
        else:
            raise ValidationError("Transaction form not linked to a user")
    

    class Meta:
        model = Transaction
        fields = ["date", "method_of_payment", "currency", "amount", "description", "category", "user"]

class TicketSaleForm(ModelForm):
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'amount-input-id', 'readonly': 'readonly'}))
    user = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.user_user = kwargs.pop('user', None)
        super(TicketSaleForm, self).__init__(*args, **kwargs)    
        self.fields['amount'].initial = 0  

        if self.user_user:
            self.fields['user'].initial = self.user_user

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['user'] = self.user_user
        return cleaned_data
    
    class Meta:
        model = TicketSale
        fields = ["date", "method_of_payment", "amount", 'user']
    
class CustomChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', None)
        super(CustomChoiceField, self).__init__(queryset, *args, **kwargs)
        
        if queryset is not None:
            self.choices = [(obj.id, f"{obj}:{obj.unitary_price}") for obj in queryset]
 
class TicketSaleDetailForm(ModelForm):
    
    quantity = forms.IntegerField(widget=forms.NumberInput())

    def __init__(self, *args, **kwargs):
        super(TicketSaleDetailForm, self).__init__(*args, **kwargs)

        category_type = 'Ticket'
        ticket_types = SystemTypeCategory.objects.filter(name=category_type)
        
        if ticket_types:
            id_ticket= ticket_types.first().id
            cat_queryset =  SystemType.objects.filter(category=id_ticket)
            self.fields['ticket_type'] = CustomChoiceField(queryset=cat_queryset)
            self.fields['ticket_type'].queryset = cat_queryset
            self.fields['ticket_type'].widget.attrs['id'] = f"{self.prefix}-ticket-type"
            self.fields['ticket_type'].widget.attrs['class'] = f"ticket-type-class"
            self.fields['quantity'].initial = 0
            self.fields['quantity'].widget.attrs['id'] = f"{self.prefix}-quantity"
            self.fields['quantity'].widget.attrs['class'] = f"quantity-class"
            self.fields['promotion_discount'].initial = 0
    
        
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    class Meta:
        model = TicketSaleDetail
        fields = ['ticket_type', 'promotion_discount', 'promotion_description' ,'ticket_sale', 'quantity'] 
    
class SouvenirSaleForm(ModelForm):
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'amount-input-id', 'readonly': 'readonly'}))
    user = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.user_user = kwargs.pop('user', None)
        super(SouvenirSaleForm, self).__init__(*args, **kwargs)    
        self.fields['amount'].initial = 0  

        if self.user_user:
            self.fields['user'].initial = self.user_user

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['user'] = self.user_user
        return cleaned_data
    
    class Meta:
        model = SouvenirSale
        fields = ["date", "method_of_payment", "amount", 'user']

class SouvenirSaleDetailForm(ModelForm):
    
    quantity = forms.IntegerField(widget=forms.NumberInput())

    def __init__(self, *args, **kwargs):
        super(SouvenirSaleDetailForm, self).__init__(*args, **kwargs)

        category_type = 'souvenir'
        souvenirs_types = SystemTypeCategory.objects.filter(name=category_type)
        
        if souvenirs_types:
            id_souvenir = souvenirs_types.first().id
            cat_queryset =  SystemType.objects.filter(category=id_souvenir)
            self.fields['souvenir_type'] = CustomChoiceField(queryset=cat_queryset)
            self.fields['souvenir_type'].queryset = cat_queryset
            self.fields['souvenir_type'].widget.attrs['id'] = f"{self.prefix}-souvenir-type"
            self.fields['souvenir_type'].widget.attrs['class'] = f"souvenir-type-class"
            self.fields['quantity'].initial = 0
            self.fields['quantity'].widget.attrs['id'] = f"{self.prefix}-quantity"
            self.fields['quantity'].widget.attrs['class'] = f"quantity-class"
    
        
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    class Meta:
        model = SouvenirSaleDetail
        fields = ['souvenir_type','souvenir_sale', 'quantity'] 
    
class FoodSaleForm(ModelForm):
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'amount-input-id', 'readonly': 'readonly'}))
    user = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.user_user = kwargs.pop('user', None)
        super(FoodSaleForm, self).__init__(*args, **kwargs)
        self.fields['amount'].initial = 0 

        if self.user_user:
            self.fields['user'].initial = self.user_user

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['user'] = self.user_user
        return cleaned_data
    
    class Meta:
        model = FoodSale
        fields = ["date", "method_of_payment", "amount", 'user']

class FoodSaleDetailForm(ModelForm):
    quantity = forms.IntegerField(widget=forms.NumberInput())

    def __init__(self, *args, **kwargs):
        super(FoodSaleDetailForm, self).__init__(*args, **kwargs)

        category_type = 'Comida'
        food_types = SystemTypeCategory.objects.filter(name=category_type)

        if food_types:
            id_food = food_types.first().id
            cat_queryset =  SystemType.objects.filter(category=id_food)
            print(cat_queryset)
            self.fields['food_type'] = CustomChoiceField(queryset=cat_queryset)
            self.fields['food_type'].queryset = cat_queryset
            #self.fields['ticket_type'].initial = cat_queryset.first()
            self.fields['food_type'].widget.attrs['id'] = f"{self.prefix}-food-type"
            self.fields['food_type'].widget.attrs['class'] = f"food-type-class"
            self.fields['quantity'].initial = 0
            self.fields['quantity'].widget.attrs['id'] = f"{self.prefix}-quantity"
            self.fields['quantity'].widget.attrs['class'] = f"quantity-class"
 
 

SouvenirSaleFormSet = inlineformset_factory(SouvenirSale, SouvenirSaleDetail,form=SouvenirSaleDetailForm, exclude=[], min_num=1, max_num=4, extra=6)
FoodSaleFormSet = inlineformset_factory(FoodSale, FoodSaleDetail,form=FoodSaleDetailForm, exclude=[], min_num=1, max_num=4, extra=4)

TicketSaleFormSet = inlineformset_factory(
    TicketSale, TicketSaleDetail, form=TicketSaleDetailForm,
    exclude=[], min_num=1, max_num=4, extra=1
)

TransactionFormSet = formset_factory(TransactionForm)

