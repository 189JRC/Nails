from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponse
from .forms import LogInForm
from appointments.models import User, Customer

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            customer = Customer.objects.create(
                name=username, number="999", user=new_user
            )
            customer.save()

        except IntegrityError:
            return render(
                request,
                "register.html",
                {"message": "Username already taken."},
            )
        login(request, new_user)
        return redirect("/appointments")
    else:
        return render(request, "register.html")

def user_login(request):
    if request.method == "POST":
        form = LogInForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])

            if user is not None:
                login(request, user)
                if user.is_staff == True:
                    return redirect("/manager_admin/home")
                return redirect("/appointments")
            else:
                return HttpResponse("Invalid login.")
    else:
        form = LogInForm()
        context = {"form": form}
        return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))
