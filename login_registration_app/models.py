from django.db import models
import re
from datetime import datetime
import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        NAME_REGEX = re.compile(r'^[A-ZÀ-ÿ\u00d1][a-zÀ-ÿ\u00f1\u00d1]+$')

        if len(postData['name']) == 0:
            errors['name'] = "Must enter a name"
        else:
            if not NAME_REGEX.match(postData['name']):
                errors['name'] = "Name must start with a capital letter and must be one word only"
            elif len(postData['name']) < 3:
                errors['name'] = "The first name must be at least 3 characters long"

        if len(postData['username']) == 0:
            errors['username'] = "Must enter an username"
        else:
            if len(postData['username']) < 3:
                errors['username'] = "The username must be at least 3 characters long"
            elif User.objects.filter(username=postData['username']):
                errors['username'] = "Must be a new User"

        if len(postData['password']) == 0:
            errors['password'] = "Must enter a password"
        else:
            if postData['password'] != postData['cpassword']:
                errors['password'] = "Passwords doesn't match"
            elif len(postData['password']) < 8:
                errors['password'] = "Password must be at least 8 characters long"
            elif User.objects.filter(username=postData['username']):
                errors['username'] = "This username is already registered"

        return errors


    def login_validator(self, postData):
        user = User.objects.filter(username=postData['username'])
        errors = {}
        # print(user)
        if len(user) > 0:
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()) is False:
                errors['user'] = "Invalid user"
        else:
            errors['user'] = "Invalid user"
        return errors    




class User(models.Model):
    name = models.CharField(max_length=40)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    # def __repr__(self):
    #     return f'{first_name} {last_name} {email}'

