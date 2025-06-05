from django.db import models

# Create your models here.


class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.datetime}"

    class Meta:
        indexes = [
            models.Index(fields=["datetime"]),
            models.Index(fields=["instructor"]),
            models.Index(fields=["name"]),
        ]


class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class}"

    class Meta:
        indexes = [
        models.Index(fields=["client_email"]),
        models.Index(fields=["fitness_class", "client_email"]),
        ]
        unique_together = ("fitness_class", "client_email")