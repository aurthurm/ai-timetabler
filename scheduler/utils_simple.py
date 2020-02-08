import random as rnd
import prettytable
from django.conf import settings

from .models import *

courses = SimpleCourse.objects.all().order_by('id')
days = SimpleDay.objects.all().order_by('id')
timeslots = SimpleTime.objects.all().order_by('id')


def random_index(items) -> int:
	return rnd.randint(0, len(items) - 1)


class Schedule:
    def __init__(self):
        self._classes = []
        self._fitness = -1
        self._conflicts = 0        
    def get_classes(self): 
        return self._classes
    def get_conflicts(self): 
        return self._conflicts
    def get_fitness(self): 
        self._fitness = self.calculate_fitness()
        return self._fitness
    def set_classes(self, course): 
        self._classes.append(course)
    def initialise(self):
        for course in courses:
            new_class = {
                '_course': course.name,
                '_teacher': course.simpleinstructor_set.first().id,
                '_times': []
            }
            for i in range(0, course.frequency):
                new_class['_times'].append((random_index(days), random_index(timeslots)))
            self._classes.append(new_class)
        return self
    def calculate_fitness(self):

        # 1. More than 1 course taught at the same timeslot in a single day
        time_slots = []
        for k, course in enumerate(self.get_classes()):
            time_slots += course['_times']

        unique_slots = set(time_slots)
        for _slot in unique_slots:
            time_conflicts = time_slots.count(_slot)
            if time_conflicts > 1:
                self._conflicts += time_conflicts - 1
                # print(f"{_slot} {time_conflicts} {self._conflicts} conflict")

        # 2. A day without free study time

        # 3. Having the same course more than once in a single day            
        for k, course in enumerate(self.get_classes()):
            # get all asigned times for this course instance
            course_slots = course['_times']
            # arange assigned times into days
            _dayz = {}
            for i in range(0, days.count()):
                _dayz[i] = []
                for slt in course_slots:
                    if i == slt[0]:
                        _dayz[i].append(slt)
            # each day must have a single slot
            for k, v in _dayz.items():
                if len(v) > 1:
                    self._conflicts += 1
            

        # 4. A full day without lectures or study only
        day_slots = [day[0] for day in time_slots]
        self._conflicts += [(i in day_slots) for i in range(0, 4)].count(False) # range 0, 4 mon - friday

        # Get Fitness
        # print(self._conflicts)
        return (1/(1.0*(self._conflicts + 1)))
        

class Population:
    def __init__(self, size):
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
        

def print_population(schedules):
    table1 = prettytable.PrettyTable(["Schedule", "Fitness", "# of Conflicts"])
    for k, schedule in enumerate(schedules):
        table1.add_row([
            str(k), 
            round(schedule.get_fitness(), 3), 
            schedule.get_conflicts()
        ])
    print(table1)


def print_fittest_schedule(fit_schedule):
    table2 = prettytable.PrettyTable(["Time/Day", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

    table_rows = {}
    for k, v in enumerate(timeslots):
        table_rows[k] = [v, '', '', '', '', '']
        
    for key, course in enumerate(fit_schedule.get_classes()):
        subj : str = course['_course']
        teacher_id: str = course['_teacher']
        slots: list = course['_times']

        # save to db

        # print
            
        for k, slot in enumerate(slots):
            #slot (day, course)
            day_index = slot[0] 
            day = days[day_index]
            time_index = slot[1]
            time = timeslots[time_index]
            
            if teacher_id != None:
                teacher = SimpleInstructor.objects.get(pk=teacher_id).name
            else:
                teacher = ""

            message = subj + "\n" + teacher + "\n"

            active = table_rows[time_index]
            active_tim = active[0]
            active_mon = active[1]
            active_tue = active[2]
            active_wed = active[3]
            active_thu = active[4]
            active_fri = active[5]

            if day_index == 0:
                active_mon += message
                table_rows[time_index] = [active_tim, active_mon, active_tue, active_wed, active_thu, active_fri]
            elif day_index == 1:
                active_tue += message
                table_rows[time_index] = [active_tim, active_mon, active_tue, active_wed, active_thu, active_fri]
            elif day_index == 2:
                active_wed += message
                table_rows[time_index] = [active_tim, active_mon, active_tue, active_wed, active_thu, active_fri]
            elif day_index == 3:
                active_thu += message
                table_rows[time_index] = [active_tim, active_mon, active_tue, active_wed, active_thu, active_fri]
            else:
                active_fri += message
                table_rows[time_index] = [active_tim, active_mon, active_tue, active_wed, active_thu, active_fri]

    for k, _row in table_rows.items():
        table2.add_row(_row)
        
    print(table2)


def save_simple_population(fit_schedule):

    print("Saving fittest Schedule >>")

    new_schedule = SimpleSchedule.objects.create()
    
    if new_schedule:
        print("New schedule instance created")
    else:
        print("New schedule instace creation failed")
        
    for key, course_ in enumerate(fit_schedule.get_classes()):
        subj : str = course_['_course']
        teacher_id: str = course_['_teacher']
        slots: list = course_['_times']

        _course = SimpleCourse.objects.get(name__exact=subj)

        if _course:
            assignment = SimpleCourseAssignment.objects.create(
                course = _course
            )

            if assignment and slots:
                for slot in slots:
                    d, t = slot[0], slot[1]
                    _d, _t = days[d], timeslots[t]
                    day_time, created = SimpleDayTime.objects.get_or_create(
                        day = _d,
                        time = _t
                    )
                    assignment.times.add(day_time)
            
                new_schedule.assignments.add(assignment)

            print(f"Course {_course.name} assigned")
            
        else:
            print("course does not exist")