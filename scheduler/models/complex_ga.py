from django.db import models


class ComplexRoom(models.Model):
    name = models.CharField(
        max_length=50
    )
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class ComplexMeetingTime(models.Model):
    times = models.CharField(
        max_length=50
    )
    code = models.CharField(
        max_length=50
    )

    def __str__(self):
        return self.times


class ComplexInstructor(models.Model):
    name = models.CharField(
        max_length=100
    )
    code = models.CharField(
        max_length=10
    )

    def __str__(self):
        return self.name


class ComplexDepartment(models.Model):
    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


class ComplexCourse(models.Model):
    name = models.CharField(
        max_length=100
    )
    code = models.CharField(
        max_length=10
    )
    instructors = models.ManyToManyField(
        "ComplexInstructor",
        blank=True,
        related_name="course_instructors"
    )
    max_students = models.IntegerField()
    department = models.ForeignKey(
        "ComplexDepartment",
        related_name="course_department",
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name


class ComplexClass(models.Model):
    """
    Final Scheduled class
    """
    course = models.ForeignKey(
        "ComplexCourse",
        on_delete=models.PROTECT
    )
    room = models.ForeignKey(
        "ComplexRoom",
        on_delete=models.PROTECT
    )
    instructor = models.ForeignKey(
        "ComplexInstructor",
        on_delete=models.PROTECT
    )
    meeting_time = models.ForeignKey(
        "ComplexMeetingTime",
        on_delete=models.PROTECT
    )

    def __str__(self):
        return "Class: " + self.course.name + " - " + self.room.name + " - " + self.instructor.name + " - " + str(self.meeting_time.times)


class ComplexSchedule(models.Model):
    """
    Fittest Generation :
    schedule
    """
    created = models.DateTimeField(auto_now=True)
    classes = models.ManyToManyField(
        "ComplexClass",
        blank=True,
        related_name="schedule_classes"
    )

    def __str__(self):
        return "Schedule: " +  str(self.created)