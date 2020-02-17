from django.db import models


class SimpleDay(models.Model):
    """
    Day a course can be taken 
    e.g: "Wednesday"
    """
    name = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.name


class SimpleTime(models.Model):
    """
    Time a course can be taken 
    e.g: "08:00 - 10:00"
    """
    name = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.name


class SimpleDayTime(models.Model):
    """
    Allocated Day and Time a course is supposed to be taught:
    The Genetic Algorithm is all about allocating these.
    """
    day = models.ForeignKey(
        "SimpleDay",
        on_delete = models.CASCADE,
        related_name="daytime_day"
    )
    time = models.ForeignKey(
        "SimpleTime",
        on_delete = models.CASCADE,
        related_name="daytime_time"
    )

    def __str__(self):
        return str(self.day) + " " + str(self.time)


class SimpleCourse(models.Model):
    """
    Assumption : Each course has one known instructor 
                 already allocated to teach.
    """
    name = models.CharField(
        max_length=255
    )
    frequency = models.IntegerField()

    def __str__(self):
        return self.name


class SimpleInstructor(models.Model):
    """
    Course Instructors:
    An instructor will have only a single course he/she teaches
    FKey() of SimpleCourse
    """
    name = models.CharField(
        max_length=255
    )
    course = models.ForeignKey(
        "SimpleCourse",
        on_delete = models.CASCADE
        )

    def __str__(self):
        return self.name # +  " : " + self.course.name


class SimpleCourseAssignment(models.Model):
    """
    Course Assignmenst:
    days and times a course can be taken for a generated schedule
    """
    course = models.ForeignKey(
        "SimpleCourse",
        on_delete = models.PROTECT
    )
    times = models.ManyToManyField(
        "SimpleDayTime",
        blank = True,
        related_name="assigned_times"
    )

    def __str__(self):
        return "Asmnt for " +  str(self.course.name)

class SimpleSchedule(models.Model):
    """
    Fittest Generation :
    schedule
    """
    created = models.DateTimeField(auto_now=True)
    assignments = models.ManyToManyField(
        "SimpleCourseAssignment",
        blank=True,
        related_name="schedule_assignment"
    )

    def __str__(self):
        return "Schedule: " + str(self.created)