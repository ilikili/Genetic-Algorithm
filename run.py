import random
import numpy as np

import constants
from functions import random_schedule, evolve, compute_fitness, mutate, crossover, print_schedule, print_metrics, format_schedule
import models

#Variables needed for GA
MUTATION_RATE = 0.02
GENERATIONS = 500
PERCENT_KEPT = 0.1

#Create the initial populations
POP_SIZE = 20
population = [random_schedule(seed=i) for i in range(POP_SIZE)]

#Run the algorithm
population, metrics = evolve(population,keep=PERCENT_KEPT,generations=GENERATIONS,seed=0)

#just print some results to the console
print_metrics(metrics)

# Best schedule in the final generation (population is not sorted after the last breeding step)
best_schedule = max(population, key=lambda s: compute_fitness(s))
final_gen = metrics[-1]["generation"] if metrics else GENERATIONS - 1
final_best_fitness = best_schedule.fitness
print(f"\nFinal generation ({final_gen}): best fitness = {final_best_fitness:.4f}")

OUTPUT_PATH = "best_schedule_output.txt"
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(f"Final generation: {final_gen}\n")
    f.write(f"Best fitness: {final_best_fitness}\n\n")
    f.write(format_schedule(best_schedule))
print(f"Best schedule written to {OUTPUT_PATH}")


def plot_fitness(metrics):
    """Matplotlib fitness chart"""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nmatplotlib is not installed. Install it with: pip install matplotlib")
        return

    generations = [m["generation"] for m in metrics]
    best = [m["best"] for m in metrics]
    avg = [m["avg"] for m in metrics]
    worst = [m["worst"] for m in metrics]

    plt.figure(figsize=(10, 6))
    plt.plot(generations, best, "b-", linewidth=2, label="Best")
    plt.plot(generations, avg, "g-", linewidth=2, label="Average")
    plt.plot(generations, worst, "r-", linewidth=2, label="Worst")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Fitness over Generations")
    plt.legend(loc="best")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


plot_fitness(metrics)
