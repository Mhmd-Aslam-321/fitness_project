from django.urls import path

from .views import BookingListView, BookPostView, ClassListView

urlpatterns = [
    path("classes/", ClassListView.as_view(), name="class-list"),
    path("book/<int:class_id>/", BookPostView.as_view(), name="book-class"),
    path("bookings/", BookingListView.as_view(), name="booking-list"),
]
