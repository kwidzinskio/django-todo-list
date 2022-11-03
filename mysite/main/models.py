from django.db import models
from django.urls import reverse


class ToDoList(models.Model): #Contest
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse("main:view-list-view", kwargs={"id": self.id})

    def __str__(self):
        return self.name

class Item(models.Model): # Vote
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300, null=True)
    complete = models.BooleanField()
    deadline = models.DateField(null=True)

    def __str__(self):
        return self.text

