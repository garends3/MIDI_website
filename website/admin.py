# Register your models here.
from django.contrib import admin
from .models import Person, ResearchTheme, Publication


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "slug")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(ResearchTheme)
admin.site.register(Publication)