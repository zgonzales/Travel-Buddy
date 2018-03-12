# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from .models import User, Destination, Trip

import bcrypt

from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'travel_buddy2/index.html')

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')

def register(request):
    errors = User.objects.reg_validator(request.POST)
    if type(errors) == list:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    
    request.session['first_name'] = errors.first_name
    request.session['id'] = errors.id
    return redirect('/travels')

def login(request):
    errors = User.objects.validate_login(request.POST)
    if type(errors) == list:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['first_name'] = errors.first_name
        request.session['id'] = errors.id
        return redirect('/travels')

def success(request):
    try:
        request.session['id']
    except KeyError:
        return redirect('/')
    
    this_user= User.objects.get(id=request.session['id'])
    content = {
        'all_trips': Trip.objects.all(),
        'your_trips': Trip.objects.filter(user=this_user),
        'trips_joined': Trip.objects.filter(users=this_user),
        'other_trips': Trip.objects.exclude(user=this_user).exclude(users=this_user),
        'logged_in': User.objects.get(id=request.session['id']),
        'users': User.objects.all()
    }
    return render(request, 'travel_buddy2/travels.html', content)

def add(request):
    content = {
        'logged_in': User.objects.get(id=request.session['id']),
        'destinations': Destination.objects.all()
    }
    return render(request, 'travel_buddy2/add.html', content)

def create(request):
    result = Trip.objects.trip_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/travels/new')
    else:
        return redirect("/travels")

def dest_info(request, dest_id):
    this_dest = Destination.objects.get(id=dest_id)
    content = {
        'trip': Trip.objects.get(destination=this_dest),
        'joined': Trip.objects.get(destination=this_dest).users.all()
    }
    return render(request, 'travel_buddy2/dest_info.html', content)

def join(request, trip_id):
    this_user = User.objects.get(id=request.session['id'])
    this_trip = Trip.objects.get(id=trip_id)
    this_trip.users.add(this_user)
    
    return redirect('/travels')