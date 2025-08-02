# board/admin.py
from django.contrib import admin
from .models import Board, List, Card

class BoardAdmin(admin.ModelAdmin):
    # This makes the ManyToManyField easier to use in the admin
    filter_horizontal = ('members',)

admin.site.register(Board, BoardAdmin) # Register Board with the custom admin class
admin.site.register(List)
admin.site.register(Card)