from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Travel
import bcrypt
from login_registration_app.models import User

def travels(request):
    user_travels = Travel.objects.filter(user=request.session['user']['id'])
    other_travels = Travel.objects.exclude(user__id=request.session['user']['id'])
    other_users = User.objects.exclude(id=request.session['user']['id'])
    context = {
        'other_travels': other_travels,
        'user_travels': user_travels,
        'other_users': other_users
    }
    return render(request, 'travels.html', context)

def join_travel(request, travel_id):
    this_user = User.objects.get(id = request.session['user']['id'])
    this_travel = Travel.objects.get(id = f'{travel_id}')
    this_user.travels.add(this_travel)
    return redirect ('/travels')


def add(request):
    if request.method == 'GET':
        return render(request, 'add.html')
    elif request.method == 'POST':
        errors = Travel.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)

            request.session['reg_destination'] = request.POST['destination']
            request.session['reg_description'] = request.POST['description']
            request.session['reg_date_from'] = request.POST['date_from']
            request.session['reg_date_to'] = request.POST['date_to']

            return redirect('/travels/add') 

        else:
            if 'reg_destination' in request.session:
                del request.session['reg_destination']
            elif 'reg_description' in request.session:
                del request.session['reg_description']
            elif 'reg_date_from' in request.session:
                del request.session['reg_date_from'] 
            elif 'reg_date_to' in request.session:
                del request.session['reg_date_to']

            this_user = User.objects.get(id = request.session['user']['id'])
            this_travel = Travel.objects.create(
                    destination = request.POST['destination'],
                    description = request.POST['description'],
                    date_from = request.POST['date_from'],
                    date_to = request.POST['date_to'],
                    planner = this_user
                )
            this_user.travels.add(this_travel)

            messages.success(request, 'Travel succesfully created')

            return redirect('/travels')



def destination(request, travel_id):
    this_travel = Travel.objects.get(id = f'{travel_id}')
    travel_users = User.objects.filter(travels__id = f'{travel_id}')
    guests = User.objects.filter(travels__id = f'{travel_id}').exclude(id=this_travel.planner.id)
    context = {
        'this_travel': this_travel,
        'travel_users': travel_users,
        'guests': guests
    }
    return render(request, 'destination.html', context)


