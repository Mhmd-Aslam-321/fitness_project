from django.db import IntegrityError, transaction
from django.utils.timezone import now
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Booking, FitnessClass
from .serializers import BookingSerializer, FitnessClassSerializer, BookingPostSerializer


class ClassListView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description="Retrieve all bookings for a user",
        responses={200: BookingSerializer()},
    )
    def get(self, *args, **kwargs):
        class_objs = FitnessClass.objects.filter(datetime__gte=now())
        serializer = FitnessClassSerializer(class_objs, many=True)
        return Response(serializer.data)


class BookPostView(APIView):
    permission_classes = [AllowAny]
    class KwargsValidationSerializer(serializers.Serializer):
        class_id = serializers.IntegerField(required=True)

    @swagger_auto_schema(
        request_body=BookingPostSerializer(),
        responses={200: "{'success': 'Booking successful'}"},
    )
    def post(self, *args, **kwargs):
        kwargs_serializer = self.KwargsValidationSerializer(data=kwargs)
        if not kwargs_serializer.is_valid():
            return Response(
                kwargs_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        fitness_class_id = kwargs_serializer.validated_data.get("class_id", None)

        try:
            fitness_class_obj = FitnessClass.objects.get(id=fitness_class_id)
        except FitnessClass.DoesNotExist:
            return Response(
                {"detail": "Fitness class does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BookingPostSerializer(data=self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        client_name = serializer.validated_data.get("client_name", None)
        client_email = serializer.validated_data.get("client_email", None)

        if fitness_class_obj.available_slots > 0:
            with transaction.atomic():  # should be atomic
                fitness_class_obj.available_slots -= 1
                fitness_class_obj.save()
                try:
                    booking_obj = Booking.objects.create(
                        fitness_class=fitness_class_obj,
                        client_name=client_name,
                        client_email=client_email,
                    )

                except IntegrityError:
                    return Response(
                        {"error": "You have already booked this class."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                BookingSerializer(booking_obj).data, status=status.HTTP_201_CREATED
            )
        
        return Response(
            {"error": "No available slots"}, status=status.HTTP_400_BAD_REQUEST
        )


class BookingListView(APIView):
    permission_classes = [AllowAny]
    class QuerySerializer(serializers.Serializer):
        email = serializers.EmailField(required=True)

    @swagger_auto_schema(
        operation_description="Retrieve all bookings for a user",
        query_serializer=QuerySerializer(),
        responses={200: BookingSerializer()},
    )
    def get(self, *args, **kwargs):
        query_serializer = self.QuerySerializer(data=self.request.query_params)
        if not query_serializer.is_valid():
            return Response(
                query_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = query_serializer.validated_data.get("email", None)
        bookings = Booking.objects.filter(client_email=email)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
