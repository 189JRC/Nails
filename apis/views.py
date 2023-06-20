from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils import timezone

from appointments.models import Appointment, Customer, Record
from collections import defaultdict
from datetime import datetime
import json
from .serializers import (
    AppointmentManagement,
    AppointmentBookingSerializer,
    AppointmentPatcher,
    AppointmentCancellationSerializer,
    MyAppointmentsSerializer,
)

def update(past_appointments):
    """Takes a queryset of appointment objects that
    require update. Future == True is set to False"""
    for apt in past_appointments:
        if apt.future == True:
            apt.future = False
            apt.save()

@staff_member_required
def create_record(request, id):
    """Takes an Appointment id and creates a Record object. 
    The Appointment object is deleted."""
    
    apt = Appointment.objects.get(pk=id)
    # Extract form data from the request
    payload = json.loads(request.body)
    earnings = payload.get("Earnings")
    earnings = int(earnings)

    if apt.booked == True:
        rec = Record.objects.create(
            type=apt.type,
            time=apt.time,
            dom=apt.dom,
            booked=True,
            customer=apt.customer,
            acknowledged=True,
            earnings=earnings,
        )
        rec.save()
        apt.delete()
        return JsonResponse({"OK": f"{id} deleted", "Record Created": rec.id})
    else:
        apt.delete()
        return JsonResponse({"OK": f"{id} deleted", "No Record created": id})

class AppointmentManagement(generics.ListAPIView):
    """API endpoint to retrieve all appointments (future and past) along with
    any associated customer information.

    This endpoint is designed to provide data for the manager's planner view.
    
    The response provides:
    - 'date': A formatted date string (e.g., "Monday, 05 June").
    - 'appointments': An array of appointment objects for the given date."""
    
    permission_classes = [IsAdminUser]
    serializer_class = AppointmentManagement
    queryset = Appointment.objects.all()

    def get(self, request, *args, **kwargs):
        #Override the default get method of ListAPIView
        response = super().get(request, *args, **kwargs)
        #Get appointments data from response
        appointment_objects = response.data #data = list of appointment objects
        # Make an empty default dict to sort dates and appointments in loop below
        grouped_data = defaultdict(list)
        #loop over the appointments
        for appointment_object in appointment_objects:
            #extract appointment date from the appointment object 
            appointment_date = appointment_object.pop("appointment_date")
            #use strptime to convert appointment_date str into a datetime object
            #use strftime to format the dt object as "Monday, 05 June"
            formatted_date = datetime.strptime(appointment_date, "%Y-%m-%d").strftime(
                "%A, %d %B"
            )
            #Update the grouped_data dict with key = formatted date and value as the apt object itself
            grouped_data[formatted_date].append(appointment_object)

        # Format the response data into a a list of regular dicts
        formatted_data = []
        for date, appointments in grouped_data.items():
            formatted_data.append({"date": date, "appointments": appointments})

        response.data = formatted_data
        return response

class AppointmentView(generics.ListAPIView):
    """This Get endpoint is designed to provide data for the customer's booking page.

    Included is a mechanism to update appointment status for any appointments that are
    now in the past (by changing future=True to False). This is achieved by 
    calling the update() function. The intention here is to never allow past appointments 
    to be visible to the end user.

    The response provides:
    - 'date': A formatted date string (e.g., "Monday, 05 June").
    - 'appointments': An array of appointment objects for the given date."""

    serializer_class = AppointmentBookingSerializer

    def list(self, request):
        # get all apts with future == True
        potential_future_appointments = Appointment.objects.filter(future=True)
        # see if any have a dom lt today -> (put into a list) make these future = False
        apts_to_update = [
            a for a in potential_future_appointments if a.dom < timezone.now().date()
        ]
        # see if any have a dom == today
        todays_apts_maybe_update = [
            a for a in potential_future_appointments if a.dom == timezone.now().date()
        ]
        # see if any have a time lt now -> make these future = False
        todays_apts_need_update = [
            a for a in todays_apts_maybe_update if a.time < timezone.now().time()
        ]
        apts_to_update += todays_apts_need_update
        # run this through a function
        update(apts_to_update)
        #get list of ids for the actual future appointments
        actual_future_appointments = [
            a.id for a in potential_future_appointments if a not in apts_to_update
        ]
        # order them by time & dom
        queryset = (
            Appointment.objects.filter(id__in=actual_future_appointments)
            .order_by("time")
            .order_by("dom")
        )
        # run them through the loop to arrange them into a dict
        # serialise them
        # send response
        appointments = {}

        for appointment in queryset:
            #dict to have key: datestring ("Monday, 05 June"), value: empty list
            date = appointment.dom.strftime("%A, %d %B")
            if date not in appointments:
                appointments[date] = []

            #serialise the appointment so that it has all required data
            serializer = self.serializer_class(appointment)
            #append apt data to the dict value (which is a list)
            appointments[date].append(serializer.data)

        #appointments key: datestring ("Monday, 05 June"), value: list of dicts (containing apt data for the given date), phew!
        return Response(appointments)

class AppointmentBookingView(generics.UpdateAPIView):
    """Allows patch requests to be made, changing a vacant appointment
    into booked=True. Changes appointment's type into customer's desired type, 
    binds customer name and number to the appointment object."""

    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentPatcher


    def patch(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response(
                {"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Extract form data from the request, this is provided by the submitted form
        customer_id = int(request.data.get("c_id"))
        number = request.data.get("number")
        type = request.data.get("type")
        name = request.data.get("name") #redundant, might be problematic if different customers have same name

        # Retrieve the customer object
        customer = Customer.objects.get(id=customer_id)

        # Update appointment object with form data, binding appointment with customer
        #Save objects as required
        appointment.booked = True
        appointment.type = type
        appointment.customer = customer
        appointment.customer.number = number
        appointment.customer.save()
        appointment.save()
        
        #Serialise data and return confirmation
        serializer = AppointmentPatcher(appointment)
        return Response(serializer.data)

class AppointmentCancellationView(generics.CreateAPIView):
    """Allows post requests to be made, for customer to cancel their appointment. 
    Resets appointment data to default status, as if it were never actually booked.
    Changes appointment's type into customer's desired type, 
    binds customer name and number to the appointment object."""
    permission_classes = [IsAuthenticated]

    def post(self, request, appointment_id):
        #Get apt and customer data from request
        customer_id = request.data.get("customer_id")
        appointment_id = request.data.get("appointment_id")
        #catch potential errors
        if not customer_id or not appointment_id:
            return Response(
                {"error": "Customer ID and Appointment ID are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            appointment = Appointment.objects.get(
                id=appointment_id, customer_id=customer_id
            )
        except Appointment.DoesNotExist:
            return Response(
                {"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
            )
        #reset appointment status to default
        appointment.booked = False
        appointment.type = "Vacant"
        appointment.customer = None
        appointment.save()

        serializer = AppointmentCancellationSerializer(appointment)
        return Response(serializer.data)

class MyAppointments(generics.ListAPIView):
    """Customer API get endpoint for a customer to access their own booked appointments"""
    permission_classes = [IsAuthenticated]
    serializer_class = MyAppointmentsSerializer

    def get_queryset(self):
        customer_id = self.kwargs["customer_id"]
        queryset = Appointment.objects.filter(customer_id=customer_id)

        if not queryset.exists():
            return Response({
                "Error": "No appointments found for the specified customer."})

        return queryset





