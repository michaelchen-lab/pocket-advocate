from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    profile = models.JSONField(null=True, blank=True)
    recommendations = models.JSONField(null=True, blank=True)

class Symptom(models.Model):
    ''' All possible symptoms accepted by application '''
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

class SymptomRecord(models.Model):
    ''' Symptoms logged by users '''
    user = models.ForeignKey(User, related_name="SymptomRecords", on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, related_name="Logs", on_delete=models.CASCADE)
    
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
