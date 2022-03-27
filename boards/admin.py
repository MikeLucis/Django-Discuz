from django.contrib import admin

from .models import Board, DocFile, Banner, HotTopics

# Register your models here.

admin.site.register(Board)
admin.site.register(Banner)
admin.site.register(HotTopics)
admin.site.register(DocFile)
