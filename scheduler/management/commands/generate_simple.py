from django.core.management.base import BaseCommand
from scheduler.views import generate_simple_schedule

class Command(BaseCommand):
    def generate_schedule(self):
        generate_simple_schedule()

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Generating a Simple Timetable Schedule'))
        self.generate_schedule()
        self.stdout.write(self.style.SUCCESS('DONE'))