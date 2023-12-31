from django.db import models
from django.contrib.auth.models import User
# https://docs.djangoproject.com/en/4.2/ref/contrib/auth/


# Create your models here.
"""class Product(models.model):
    title
    content
    price
    """
   
class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Room(models.Model):
    host =  topic = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    desription = models.TextField(null=True, blank=True)
    #participants = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['-updated', '-created']
        
        
    #string representation of this room 
    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50] #trim it down we only want the first 50 characters in the preview