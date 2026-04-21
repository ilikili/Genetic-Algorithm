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


def plot_fitness_cli(metrics):
    import sys

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    try:
        import plotext as plt
    except ImportError:
        print("\nplotext is not installed. Install it with: pip install plotext")
        return

    generations = [m["generation"] for m in metrics]
    best = [m["best"] for m in metrics]
    avg = [m["avg"] for m in metrics]
    worst = [m["worst"] for m in metrics]

    plt.clear_data()
    plt.clear_figure()
    plt.theme("clear")
    plt.title("Fitness Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.plot(generations, best, label="Best", marker=".")
    plt.plot(generations, avg, label="Average", marker=".")
    plt.plot(generations, worst, label="Worst", marker=".")
    plt.plotsize(100, 30)
    plt.grid(True)
    plt.show()


plot_fitness_cli(metrics)