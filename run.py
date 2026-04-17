import random
import numpy as np

import constants
from functions import random_schedule, evolve, compute_fitness, mutate, crossover, print_schedule, print_metrics
import models

#Variables needed for GA
MUTATION_RATE = 0.02
GENERATIONS = 50
PERCENT_KEPT = 0.1

#Create the initial populations
POP_SIZE = 20
population = [random_schedule(seed=i) for i in range(POP_SIZE)]

#Run the algorithm
population, metrics = evolve(population,keep=PERCENT_KEPT,generations=GENERATIONS,seed=0)

#just print some results to the console
print_metrics(metrics)