from django.db import models
from django.contrib.auth.models import User


class Appointment(models.Model):
    TIME_SLOTS = [
        ("10:00", "10:00 AM"),
        ("11:00", "11:00 AM"),
        ("12:00", "12:00 PM"),
        ("13:00", "1:00 PM"),
        ("14:00", "2:00 PM"),
        ("15:00", "3:00 PM"),
        ("16:00", "4:00 PM"),
        ("17:00", "5:00 PM"),
    ]

    SERVICES = (
        ("Acrylic Nails", "Acrylic Nails"),
        ("Acrylic Toes", "Acrylic Toes"),
        ("Nails and Toes", "Nails and Toes"),
        ("Vacant", "Vacant"),
    )

    type = models.CharField(choices=SERVICES, max_length=20, null=True)
    time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    dom = models.DateField(null=True)
    booked = models.BooleanField(default=False)
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, null=True, default=None
    )
    future = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type} at {self.time} on {self.dom}, with {self.customer}"

    class Meta:
        unique_together = [["time", "dom"]]


class Customer(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = [["name", "user"]]


class Record(models.Model):
    type = models.CharField(max_length=20, null=True)
    time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    dom = models.DateField(null=True)
    booked = models.BooleanField(default=False)
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, null=True, default=None
    )
    acknowledged = models.BooleanField(default=False)
    earnings = models.IntegerField()

    def __str__(self):
        return f"{self.type} at {self.time} on {self.dom}, with {self.customer}: earnings: {self.earnings}"
