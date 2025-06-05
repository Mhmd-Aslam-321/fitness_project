from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from fitness.models import FitnessClass  

class Command(BaseCommand):
    help = 'Create sample fitness classes'

    def handle(self, *args, **options):
        classes = [
            ("Yoga", "John", 10),
            ("Zumba", "Aslam", 15),
            ("HIIT", "Yedu", 8),
        ]

        now = timezone.now()

        for i, (name, instructor, slots) in enumerate(classes):
            class_time = now + timedelta(days=i+1)
            obj, created = FitnessClass.objects.get_or_create(
                name=name,
                datetime=class_time,
                instructor=instructor,
                defaults={'total_slots':20 , 'available_slots': slots}
            )
            status = "Created" if created else "Already exists"
            self.stdout.write(f"{status}: {name} on {class_time.strftime('%Y-%m-%d %H:%M')}")

        self.stdout.write(self.style.SUCCESS("✅ Sample fitness classes added successfully!"))
