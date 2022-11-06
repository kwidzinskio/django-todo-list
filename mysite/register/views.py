from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
import re
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.password_validation import password_validators_help_texts


# Create your views here.
def register_view(response):

    if response.method == "POST":
        form = RegisterForm(response.POST)

        if form.is_valid():
            form.save()
            return redirect("/")

    else:
        form = RegisterForm()

    context = {
        "form": form
    }

    return render(response, "register/register.html", context)

def profile_view(response):
    if response.user.is_authenticated:
        user = User.objects.get(id=response.user.id)
        password_validation = []
        password_validators = password_validators_help_texts()
        context = {
            "response": response,
            "user": user,
            "edit_username": False,
            "edit_email": False,
            "edit_password": False,
            "password_validation": password_validation,
            "password_validators": password_validators,
        }

        if response.POST.get("editUsername"):
            context["edit_username"] = True
        elif response.POST.get("saveNewUsername"):
            new_username = response.POST.get("newUsername")
            if len(new_username) > 3:
                user.username = new_username
                user.save()
                messages.success(response, 'Your username was successfully updated!')
                return HttpResponseRedirect(reverse('register:profile-view',))
            else:
                messages.error(response, 'Your username must contain at least 5 characters!')
                context["edit_username"] = True

        elif response.POST.get("editEmail"):
            context["edit_email"] = True
        elif response.POST.get("saveNewEmail"):
            new_email = response.POST.get("newEmail")
            if re.search("(?i:^[a-z0-9]+\.?[a-z0-9]+@[a-z]+\.[a-z]{2,3}$)", new_email):
                user.email = new_email
                user.save()
                messages.success(response, 'Your email was successfully updated!')
                return HttpResponseRedirect(reverse('register:profile-view', ))
            else:
                messages.error(response, 'Your email is invalid!')
                context["edit_email"] = True


        elif response.POST.get("editPassword"):
            context["edit_password"] = True
        elif response.POST.get("csrfmiddlewaretoken"): #todo
            old_password = response.POST.get("oldPassword")
            new_password = response.POST.get("newPassword")
            new_password_repeat = response.POST.get("newPasswordRepeat")
            if len(new_password) >= 8 == None and user.check_password(old_password) and new_password == new_password_repeat:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(response, user)
                messages.success(response, 'Your password was successfully updated!')
            else:
                if not len(new_password) >= 8:
                    password_validation.append("Password too short")
                if not user.check_password(old_password):
                    password_validation.append("Old password doesn't match")
                if not new_password == new_password_repeat:
                    password_validation.append("Passwords are not the same")
                [messages.error(response, password_validation[i]) for i in range(len(password_validation))]
                context["edit_password"] = True

        return render(response, "register/profile.html", context)

    else:
        return render(response, "register/log_in_first.html", {})