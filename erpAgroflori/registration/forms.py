from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from users.models import Person, User
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Nombre de usuario', min_length=5, max_length=150)
    email = forms.EmailField(label='Correo', widget=forms.EmailInput())
    first_name = forms.CharField(label='Nombre', widget=forms.TextInput())
    last_name = forms.CharField(label='Apellidos', widget=forms.TextInput())
    
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username = username)
        if new.count():
            raise ValidationError("Ya existe una cuenta con este nombre de usuario.")
        return username
    
    def clean_email(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError("Ya existe una cuenta con este correo.")  
        return email  
    


class RegistrationForm(ModelForm):
    
    def __init__(self, *args,**kwargs):
        user_value = kwargs.pop('user_value', None)
        super(RegistrationForm, self).__init__(*args,**kwargs)
        if user_value:
            self.fields['user'].initial = user_value.id

    user = forms.CharField(widget=forms.HiddenInput())
    blood_type = forms.CharField(label="Tipo de sangre", max_length=20)
    birth_date = forms.DateField(label="Fecha de nacimiento", widget=forms.DateInput())
    date_joined_agr = forms.DateField(label = "Fecha de ingreso a Agroflori", widget=forms.DateInput(format="%d %b, %Y"))
    phone = PhoneNumberField()
    emergency_name = forms.CharField(label="Nombre de un contacto de emergencia")
    emergency_phone = PhoneNumberField()

    def __save__(self, commit=True):
        super().save(commit=False)
        print (f"user_value {self.user_value}")
        if not self.user_value:
            person = Person.objects.create(user= self.user_value, blood_type =self.blood_type,
                                       birth_date = self.birth_date, date_joined_agr = self.joined_date,
                                       phone=self.phone, emergency_phone=self.emergency_phone,
                                       emergency_name=self.emergency_contact)   
            return person
        else:
            raise ValidationError("Registration form not linked to a user")
    
    class Meta:
        model = Person
        fields = ("user", "phone", "birth_date", "date_joined_agr", "blood_type",
                    "emergency_name", "emergency_phone")

    
 #class CustomFieldName(models.Field):

class LogInForm(AuthenticationForm):
    pass