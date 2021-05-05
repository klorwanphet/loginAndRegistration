from django.http.request import validate_host
from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt


def index(request):
    return render(request, 'index.html')


def register(request):
    hash1=bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
    errors=User.objects.basic_validator(request.POST)
    if errors:
        for k,v in errors.items():
            messages.error(request,v)
        return redirect("/")
    
    else:
        messages.info(request, "You have successfully registered an account. Please log in to continue.")
        new_user=User.objects.create(
            first_name=request.POST['fname'],
            last_name=request.POST['lname'],
            email=request.POST['email'],
            password= hash1
        )
        request.session['userid']= new_user.id
        return redirect("/")

def login(request):
    errors=User.objects.login_validator(request.POST)
    if len(errors)>0:
        for k,v in errors.items():
            messages.error(request,v)
        return redirect("/")
    else:
        user=User.objects.filter(email=request.POST['email1'])
        request.session['userid']=user[0].id
        if len(user) !=1:
            messages.error(request,"User does not exist.")
            return redirect("/")

        return redirect('/dashboard')
    

def dashboard(request):
    context ={
        "logged_in":User.objects.get(id=request.session['userid'])
    }
    if not"userid" in request.session:
        messages.error(request, "Log in to view this page.")
        return redirect('/')

    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')
    