from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import FitnessClass, Booking
from django.utils import timezone
from datetime import timedelta

class BookingAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            datetime=timezone.now() + timedelta(days=1),
            instructor="Alice",
            total_slots=10,
            available_slots=5
        )

        self.fitness_class2 = FitnessClass.objects.create(
            name="Zumba",
            datetime=timezone.now() + timedelta(days=2),
            instructor="Bob",
            total_slots=10,
            available_slots=0
        )
          
        self.classes_url = reverse('class-list')  


    def test_get_classes(self):
        response = self.client.get(self.classes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)


    def test_book_class_success(self):
        booking_url = reverse('book-class', kwargs={'class_id': self.fitness_class.id})
        data = {
            "fitness_class": self.fitness_class.id,
            "client_name": "aslam",
            "client_email": "aslam@test.com"
        }
        response = self.client.post(booking_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().client_email, "aslam@test.com")


    def test_book_class_failure_no_slots(self):
        booking_url = reverse('book-class', kwargs={'class_id': self.fitness_class2.id})
        data = {
            "client_name": "aslam",
            "client_email": "aslam@test.com"
        }
        response = self.client.post(booking_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_book_class_duplicate(self):
        booking_url = reverse('book-class', kwargs={'class_id': self.fitness_class.id})
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="aslam",
            client_email="aslam@test.com"
        )
        # Try booking again with same email and class
        data = {
            "fitness_class": self.fitness_class.id,
            "client_name": "aslam",
            "client_email": "aslam@test.com"
        }
        response = self.client.post(booking_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_bookings_by_email(self):
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="aslam",
            client_email="aslam@test.com"
        )
        url = reverse('booking-list') + '?email=aslam@test.com'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_bookings_missing_email(self):
        url = reverse('booking-list')  # no ?email= param
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
