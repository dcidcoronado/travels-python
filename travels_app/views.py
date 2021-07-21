from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Travel
import bcrypt
from login_registration_app.models import User

def travels(request, travel_id):
    if request.method == 'GET':
        all_travels = Travel.objects.all()
        user_travels = Travel.objects.filter(user=request.session['user']['id'])
        context = {
            'all_travels': all_travels,
            'user_travels': user_travels
        }
        return render(request, 'travels.html', context)


    elif request.method == 'POST':
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
            Travel.objects.create(
                user = this_user,
                destination = request.POST['destination'],
                description = request.POST['description'],
                date_from = request.POST['date_from'],
                date_to = request.POST['date_to']
            )

            messages.success(request, 'Travel succesfully created')

            return redirect('/travels')



def destination(request, travel_id):
    this_travel = Travel.objects.get(id = f'{travel_id}')
    travel_users = User.objects.filter(travels__id = f'{travel_id}')
    planner = travel_users.first()
    guests = User.objects.exclude(planner)
    context = {
        'this_travel': this_travel,
        'travel_users': travel_users,
        'planner': planer,
        'guests': guests
    }
    return render(request, destination.html, context)


