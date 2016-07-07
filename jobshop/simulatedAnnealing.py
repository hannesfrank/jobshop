from .jobshop import *

import math
import random
import time


def getNeigbors(state, mode="normal"):
    allNeighbors = []

    for i in range(len(state)-1):
        neighbor = state[:]
        if mode == "normal":
            swapIndex = i + 1
        elif mode == "random":
            swapIndex = random.randrange(len(state))
        neighbor[i], neighbor[swapIndex] = neighbor[swapIndex], neighbor[i]
        allNeighbors.append(neighbor)

    return allNeighbors

def simulatedAnnealing(jobs, T, termination, halting, mode, decrease):
    numberOfJobs = len(jobs)
    numberOfMachines = len(jobs[0])

    state = randomSchedule(numberOfJobs, numberOfMachines)

    for i in range(halting):
        T = decrease * float(T)

        for k in range(termination):
            actualCost = cost(jobs, state)

            for n in getNeigbors(state, mode):
                nCost = cost(jobs, n)
                if nCost < actualCost:
                    state = n
                    actualCost = nCost
                else:
                    probability = math.exp(-nCost/T)
                    if random.random() < probability:
                        state = n
                        actualCost = nCost

    return actualCost, state



def simulatedAnnealingSearch(jobs, maxTime=None, T=200, termination=10, halting=10, mode="random", decrease=0.8):
    """
    Perform random search for problem instance jobs.
    Set maxTime to limit the computation time or raise
    a KeyboardInterrupt (Ctrl+C) to stop.
    """

    numExperiments = 1      # experiments performed per loop
                            # used to balance logging output
    solutions = []   # list of (time, schedule) with decreasing time
    best = 10000000  # TODO set initial value for max or add check for None in loop

    t0 = time.time()
    totalExperiments = 0

    j = len(jobs)
    m = len(jobs[0])
    rs = randomSchedule(j, m)

    while True:
        try:
            start = time.time()

            for i in range(numExperiments):
                cost, schedule = simulatedAnnealing(jobs, T=T, termination=termination, halting=halting, mode=mode, decrease=decrease)

                if cost < best:
                    best = cost
                    solutions.append((cost, schedule))

            totalExperiments += numExperiments

            if maxTime and time.time() - t0 > maxTime:
                raise OutOfTime("Time is over")

            t = time.time() - start
            if t > 0:
                print("Best:", best, "({:.1f} Experiments/s, {:.1f} s)".format(
                        numExperiments/t, time.time() - t0))

            # Make outputs appear about every 3 seconds.
            if t > 4:
                numExperiments //= 2
                numExperiments = max(numExperiments, 1)
            elif t < 1.5:
                numExperiments *= 2

        except (KeyboardInterrupt, OutOfTime) as e:
            print()
            print("================================================")
            print("Best time:", best, "  (lower bound {})".format(lowerBound(jobs)))
            print("Best solution:")
            print(solutions[-1][1])
            print("Found in {:} experiments in {:.1f}s".format(totalExperiments, time.time() - t0))

            return solutions[-1]

