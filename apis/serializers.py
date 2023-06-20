from rest_framework import serializers
from appointments.models import Appointment, Customer

class CustomerSerializer(serializers.ModelSerializer):
    """Provides serialised customer data to AppointmentManagement Class"""
    class Meta:
        model = Customer
        fields = ("name", "number", "id")

class AppointmentManagement(serializers.ModelSerializer):
    """Serialises appointment data for AppointmentManagement API.
    Customer Data is nested into appointment object data when necessary.
    (Not all appointments have customers)"""
    customer = CustomerSerializer(
        required=False
    )  # Nested data for customer details
    appointment_date = (
        serializers.SerializerMethodField()
    )  # Create a field for formatted date

    def get_appointment_date(self, obj):
        return obj.dom.strftime("%Y-%m-%d")  # Format the date as needed using strftime

    class Meta:
        model = Appointment
        fields = (
            "appointment_date",
            "future",
            "id",
            "time",
            "type",
            "dom",
            "booked",
            "customer",
        )

class AppointmentPatcher(serializers.ModelSerializer):
    """Serialiser for booked appointment. Binds the customer data to appointment data.
    Overrides the default representation of appointment object, adding customer name 
    and number to the Appointment object."""
    class Meta:
        model = Appointment
        fields = ["id", "type", "booked", "customer"]

    def to_representation(self, instance):
        # Customize the representation to include customer name and number
        #Access the to_representation method of the parent class
        apt_representation = super().to_representation(instance)
        #apt_representation is how the appointment instance is to be serialised
        apt_representation["customer_name"] = instance.customer.name
        #add new fields to the serialised data, from the Foreign key of ap't model
        apt_representation["customer_number"] = instance.customer.number
        return apt_representation

class AppointmentCancellationSerializer(serializers.Serializer):
    """Serialises customer data for the POST request from customer to 'cancel' their appointment."""
    customer_id = serializers.IntegerField()
    id = serializers.IntegerField()

class AppointmentBookingSerializer(serializers.ModelSerializer):
    """Serialises appointment object and changes the 'time' field 
    from a datetime object into a formatted string."""
    time = serializers.SerializerMethodField()

    def get_time(self, obj):
        return obj.time.strftime("%I %p").lstrip("0")

    class Meta:
        model = Appointment
        fields = "__all__"

class MyAppointmentsSerializer(serializers.ModelSerializer):
    """Serialises appointment object, adding formatted_date, formatted_time,
    and price_time to serialised appointment data.
    adds formatted date string from the date(datetime object).
    adds formatted date string from the time(time object).
    creates new 'price_time' field for customer to see."""
    formatted_date = serializers.SerializerMethodField()
    formatted_time = serializers.SerializerMethodField()
    price_time = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            "id",
            "type",
            "time",
            "dom",
            "booked",
            "future",
            "customer",
            "formatted_date",
            "formatted_time",
            "price_time",
        ]

    def get_formatted_date(self, obj):
        return obj.dom.strftime("%A, %d %B")

    def get_formatted_time(self, obj):
        return obj.time.strftime("%-I%p")

    def get_price_time(self, obj):
        #Probably would have been better to integrate this into model
        if obj.type == "Acrylic Nails":
            price_time = "£25, 1 hour appointment"
        elif obj.type == "Acrylic Toes":
            price_time = "£25, 1 hour appointment"
        elif obj.type == "Nails & Toes":
            price_time = "£40, 2 hour appointment"
        return price_time
