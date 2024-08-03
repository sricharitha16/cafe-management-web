from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    security_question = models.CharField(max_length=255, default='admin')
    security_answer = models.CharField(max_length=255, default='admin')
    
    def set_security_answer(self, raw_answer):
        self.security_answer = make_password(raw_answer)

    class Meta:
        app_label = 'users'

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images/', default='default_event_image.jpg')
    participants = models.ManyToManyField(User, related_name='events_participants', blank=True)

    def __str__(self):
        return self.title

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Feedback from {self.name}"

class Item(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='item_images/', default='default_item_image.jpg')
