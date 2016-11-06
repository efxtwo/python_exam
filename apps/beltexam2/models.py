from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class UserManager(models.Manager):
    def login(self, email, password):
        errors = []
        if len(User.objects.filter(email = email)) <1:
            errors.append('Invalid User')
        else:
            user = User.objects.get(email = email)
            if bcrypt.hashpw(password.encode(), user.password.encode()) != user.password:
                errors.append('Invalid password')
        return errors

    def register(self, post):
        encrypted_password=bcrypt.hashpw(post['pw'].encode(), bcrypt.gensalt())
        User.objects.create(name=post['name'],username=post['username'],email=post['email'],birthday=post['birthdate'], password=encrypted_password)

    def validate_user_info(self, post):
        errors = []

        if len(post['name']) == 0:
            errors.append("Do you have a name or can I call you mine?")
        elif len(post['name']) < 2:
            errors.append("Name must be at least 2 characters")

        if len(post['username']) == 0:
            errors.append("Let me guess, your alias is GORGEOUS?")
        elif len(post['username']) < 2:
            errors.append("username must be at least 2 characters")

        if len(post['email']) == 0:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(post['email']):
            errors.append("Valid email is required")

        if len(post['pw']) == 0:
            errors.append("Password is required")
        elif len(post['pw']) < 8:
            errors.append("Password must be at least 8 characters")
        elif post['pw'] != post['confirmpass']:
            errors.append("Password fields must match")

        if len(post['email']) <= 0:
            errors.append("Email address not available")
        return errors

    def validate_user_post(self, post):
        if len(post['quotedby']) == 0:
            errors.append("Please enter a name")
        elif len(post['quotedby']) < 3:
            errors.append("must be longer than that")

        if len(post['message']) == 0:
            errors.append("leave a quote")
        elif len(post['message']) < 3:
            errors.append("you must be inspirational")


class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quotes(models.Model):
    creator = models.ForeignKey(User)
    favoriter = models.ManyToManyField(User, related_name='inspiration')
    author = models.CharField(max_length=100)
    comment = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
