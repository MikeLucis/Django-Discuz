from django.contrib import admin

from .models import Board, Banner, HotTopics

# Register your models here.

admin.site.register(Board)
admin.site.register(Banner)
admin.site.register(HotTopics)
