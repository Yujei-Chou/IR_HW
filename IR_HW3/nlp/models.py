from django.db import models
# Create your models here.

class PubMed(models.Model):
    id = models.IntegerField(primary_key=True)   
    title = models.CharField(max_length=100000)
    abstract = models.CharField(max_length=100000)

class withoutPuncTokens(models.Model):
    word = models.CharField(max_length=1000)
    count = models.IntegerField()