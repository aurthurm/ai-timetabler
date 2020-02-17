from django.shortcuts import render
from django.conf import settings

from .utils_simple import Population as SimplePopulation
from .utils_simple import GeneticAlgo as SimpleGeneticAlgo
from .utils_simple import print_population as simple_print_population
from .utils_simple import print_fittest_schedule as simple_print_fittest_schedule
from .utils_simple import save_simple_population

from .utils_complex import Population as ComplexPopulation
from .utils_complex import GeneticAlgo as ComplexGeneticAlgo
from .utils_complex import DisplayManager as ComplexDisplayManager

from .models import GAType, SimpleSchedule, ComplexSchedule, SimpleDay, SimpleTime


days = SimpleDay.objects.all().order_by('id')
timeslots = SimpleTime.objects.all().order_by('id')


def home(request):
    ga = GAType.objects.first()
    context = {
        "algorithm": ga,
    }
    if ga.simple_ga:
        context["title"] = "Single Department of a faculty and or possible Single Lecture Room"
        schedules = SimpleSchedule.objects.all().order_by('-created')

        tables = []
        table_data = {}
        for k, v in enumerate(timeslots):
            table_data[v.name] = {
                'time': v.name,
                'monday': {'course': '', 'instructor': ''},
                'tuesday': {'course': '', 'instructor': ''},
                'wednesday': {'course': '', 'instructor': ''},
                'thursday': {'course': '', 'instructor': ''},
                'friday': {'course': '', 'instructor': ''},
            }
            table_data['created'] = ''
            
        for schedule in schedules:
            table_data['created'] = schedule.created
            for assignment in schedule.assignments.all():
                _course = assignment.course.name
                _instructor =  assignment.course.simpleinstructor_set.first().name
                data = { 'instructor': _instructor, 'course': _course }

                for time in assignment.times.all():
                    _time = time.time.name
                    _day = time.day.name

                    for k, v in table_data.items():
                        if k == _time:
                            if _day == "Monday":
                                v['monday'] = data
                            elif _day == "Tuesday":
                                v['tuesday'] = data
                            elif _day == "Wednesday":
                                v['wednesday'] = data
                            elif _day == "Thursday":
                                v['thursday'] = data
                            else:
                                v['friday'] = data
                
            tables.append(table_data.copy())
            #reset
            for k, v in enumerate(timeslots):
                table_data[v.name] = {
                    'time': v.name,
                    'monday': {'course': '', 'instructor': ''},
                    'tuesday': {'course': '', 'instructor': ''},
                    'wednesday': {'course': '', 'instructor': ''},
                    'thursday': {'course': '', 'instructor': ''},
                    'friday': {'course': '', 'instructor': ''},
                }
            table_data['created'] = ''

        # context["schedules"] = schedules
        context["tables"] = tables
        return render(request, 'simple.html', context=context)
    else:
        context["title"] = "Multiple Lecture Rooms, Shared Instructors, Different Departments"
        context["schedules"] = ComplexSchedule.objects.all().order_by('-created')
        return render(request, 'complex.html', context=context)

def generate_simple_schedule(print_detail=False):
    generationNumber = 0
    print(f"\n>> Generation {generationNumber}\n")
    population = SimplePopulation(settings.POPULATION_SIZE)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse = True)
    if print_detail:
        print("\nPopulation Fitness")
        simple_print_population(population.get_schedules())
        print("\nFittest Schedule")
        simple_print_fittest_schedule(population.get_schedules()[0])

    if population.get_schedules()[0].get_fitness() == 1.0:
        save_simple_population(population.get_schedules()[0])


    algo = SimpleGeneticAlgo()
    while population.get_schedules()[0].get_fitness() != 1.0:
        generationNumber += 1
        print(f"\n>> Generation: {generationNumber}")
        population = algo.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse = True)
        if print_detail:
            print("\nPopulation Fitness")
            simple_print_population(population.get_schedules())
            print("\nFittest Schedule")
            simple_print_fittest_schedule(population.get_schedules()[0])

        if population.get_schedules()[0].get_fitness() == 1.0:
            save_simple_population(population.get_schedules()[0])

    return population


def generate_complex_schedule():
    generationNumber = 0
    print(f"\n>> Generation: {generationNumber}")
    population = ComplexPopulation(settings.POPULATION_SIZE)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse = True)
    dsp = ComplexDisplayManager()
    print("\n__ Population\n")
    dsp.print_generation(population)
    print("\n__ Schedule\n")
    dsp.print_schedule_as_table(population.get_schedules()[0])
        
    if population.get_schedules()[0].get_fitness() == 1.0:
        dsp.save_schedule(population.get_schedules()[0])

    algo = ComplexGeneticAlgo()
    while population.get_schedules()[0].get_fitness() != 1.0:
        generationNumber += 1
        print(f"\n>> Generation: {generationNumber}")
        population = algo.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse = True)
        print("\n__ Population\n")
        dsp.print_generation(population)
        print("\n__ Schedule\n")
        dsp.print_schedule_as_table(population.get_schedules()[0])
        
        if population.get_schedules()[0].get_fitness() == 1.0:
            dsp.save_schedule(population.get_schedules()[0])

    return population