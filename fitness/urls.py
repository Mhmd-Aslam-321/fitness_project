from django.urls import include, path

urlpatterns = [
    path("v1/", include("fitness.v1.urls")),
]