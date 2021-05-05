3
from django.contrib import messages
from django.db import models
import re
import bcrypt

class userManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):              
            errors['email'] = "Invalid email address!"
        if len(postData['fname']) <2:
            errors['fname'] = "First name field must have 2 or more characters"
        if len(postData['lname']) <2:
            errors['lname'] = "last name field must have 2 or more characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters in length"
        if postData['password'] != postData['cpassword']:
            errors["password_match"] = "Passwords do not match!"
        try:
            User.objects.get(email_address = postData['email'])
            errors['email_unique'] = "a user already exists with that email address."
        except:
            pass
    
        return errors

    def login_validator(self, postData):
        errors={}
        
        user = User.objects.filter(email=postData['email1']) 
        if len(user)<1:
            errors['email1']="Invalid email or password"
        else:
            logged_user = user[0] 
            if not bcrypt.checkpw(postData['password1'].encode(), logged_user.password.encode()):
                errors['password1']= "Invalid email or password"
        
        return errors
class User(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = userManager()
