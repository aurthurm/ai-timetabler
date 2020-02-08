import random as rnd
import prettytable
from django.conf import settings

from .models import *


class Class:
    def __init__(self, id, department, course):
        self._id = id
        self._department = department
        self._course = course
        self._instructor = None
        self._meetingTime = None
        self._room = None
    def get_id(self):
        return self._id
    def get_department(self):
        return self._department
    def get_course(self):
        return self._course
    def get_instructor(self):
        return self._instructor
    def get_meetingTime(self):
        return self._meetingTime
    def get_room(self):
        return self._room
    def set_instructor(self, instructor):
        self._instructor = instructor
    def set_meetingTime(self, meetingTime):
        self._meetingTime = meetingTime
    def set_room(self, room):
        self._room = room
    def __str__(self):
        return str(self._department.name) + ", " + \
               str(self._course.code) + ", " +  \
               str(self._room.name) + ", " +  \
               str(self._instructor.id) + ", " +  \
               str(self._meetingTime.id)


class Data:
    def __init__(self):
        self._rooms = ComplexRoom.objects.all()
        self._meetingTimes = ComplexMeetingTime.objects.all()
        self._instructors = ComplexInstructor.objects.all()
        self._courses = ComplexCourse.objects.all()
        self._departments = ComplexDepartment.objects.all()
        self._numberOfClasses = 0
        for department in self._departments:
            self._numberOfClasses += department.course_department.all().count()
    def get_departments(self):
        return self._departments
    def get_courses(self):
        return self._courses
    def get_instructors(self):
        return self._instructors
    def get_meetingTimes(self):
        return self._meetingTimes
    def get_rooms(self):
        return self._rooms
        
data = Data()


class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNumber = 0
        self._isFitnessChanged = False
    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes
    def get_numberOfConflicts(self):
        return self._numberOfConflicts
    def get_fitness(self):        
        self._fitness = self.calculateFitness()
        return self._fitness
    def initialise(self):
        departments = self._data.get_departments()
        for department in departments:
            courses = department.course_department.all()
            for course in courses:
                newClass = Class(self._classNumber, department, course)
                self._classNumber += 1
                newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0, data.get_meetingTimes().count())])
                newClass.set_room(data.get_rooms()[rnd.randrange(0, data.get_rooms().count())])
                newClass.set_instructor(course.instructors.all()[rnd.randrange(0, course.instructors.all().count())])
                self._classes.append(newClass)
        return self
    def calculateFitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):
            if (classes[i].get_room().capacity < classes[i].get_course().max_students):
                self._numberOfConflicts  += 1
            for j in range(0, len(classes)):
                if j >= i :
                    if (classes[i].get_meetingTime() == classes[j].get_meetingTime() and classes[i].get_id() != classes[j].get_id()):
                        if (classes[i].get_room() == classes[j].get_room()):
                            self._numberOfConflicts  += 1
                        if (classes[i].get_instructor() == classes[j].get_instructor()):
                            self._numberOfConflicts  += 1
        return 1/(1.0*self._numberOfConflicts + 1)
    
    def __str__(self):
        returnValue: str = ""
        for i in range(0, len(self.classes) - 1):
            returnValue += str(self.classes[i]) + ", "
        returnValue += str(self._classes[len(self._classes) - 1])
        return returnValue
        

class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range(0, size):
            self._schedules.append(Schedule().initialise())
    def get_schedules(self):
        return self._schedules


class GeneticAlgo:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))
    def _crossover_population(self, population):
        crossover_population = Population(0)
        for i in range(0, settings.NUMBER_OF_ELITE_SCHEDULES):
            crossover_population.get_schedules().append(population.get_schedules()[i])
        i = settings.NUMBER_OF_ELITE_SCHEDULES
        while i < settings.POPULATION_SIZE:
            schedule1 = self._select_tournament_population(population).get_schedules()[0]
            schedule2 = self._select_tournament_population(population).get_schedules()[0]
            crossover_population.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_population
    def _mutate_population(self, population):
        for i in range(settings.NUMBER_OF_ELITE_SCHEDULES, settings.POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population
    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialise()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if(rnd.random() > 0.5):
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule
    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialise()
        for i in range(0, len(mutateSchedule.get_classes())):
            if(settings.MUTATION_RATE > rnd.random()):
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule
    def _select_tournament_population(self, population):
        tournament_population = Population(0)
        i = 0
        while i < settings.TOURNAMENT_SELECTION_SIZE:
            tournament_population.get_schedules().append(population.get_schedules()[rnd.randrange(0, settings.POPULATION_SIZE)])
            i += 1
            tournament_population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse = True)
        return tournament_population
        

class DisplayManager:
    def print_meeting_times(self):
        meetingtimeTable = prettytable.PrettyTable(["id", "Meeting Time"])
        meetingTimes = data.get_meetingTimes()
        for i in range(0, len(meetingTimes)):
            meetingtimeTable.add_row([meetingTimes[i].get_id(), meetingTimes[i].get_time()])
        print(meetingtimeTable)
        
    def print_generation(self, population):
        table1 = prettytable.PrettyTable(["Schedule", "Fitness", "# of Conflicts", "classes [dpt, class, room, instructor, Meeting Time]"])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([
                str(i), 
                round(schedules[i].get_fitness(), 3), 
                schedules[i].get_numberOfConflicts(), 
                #schedules[i].get_classes() +
                " [" + "..." + "]",
            ])
        print(table1)
        
    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(["Class #", "Dept", "Course (# , max # of students)", "Room (Capacity)", "Instructor (ID)", "Meeting Time (ID)"])
        for i in range(0, len(classes)):
            table.add_row([
                str(i), classes[i].get_department().name, 
                classes[i].get_course().name + " (" + str(classes[i].get_course().code) + ", " + str(classes[i].get_course().max_students) + ")",
                classes[i].get_room().name + " (" + str(classes[i].get_room().capacity) + ")",
                classes[i].get_instructor().name + " (" + classes[i].get_instructor().code + ")",
                classes[i].get_meetingTime().times + " (" + classes[i].get_meetingTime().code + ")",
            ])
        print(table)

    def save_schedule(self, schedule):
        print("Saving New Complex Schedule")

        c_schedule = ComplexSchedule.objects.create()
        if c_schedule:
            print("New complex schedule instance created")
        else:
            print("New complex schedule instance failed")
            
        classes = schedule.get_classes()
        for i in range(0, len(classes)):
            _class = classes[i]
            c_class = ComplexClass.objects.create(
                course = _class.get_course(),
                room = _class.get_room(),
                instructor = _class.get_instructor(),
                meeting_time = _class.get_meetingTime()
            )
            c_schedule.classes.add(c_class)
            print(f"Added class {_class} to schedule")
