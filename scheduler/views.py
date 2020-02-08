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

from .models import GAType, SimpleSchedule, ComplexSchedule

def home(request):
    ga = GAType.objects.first()
    context = {
        "algorithm": ga,
    }
    if ga.simple_ga:
        context["title"] = "Single Department of a faculty and or possible Single Lecture Room"
        context["schedules"] = SimpleSchedule.objects.all().order_by('-created')
        return render(request, 'simple.html', context=context)
    else:
        context["title"] = "Multiple Lecture Rooms, Shared Instructors, Different Departments"
        context["schedules"] = ComplexSchedule.objects.all().order_by('-created')
        return render(request, 'complex.html', context=context)

def generate_simple_schedule():
    generationNumber = 0
    print(f"\n>> Generation {generationNumber}\n")
    population = SimplePopulation(settings.POPULATION_SIZE)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse = True)
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