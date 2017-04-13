from django.contrib import admin

# Register your models here.

from .models import Question, Option, Vote

admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Vote)

