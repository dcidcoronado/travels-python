from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    # if 'user' in request.session:
    #     del request.session['user']
    return render(request, 'index.html')


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        request.session['reg_name'] = request.POST['name']
        request.session['reg_username'] = request.POST['username']

        return redirect('/') 

    else:
        if 'reg_name' in request.session:
            del request.session['reg_name']
        if 'reg_username' in request.session:
            del request.session['reg_username']
        
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            name = request.POST['name'],
            username = request.POST['username'],
            password = pw_hash
        )

        messages.success(request, 'User succesfully created') 

        return redirect('/')


def login(request):
    errors = User.objects.login_validator(request.POST)
    # print(request.POST['email'])
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        if 'user' in request.session:
            messages.info(request, "You're already logged")
            return redirect('/')
        user = User.objects.filter(username=request.POST['username'])
        logged_user = user[0]
        userlogged = {
            'id': logged_user.id,
            'name': logged_user.name,
            'username': logged_user.username
            }
        request.session['user'] = userlogged
        messages.success(request, 'User succesfully logged')
        return redirect('/travels')


def success(request):
    if 'user' not in request.session:
        return redirect('/')
    return redirect('/travels')


def logout(request):
    request.session.flush()
    messages.info(request, 'User succesfully logout')
    return redirect('/')

