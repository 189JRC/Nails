from django.shortcuts import render
from .models import Appointment, Customer
from datetime import datetime
import random

def user_home(request):
    """Renders user SPA page and calls functions to get
    user greeting and random quote."""
    customer = Customer.objects.get(user=request.user)    
    context = {"customer_id": customer.id, "customer_name": customer.name}
    context["greeting"] = time_of_day()
    context["quote"] = random_quote()
    return render(request, "user_appointments.html", context)

def time_of_day():
    time = int(datetime.now().strftime("%H"))
    if time < 12:
        greeting = "Good Morning"
    elif 11 < time < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    return greeting

def random_quote():
    quotes = [
        "Everything has beauty, but not everyone sees it.",
        "Beauty is in the eye of the beholder.",
        "Beauty is not in the face; it is a light in the heart.",
    ]
    select = random.randint(0, len(quotes) - 1)
    return quotes[select]
    

