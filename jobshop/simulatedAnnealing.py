from .jobshop import *
import random, math

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

def simulatedAnnealing(jobs, numberOfJobs, numberofMachines, T=200, termination=10, halting=10, mode="random"):
    # start with random solution
    state = randomSchedule(numberOfJobs, numberofMachines)

    for i in range(halting):
        T = 0.8 * T

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
