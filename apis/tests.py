from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from appointments.models import Appointment, Customer, Record

class AppointmentManagementTest(APITestCase):
    """Test to ensure that appointment/customer data provided
    by the GET API endpoint ('/api/appointments/management') is accessible
    only to an admin/superuser and not to a regular user."""

    def setUp(self):
        """Create temporary user and admin user objects."""
        self.user = User.objects.create_user(
            username="regularuser", password="password123"
        )
        self.admin_user = User.objects.create_superuser(
            username="adminuser", password="password123"
        )
        self.url_management = "/api/appointments/management"

    def test_admin_access(self):
        """Force authentication of the admin user and make a GET
        request to the API. An HTTP 200 response is expected."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_access(self):
        """Force authentication of the regular user and make a GET
        request to the API. An HTTP 403 response is expected."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AppointmentViewTest(APITestCase):
    """Test to ensure that appointment data provided
    by the GET API endpoint ('/api/appointments/view') is accessible
    only to a logged in user."""

    def setUp(self):
        """Create temporary user and admin user objects."""
        self.user = User.objects.create_user(
            username="regularuser", password="password123"
        )
        self.url = "/api/appointments/view"

    def test_user_access(self):
        """Force authentication of the regular user and make a GET
        request to the API. An HTTP 200 response is expected."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def non_user_forbidden(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#TODO: make tests for AppointmentView to ensure appointment 'Future' status is updated correctly
