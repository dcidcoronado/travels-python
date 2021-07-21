from django.db import models
import re
import datetime
from datetime import datetime
import bcrypt
from login_registration_app.models import User

# Create your models here.
class TravelManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['destination']) == 0:
            errors['destination'] = 'Please, enter a destination'


        if len(postData['description']) == 0:
            errors['description'] = 'Please, enter a description'


        if len(postData['date_from']) == 0:
            errors['date_from'] = 'Please, enter a travel date from'
        else: 
            today = datetime.now()
            start = datetime.strptime(postData['date_from'], '%Y-%m-%d')
        
            sum_today = today.year + today.month + today.day
            sum_start = start.year + start.month + start.day

            if sum_today > sum_start :
                errors['date_from'] = 'Travel date from must be in the future'


        if len(postData['date_to']) == 0:
            errors['date_to'] = 'Please, enter a travel date to'
        else:
            start = datetime.strptime(postData['date_from'], '%Y-%m-%d')
            end = datetime.strptime(postData['date_to'], '%Y-%m-%d')
            sum_start = start.year + start.month + start.day
            sum_end = end.year + end.month + end.day


            if sum_start > sum_end :
                errors['date_to'] = 'Travel date to must be later than the travel date from'

        return errors


class Travel(models.Model):
    user = models.ManyToManyField(User, related_name="travels")
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TravelManager()