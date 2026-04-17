#function definitions

import random
import numpy as np

from constants import TEACHERS, CLASSROOMS, ROOM_CAPACITY, TIMES, SECTIONS, EXPECTED_STUDENTS, PREFERRED_CLASSES, SLIGHT_PREFERRED_CLASSES
from models import Schedule

TIME_INDEX = {t: i for i, t in enumerate(TIMES)}

#This randomly takes options and puts them in the sections of the schedules.
def random_schedule(seed=None):
    rng = np.random.Generator(np.random.PCG64DXSM(seed))
    assignments = {}
    for section in SECTIONS:
        teacher = rng.choice(TEACHERS)
        room = rng.choice(CLASSROOMS)
        time = rng.choice(TIMES)
        assignments[section] = (teacher, room, time)
    return Schedule(assignments)

def evolve(population, keep=0.5, generations=50, seed=None):
    rng = np.random.Generator(np.random.PCG64DXSM(seed))

    metrics = [] #store performance
    prev_avg = None

    for gen in range(generations):

        # --- Evaluate all schedules ---
        for schedule in population:
            compute_fitness(schedule)

        # --- Sort by fitness (descending) ---
        population.sort(key=lambda s: s.fitness, reverse=True)

        # --- Compute metrics ---
        best = population[0].fitness
        worst = population[-1].fitness
        avg = sum(s.fitness for s in population) / len(population)

        if prev_avg is None:
            improvement = 0.0
        else:
            improvement = ((avg - prev_avg) / abs(prev_avg)) * 100 if prev_avg != 0 else 0.0

        metrics.append({
            "generation": gen,
            "best": best,
            "avg": avg,
            "worst": worst,
            "improvement_percent": improvement
        })
        prev_avg = avg

        #Elitism keeps the top % of schedules
        elite_count = max(1, int(len(population) * keep))
        new_population = population[:elite_count]

        #Fill the rest of the population
        while len(new_population) < len(population):

            parent_a = rng.choice(population)
            parent_b = rng.choice(population)

            child = crossover(parent_a, parent_b, seed=rng.integers(1e9))

            if rng.random() < 0.10:
                mutate(child, seed=rng.integers(1e9))

            compute_fitness(child)
            new_population.append(child)

        population = new_population

    return population, metrics

def compute_fitness(schedule):
    score = 0
    score += score_room_conflicts(schedule)
    score += score_room_size(schedule)
    score += score_facilitator_preference(schedule)
    score += score_facilitator_load(schedule)
    score += score_sla_spacing(schedule)
    schedule.fitness = score
    return score

#Slightly alter the assignments of a schedule
def mutate(schedule, MUTATION_RATE=0.1, seed=None):
    rng = np.random.Generator(np.random.PCG64DXSM(seed))

    # Pick a random section to mutate
    section = rng.choice(SECTIONS)

    teacher, room, time = schedule.assignments[section]

    # Mutate teacher
    if rng.random() < MUTATION_RATE:
        teacher = rng.choice(TEACHERS)

    # Mutate room
    if rng.random() < MUTATION_RATE:
        room = rng.choice(CLASSROOMS)

    # Mutate time
    if rng.random() < MUTATION_RATE:
        time = rng.choice(TIMES)

    # Save new assignment
    schedule.assignments[section] = (teacher, room, time)

    # Will need a new fitness
    schedule.fitness = None

    return schedule

#breed two parent schedules together
def crossover(parent_a, parent_b, seed=None):
    rng = np.random.Generator(np.random.PCG64DXSM(seed))

    child_assignments = {}

    for section in SECTIONS:
        if rng.random() < 0.5:
            child_assignments[section] = parent_a.assignments[section]
        else:
            child_assignments[section] = parent_b.assignments[section]

    return Schedule(child_assignments)

#Output a specific schedule's information
def print_schedule(schedule):
    print("=== Schedule ===")

    for section, (teacher, room, time) in schedule.assignments.items():
        print(f"{section}:  Teacher={teacher},  Room={room},  Time={time}")

    if schedule.fitness is not None:
        print(f"\nFitness: {schedule.fitness}")

    print("================\n")

def print_metrics(metrics):
    # Header
    print(f"{'Gen':<5} {'Best':<10} {'Avg':<10} {'Worst':<10} {'Improve %':<10}")
    print("-" * 50)

    for m in metrics:
        print(
            f"{m['generation']:<5}"
            f"{m['best']:<10.2f}"
            f"{m['avg']:<10.2f}"
            f"{m['worst']:<10.2f}"
            f"{m['improvement_percent']:<10.2f}"
        )

def score_room_conflicts(schedule):
    buckets = {}  # (room, time) → list of sections

    for section, (teacher, room, time) in schedule.assignments.items():
        key = (room, time)
        buckets.setdefault(key, []).append(section)

    conflicts = 0
    for key, sections in buckets.items():
        if len(sections) > 1:
            conflicts += (len(sections) - 1)

    return -0.5 * conflicts

def score_room_size(schedule):
    score = 0

    for section, (teacher, room, time) in schedule.assignments.items():
        expected = EXPECTED_STUDENTS[section]
        capacity = ROOM_CAPACITY[room]

        if capacity < expected:
            score -= 0.5
        elif capacity > 3 * expected:
            score -= 0.4
        elif capacity > 1.5 * expected:
            score -= 0.2
        else:
            score += 0.3

    return score

def score_facilitator_preference(schedule):
    score = 0

    for section, (teacher, room, time) in schedule.assignments.items():
        if teacher in PREFERRED_CLASSES.get(section, {}):
            score += 0.5
        elif teacher in SLIGHT_PREFERRED_CLASSES.get(section, {}):
            score += 0.2
        else:
            score -= 0.1

    return score

def score_facilitator_load(schedule):
    score = 0

    # Count per facilitator
    total_load = {t: 0 for t in TEACHERS}
    slot_load = {t: {} for t in TEACHERS}

    for section, (teacher, room, time) in schedule.assignments.items():
        total_load[teacher] += 1
        slot_load[teacher].setdefault(time, 0)
        slot_load[teacher][time] += 1

    # Slot load scoring
    for teacher in TEACHERS:
        for time, count in slot_load[teacher].items():
            if count == 1:
                score += 0.2
            elif count > 1:
                score -= 0.2

    # Total load scoring
    for teacher, count in total_load.items():
        if count > 4:
            score -= 0.5
        elif count < 3:
            if teacher == "Tyler":
                if count < 2:
                    pass  # no penalty
                else:
                    score -= 0.4
            else:
                score -= 0.4

    return score

def score_sla_spacing(schedule):
    score = 0

    # Extract times
    def t(section):
        _, _, time = schedule.assignments[section]
        return TIME_INDEX[time]

    # Helper: check Roman/Beach
    def is_rb(room):
        return room.startswith("Roman") or room.startswith("Beach")

    # SLA101 spacing
    t101a = t("SLA101A")
    t101b = t("SLA101B")
    diff101 = abs(t101a - t101b)

    if diff101 >= 4:
        score += 0.5
    if diff101 == 0:
        score -= 0.5

    # SLA191 spacing
    t191a = t("SLA191A")
    t191b = t("SLA191B")
    diff191 = abs(t191a - t191b)

    if diff191 >= 4:
        score += 0.5
    if diff191 == 0:
        score -= 0.5

    # SLA101 vs SLA191 cross‑rules
    pairs_101 = ["SLA101A", "SLA101B"]
    pairs_191 = ["SLA191A", "SLA191B"]

    for s101 in pairs_101:
        for s191 in pairs_191:
            t1 = t(s101)
            t2 = t(s191)
            diff = abs(t1 - t2)

            room101 = schedule.assignments[s101][1]
            room191 = schedule.assignments[s191][1]

            if diff == 1:  # consecutive
                score += 0.5
                if is_rb(room101) != is_rb(room191):
                    score -= 0.4

            elif diff == 2:  # 1 hour apart
                score += 0.25

            elif diff == 0:  # same slot
                score -= 0.25

    return score
