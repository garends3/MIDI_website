
# Register your models here.
from django.contrib import admin
from .models import Person, ResearchTheme, Publication

admin.site.register(Person)
admin.site.register(ResearchTheme)
admin.site.register(Publication)