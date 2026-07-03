# Create your models here.
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="people/", blank=True)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ResearchTheme(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Publication(models.Model):
    pmid = models.CharField(max_length=50, unique=True, blank=True, null=True)  # add this
    title = models.CharField(max_length=500)
    authors = models.TextField()
    journal = models.CharField(max_length=500, blank=True)
    year = models.IntegerField(blank=True, null=True)
    link = models.URLField(blank=True)

class PhDThesis(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    year = models.IntegerField()
    link = models.URLField(blank=True, null=True)  # <-- added field for clickable link

    def __str__(self):
        return f"{self.title} ({self.year})"

    def __str__(self):
        return f"{self.title} ({self.year})"