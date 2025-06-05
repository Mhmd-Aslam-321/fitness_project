from rest_framework import serializers

from ..models import Booking, FitnessClass


class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ["id", "name", "datetime", "instructor", "available_slots"]


class BookingPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["client_name", "client_email"]


class BookingSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer()

    class Meta:
        model = Booking
        fields = ["id", "client_name", "client_email", "fitness_class"]
