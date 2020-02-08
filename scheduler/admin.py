from django.contrib import admin
from .models import (
    # Simple GA Models
    SimpleDay,
    SimpleTime,
    SimpleDayTime,
    SimpleInstructor,
    SimpleCourse,
    SimpleSchedule,
    SimpleCourseAssignment,
    # Complex GA Models
    ComplexRoom,
    ComplexMeetingTime,
    ComplexInstructor,
    ComplexDepartment,
    ComplexCourse,
    ComplexClass,
    ComplexSchedule,

    #
    GAType
)


admin.site.register(GAType)

# Simple GA Admin Panels
admin.site.register(SimpleDay)
admin.site.register(SimpleTime)
admin.site.register(SimpleDayTime)
admin.site.register(SimpleInstructor)
admin.site.register(SimpleCourse)
admin.site.register(SimpleSchedule)
admin.site.register(SimpleCourseAssignment)

# Complex GA Admin Panels
admin.site.register(ComplexRoom)
admin.site.register(ComplexMeetingTime)
admin.site.register(ComplexInstructor)
admin.site.register(ComplexDepartment)
admin.site.register(ComplexCourse)
admin.site.register(ComplexClass)
admin.site.register(ComplexSchedule)