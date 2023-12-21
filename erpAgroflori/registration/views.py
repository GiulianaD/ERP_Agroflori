from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, CustomUserCreationForm
from users.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def redirect_log_in(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        return redirect("log-in")

def logout_view(request):
    logout(request)
    return redirect("log-in")

# Create your views here.
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)      
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Usuario registrado.')
            return redirect('complete-registration', username = form.cleaned_data['username'].lower())
        return render(request, "registration.html", {"form": form})
    else:
            form = CustomUserCreationForm()
            return render(request, "registration.html", {"form": form})

def complete_registration(request, username=None):
    
    user = User.objects.get(username=username)
    if user:
        if request.method == "POST":
            form = RegistrationForm(request.POST, **{"user_value":user}, )
            if form.is_valid():
                form.save(commit=True)
                messages.success(request, 'Gracias {} por terminar de registrarte. .'.format(username))
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            print(form.errors)    
            return render(request, "complete_registration.html", {'form':form})
        else:
            form = RegistrationForm(**{'user_value':user})        
            return render(request, "complete_registration.html", {'form': form})
    else:
         return HttpResponse("You are not allowed to enter this page.")
    
def authenticate_user(request):
    if request.method == "POST":
        form = AuthenticationForm(None, request.POST)
        if form.is_valid():
            user = authenticate(**form.clean())
            if user:
                login(request, user)
                return redirect('home')
            else:
                return render(request, "login.html", {"form": form})           
        return render(request, "login.html", {"form": form})
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})