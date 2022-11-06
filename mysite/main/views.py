from django.shortcuts import render
from .forms import CreateNewList
from django.http import HttpResponseRedirect, Http404
from .models import ToDoList
from django.urls import reverse
from django.db.models import Count, Q


def homepage_view(response):
    context = {
        "response": response
    }
    return render(response, "main/homepage.html", context)

def view_lists_view(response):
    if response.user.is_authenticated:
        todo_lists = ToDoList.objects.filter(user=response.user).annotate(
            imcompleted_tasks_qty=Count('item', filter=Q(item__complete=False)))
    else:
        return render(response, "register/log_in_first.html", {})

    context = {
        "response": response,
        "todo_lists": todo_lists,
    }
    return render(response, "main/view_lists.html", context)

def create_list_view(response):
    if response.user.is_authenticated:
        if response.method == "POST":
            form = CreateNewList(response.POST)

            if form.is_valid():
                name = form.cleaned_data["name"]
                to_do_list = ToDoList(name = name)
                to_do_list.save()
                response.user.todolist.add(to_do_list)
                return HttpResponseRedirect(reverse('main:view-list-view', kwargs={"id": to_do_list.id}))

        else:
            form = CreateNewList()

        context = {
                   "response": response,
                   "form": form
                   }
        return render(response, "main/create_list.html", context)

    else:
        return render(response, "register/log_in_first.html", {})

def view_list_view(response, id):
    try:
        if response.user.is_authenticated:
            list = ToDoList.objects.filter(user=response.user).get(id=id)
        else:
            response.user = None
            list = ToDoList.objects.filter(user=response.user).get(id=id)
    except ToDoList.DoesNotExist:
        raise Http404

    def check_all_changes():
        # task name change
        text = response.POST.get("name" + str(task.id))
        task.text = text

        # task deadline change
        deadline = response.POST.get("ddl" + str(task.id))
        if str(deadline) == "":
            deadline = None
        task.deadline = deadline

        # task done change
        if response.POST.get("done" + str(task.id)) == "clicked":
            task.complete = True
        else:
            task.complete = False

        task.save()

    # save changes to the list
    if response.POST.get("save"):
        for task in list.item_set.all():
            check_all_changes()

    # add new item
    elif response.POST.get("newTask"):
        print('afasasa')
        text = response.POST.get("newTask")
        deadline = response.POST.get("taskDeadline")
        if str(deadline) == "":
            deadline = None
        for task in list.item_set.all():
            check_all_changes()
        list.item_set.create(text=text, deadline=deadline, complete=False)

    # delete list
    elif response.POST.get("deleteList"):
        list.delete()
        return HttpResponseRedirect(reverse('main:view-lists-view',))

    # delete task
    for task in list.item_set.all():
        if response.POST.get("remove" + str(task.id)):
            task.delete()
            for task in list.item_set.all():
                check_all_changes()

    context = {
        "response": response,
        "list": list
    }

    return render(response, "main/view_list.html", context)
