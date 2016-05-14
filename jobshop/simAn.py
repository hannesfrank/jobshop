from .jobshop import *
import copy, random, math

def getNeigbours(state, mode="normal"):
    allNeighbours = []
    for i in range(len(state)-1):
        tempState = copy.copy(state)
        if mode == "normal":
            tempState[i] = tempState[i+1]
            tempState[i+1]= state[i]
        elif mode == "random":
            ranNum = random.randint(0, len(tempState)-1)
            tempState[i] = tempState[ranNum]
            tempState[ranNum]= state[i]
        allNeighbours.append(tempState)

    return allNeighbours

def simulatedAnnealing(jobs, numberOfJobs, numberofMachines, T=200, termination=10, halting=10, mode = "random"):
    #start with random solution
    state = []
    for i in range(numberOfJobs):
        for j in range(numberofMachines):
            state.append(i)
    random.shuffle(state)

    i = 0
    while i < halting:
        k = 0
        T = 0.8 * T
        while k < termination:
            actualCost = cost(jobs, state)
            myNeighbours = getNeigbours(state, mode)
            for n in myNeighbours:
                nCost = cost(jobs, n)
                if nCost < actualCost:
                    state = n
                    actualCost = nCost
                    continue
                else:
                    probability = math.exp(-nCost/T)
                    ranVal = random.randint(0,100)
                    if ranVal < probability*100:
                        state = n
                        actualCost = nCost
                        continue
            k += 1
        i += 1

    return state, actualCost