from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *

# Create your views here.


def home(request):
    return render(request, "home.html")


def auth(request, page):
    
    if page == "login":
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                
                
                user = authenticate(request, username=form.cleaned_data['email'], password = form.cleaned_data['password'] )
                
                if user:
                    login(request, user)
                    return redirect("stress-report")
                else:
                    messages.error(request, 'Invalid Credentials')
        else: 
              form = LoginForm()  
        
    elif page == "logout":
        logout(request)
        return redirect("/auth/login/")
        
    else:
        if request.method == "POST":
            
            form = RegisterForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                     messages.error(request, "Password did'nt match")
                     print( form.cleaned_data['password'] is not form.cleaned_data['confirm_password'])
                else:
                    
                    user = form.save()
                    print(user)
                    StressRecord.objects.create(user=user)
                    all_modules = Module.objects.all()
                    user.module.add(*all_modules)
                    login(request, user)
                    return redirect("home")
        else:
            form = RegisterForm()
        
    return render(request, "auth.html", {"form": form, 'page': page})

@login_required(login_url="auth/login/")
def stress_report(request):
    if request.user.is_superuser:
        return redirect("home")
    record = StressRecord.objects.get(user =request.user)
    
    return render(request, "stress_report.html", {"record": record})

@login_required(login_url="auth/login/")
def programs(request):
    modules = Module.objects.all()
    return render(request, "programs.html", {"modules": modules})
