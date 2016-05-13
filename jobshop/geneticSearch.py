from .jobshop import *

import random
import time

# TODO do we need to parameterize select?
def geneticSearchTemplate(jobs, mutate, recombine, populationSize=20, maxTime=None):
    """
    Genetic algorithm for the jobshop scheduling problem.
    """

    numGenerations = 100   # generations calculated between logging
    solutions = []   # list of (time, schedule) with decreasing time
    best = 10000000  # TODO set initial value for max of add check in loop

    t0 = time.time()
    totalGenerations = 0

    j = len(jobs)
    m = len(jobs[0])
    l = j*m

    # initial generation
    schedules = [randomSchedule(j, m) for i in range(populationSize)]
    fitness = [cost(jobs, s) for s in schedules]

    # TODO rethink datastructure for population
    #   - using (cost, permutation) let us easily sort by cost
    #   - but cost changes in every step and we jsut need to recalculate at the end
    population = list(zip(fitness, schedules))

    while True:
        try:
            start = time.time()

            for g in range(numGenerations):
                # (1) selection
                population.sort()
                # get an even number of individuals
                # fittest = population[:(populationSize//4) * 2]
                # select best half
                fittest = population[:populationSize // 2]

                # (2) recombination
                next_generation = []
                while len(fittest) + len(next_generation) < populationSize:
                    next_generation.append(
                        recombine(random.choice(fittest)[1], random.choice(fittest)[1]))

                # dummy value for cost
                population = fittest + [(0, s) for s in next_generation]  

                # old idea
                # random.shuffle(fittest)
                # for (_, i1), (_, i2) in zip(*[iter(goodPopulation)]*2):
                #     # TODO randomize which parts are taken from which individual
                #     pass           

                # (3) mutation
                for _, individual in population:
                    mutate(individual)

                # reevaluate population
                population = [(cost(jobs, i), i) for _, i in population]

                best_individuum = min(population)

                if best_individuum[0] < best:
                    best = best_individuum[0]
                    solutions.append(best_individuum)

                totalGenerations += 1

            # print("Generation", totalGenerations)

            if maxTime and time.time() - t0 >= maxTime:
                raise OutOfTime("Time is over")

            t = time.time() - start
            if t > 0:
                print("Best:", best, "({:.1f} Generations/s, {:.1f} s)".format(
                        numGenerations/t, time.time() - t0))

            # Make outputs appear about every 3 seconds.
            if t > 4:
                numGenerations //= 2
            elif t < 1.5:
                numGenerations *= 2
        
        except (KeyboardInterrupt, OutOfTime) as e:
            print()
            print("================================================")
            print("Best time:", best, "  (lower bound {})".format(lowerBound(jobs)))
            print("Best solution:")
            print(solutions[-1][1])
            print("Found in {:} generations in {:.1f}s".format(totalGenerations, time.time() - t0))

            return solutions[-1]


def recombine_dummy(s1, s2):
    return s1


def mutate_dummy(s):
    pass


def mutate_permuteSubsequence(s, max_shuffle_fraction=4):
    """Mutate by random.shuffling a subsequence of a schedule."""
    a, b = sorted([random.randint(0, len(s) - 1), random.randint(0, len(s) - 1)])

    # The mutation should not be too large.
    # TODO maybe just:
    # b = random.randint(a, j*m//constant)
    # TODO think about probabilities...
    b = min(b, a + len(s) // max_shuffle_fraction)

    shuffle(s, a, b)


def mutate_swap(s):
    """Mutate by swapping two instructions."""
    a, b = random.randint(0, l - 1)
