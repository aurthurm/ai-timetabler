from django.core.management.base import BaseCommand
from scheduler.models import ComplexSchedule

class Command(BaseCommand):
    def clear_schedule(self):
        schedules = ComplexSchedule.objects.all()
        for schedule in schedules:
            for _class in schedule.classes.all():
                _class.delete()
            schedule.delete()

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Deleting all available Complex Timetable Schedule'))
        self.clear_schedule()
        self.stdout.write(self.style.SUCCESS('DONE'))