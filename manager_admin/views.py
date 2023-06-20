from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from appointments.models import Appointment, Customer, User
from datetime import date, datetime, timedelta
from datetime import time as t
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from appointments.views import time_of_day


def home(request):
    context = {"greeting": time_of_day()}
    return render(request, "home.html", context)

def delete_apt(request, id):
    if request.method == "GET":
        obj = Appointment.objects.filter(pk=id)
        obj.delete()
        return JsonResponse({"message": "appointment deleted successfully"})

# this will be rendered obsolete with an affective API endpoint
def appointment_dict():
    """Make a dictionary of future appointments with KEY='date' VALUE='weekday'"""
    try:
        appointments = Appointment.objects.filter(future=True)
        appointment_dict = {}
        for apt in appointments:
            k = apt.dom
            if k in appointment_dict:
                pass
            else:
                appointment_dict[k] = apt.dom.strftime("%A")
        return appointment_dict
    except:
        return None

def latest_appointment():
    try:
        return Appointment.objects.last().dom
    except:
        return datetime.today()

# This function enables Vic to create new appointment schedule
def generate(request):
    """Generates a full standard calendar work week starting from soonest Monday after today"""

    # Find latest appointment
    next_available = latest_appointment()

    while next_available.strftime("%A") != "Monday":
        next_available += timedelta(days=1)

    # create list of dates for new appointments
    apt_dates = []
    while len(apt_dates) < 7:
        apt_dates.append(next_available)
        next_available += timedelta(days=1)

    # fill list of days with appointments at specific times
    # times = [t(10), t(11), t(12), t(13), t(14), t(15), t(16), t(17)]

    for date in apt_dates:
        if date.strftime("%A") == "Saturday" or date.strftime("%A") == "Sunday":
            pass
        else:
            for time in Appointment.TIME_SLOTS:
                Appointment.objects.create(type="Vacant", time=time[0], dom=date)

    # return all appointments
    appointments = Appointment.objects.all()

    context = {
        "appointments": appointments,
        "next_available": next_available,
    }
    return redirect("manager_admin:planner")

def planner(request):
    today = date.today()
    next_available = latest_appointment()

    full_day = timedelta(days=1)
    while next_available.strftime("%A") != "Monday":
        next_available += full_day
    next_available_weekday = next_available.strftime("%A")

    appointments = Appointment.objects.all()
    booked_appointments = Appointment.objects.filter(booked=True, future=True)
    context = {
        "appointments": appointments,
        "today": today.strftime("%A, %d %B"),
        "next_available": next_available,
        "next_available_weekday": next_available_weekday,
        "appointment_dict": appointment_dict(),
        "booked_appointments": booked_appointments,
    }
    return render(request, "planner.html", context)
