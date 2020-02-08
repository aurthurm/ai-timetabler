from django.core.management.base import BaseCommand
from scheduler.views import generate_complex_schedule

class Command(BaseCommand):
    def generate_schedule(self):
        generate_complex_schedule()

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Generating a Complex Timetable Schedule'))
        self.generate_schedule()
        self.stdout.write(self.style.SUCCESS('DONE'))