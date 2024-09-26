from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from problema import DIAS_SEMANA
from problema import VEGETALES
from problema import FRUTAS
from problema import NUECES
from problema import CANT_ATRIBUTOS
from problema import CANT_DIAS
from problema import funcion_puntaje
from problema import crear_ind
from problema import imprimir_ind
import numpy

import matplotlib.pyplot as plt
import seaborn as sns

#Busca el menor peso
creator.create("FitnessMax", base.Fitness, weights = (1.0,))

#Crea individuo
creator.create("Individual", list, fitness=creator.FitnessMax, strategy = None)

creator.create("Strategy", list, typecode="d")

#Registra
toolbox = base.Toolbox()

IND_SIZE = CANT_ATRIBUTOS * CANT_DIAS
#Función creadora de individuo
toolbox.register("individual", crear_ind, creator.Individual, creator.Strategy)
#Función creadora de poblacion
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
#Función evaluadora de pesos
toolbox.register("evaluate", funcion_puntaje)
#Método de selección
toolbox.register("select", tools.selTournament, tournsize = 4)
#Método de cruzamiento
toolbox.register("mate", tools.cxOnePoint)
#Método de mutación
toolbox.register("mutate",  tools.mutUniformInt, low = 1, up = 4, indpb=0.1)


#Población inicial
initialPopulation = 100
pop = toolbox.population(n=initialPopulation)

hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)

stats.register("avg", numpy.mean, axis=0)
stats.register("std", numpy.std, axis=0)
stats.register("min", numpy.min, axis=0)
stats.register("max", numpy.max, axis=0)



#Criterio de paro
stop = 10
pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, mu=initialPopulation, lambda_=initialPopulation, cxpb=0.7,   mutpb=0.3, ngen=stop, stats=stats, halloffame=hof)

best_solution = tools.selBest(pop, 1)[0]
print("\nBEST SOLUTION:")
print("")
print(best_solution)

imprimir_ind(best_solution)


# History AVG
plt.figure(figsize=(10,8))
front = numpy.array([(c['gen'], c['avg'][0]) for c in logbook])
plt.plot(front[:,0][1:-1], front[:,1][1:-1], "-bo", c="b")
plt.axis("tight")
plt.show()