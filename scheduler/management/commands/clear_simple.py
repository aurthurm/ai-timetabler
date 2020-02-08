from django.core.management.base import BaseCommand
from scheduler.models import SimpleSchedule

class Command(BaseCommand):
    def clear_schedule(self):
        schedules = SimpleSchedule.objects.all()
        for schedule in schedules:
            for assignment in schedule.assignments.all():
                assignment.delete()
            schedule.delete()

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Deleting all available Simple Timetable Schedule'))
        self.clear_schedule()
        self.stdout.write(self.style.SUCCESS('DONE'))