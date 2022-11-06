from django.contrib import admin
from .models import ToDoList, Item
from register.models import Profile

admin.site.register(ToDoList)
admin.site.register(Item)
admin.site.register(Profile)
