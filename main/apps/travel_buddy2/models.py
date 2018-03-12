# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import bcrypt

import re

from django.contrib import messages

from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, post_data):
        errors = []
        if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2:
            errors.append("name fields must be at least 3 characters")
        if len(post_data['pass']) < 8:
            errors.append("password must be at least 8 characters")       
        if not re.match(NAME_REGEX, post_data['first_name']):
            errors.append('name fields must be letter characters only')
        if not re.match(NAME_REGEX, post_data['last_name']):
            errors.append('name fields must be letter characters only')
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("email already in use")
        if post_data['pass'] != post_data['pass_conf']:
            errors.append("passwords do not match")

        if not errors:
            hashed = bcrypt.hashpw((post_data['pass'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                first_name=post_data['first_name'],
                last_name=post_data['last_name'],
                email=post_data['email'],
                password=hashed
            )
            return new_user
        return errors

    def validate_login(self, post_data):
        errors = []
        if len(self.filter(email=post_data['email2'])) > 0:
            this_user = self.filter(email=post_data['email2'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), this_user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return this_user

class TripManager(models.Manager):
    def trip_validator(self, post_data):
        errors = []
        if len(post_data['destination']) < 1 or len(post_data['description']) < 1:
            errors.append('fields are required')
        if post_data['from'] < unicode(datetime.now()):
            errors.append('travel dates must be in the future')
        if post_data['from'] > post_data['to']:
            errors.append('return date must not precede departure date')

        if not errors:
            if  Destination.objects.get(name=post_data['destination']):
                this_dest = Destination.objects.get(name=post_data['destination'])
            else: 
                this_dest = Destination.objects.create(name=post_data['destination'])

            print post_data['id']
            print type(int(post_data['id']))
            this_trip = self.create(
                user = User.objects.get(id=post_data['id']),
                destination = this_dest,
                desc = post_data['description'],
                leave_date = post_data['from'],
                return_date =  post_data['to']
            )
            
            return this_trip
        else:
            return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Destination(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Trip(models.Model):
    desc = models.TextField()
    leave_date = models.DateField()
    return_date = models.DateField()
    destination = models.ForeignKey(Destination, related_name="trips_to")
    user = models.ForeignKey(User, related_name="trips_created")
    users = models.ManyToManyField(User, related_name="trips_joined")
    objects = TripManager()
    

