from jobshop import *
from jobshop import geneticSearch

from functools import partial
import optparse
import random

# TODO: make command line program

if __name__ == '__main__':

    parser = optparse.OptionParser()

    parser.add_option('-a', '--algorithm',
        action="store", dest="algorithm",
        help="Choose Algorith: SA (Simulated Annealing), GS (GeneticSearch)", default="GS")

    parser.add_option('-s', '--select',
        action="store", dest="select",
        help="Choose Selectionmethod: best, stochastic, richard, tournament", default="best")

    parser.add_option('-r', '--recombine',
        action="store", dest="recombine",
        help="Choose Selectionmethod: first, crossover", default="crossover")

    parser.add_option('-m', '--mutate',
        action="store", dest="mutate",
        help="Choose Mutationmethod: permutate, swap", default="permutate")

    parser.add_option('-n', '--neighbourhood',
        action="store", dest="neighbourhood",
        help="Choose Mode for neighbourhood: random, normal", default="random")

    parser.add_option('-t', '--temp',
        action="store", dest="temperature",
        help="Choose Number for temperature", default=200)

    parser.add_option('-e', '--termination',
        action="store", dest="termination",
        help="Choose Number for termination", default=10)

    parser.add_option('-g', '--halting',
        action="store", dest="halting",
        help="Choose Number for halting", default=10)

    parser.add_option('-c', '--decrease',
        action="store", dest="decrease",
        help="Choose Number for decrease below 1", default=0.8)

    parser.add_option('-d', '--seed',
        action="store", dest="seed",
        help="Choose Number for Seed", default=1)

    options, args = parser.parse_args()

    abz5 = 'instances/abz5'
    vorlesungsbeispiel = 'instances/vorlesungsbeispiel'
    tai01 = 'instances/tai01'  # upper boulnd: 1231, lower bound 1005

    jobs = readJobs(tai01)

    m = len(jobs[0])
    j = len(jobs)

    print("Number of machines:", m)
    print("Number of jobs:", j)
    # printJobs(jobs)

    # rs = randomSchedule(j, m)
    # print(cost(jobs, rs))

    # cost, solution = randomSearch(jobs, maxTime=20)
    if str(options.seed).isdigit():
        random.seed(int(options.seed))
    else:
        print("No valid seed, default: 1")
        random.seed(1)

    if options.neighbourhood == "random":
        neighbourhood = "random"
    elif options.neighbourhood == "normal":
        neighbourhood = "normal"
    else:
        print("No valid neighbourhood chosen, default: random")
        neighbourhood = "random"

    if str(options.temperature).isdigit():
        temperature = int(options.temperature)
    else:
        temperature = 200   

    if str(options.termination).isdigit():
        termination = int(options.termination)
    else:
        termination = 10 

    if str(options.halting).isdigit():
        halting = int(options.halting)
    else:
        halting = 10 

    if options.decrease:
        decrease = options.decrease
    else:
        decrease = 0.8 

    if options.select == "best":
        select = geneticSearch.select_best
    elif options.select == "stochastic":
        select = geneticSearch.select_stochastic
    elif options.select == "richard":
        select = geneticSearch.select_richard
    elif options.select == "tournament":
        select = geneticSearch.select_tournament
    else:
        print("No valid selectionmethod chosen, default: best")
        select = geneticSearch.select_best

    if options.recombine == "first":
        recombine = geneticSearch.recombine_first
    elif options.recombine == "crossover":
        recombine = geneticSearch.recombine_simpleCrossover
    else:
        print("No valid recombine method chosen, default: crossover")
        recombine = geneticSearch.recombine_simpleCrossover

    if options.mutate == "swap":
        mutate = partial(geneticSearch.mutate_swap, num_swaps=10)
    elif options.mutate == "permutate":
        mutate = partial(geneticSearch.mutate_permuteSubsequence, max_shuffle_fraction=8)
    else:
        print("No valid mutation method chosen, default: permutate")

    if options.algorithm == "GS":
        cost, solution = geneticSearchTemplate(jobs, select=select, recombine=recombine, mutate=mutate, maxTime=20)
    elif options.algorithm == "SA":
        cost, solution = simulatedAnnealingSearch(jobs, maxTime=20, T=int(temperature), termination=int(termination), halting=int(halting), mode=neighbourhood, decrease=float(decrease))
    else:
        print("No valid algorithm chosen, default: GS")
        cost, solution = geneticSearchTemplate(jobs, select=select, recombine=recombine, mutate=mutate, maxTime=20)



    # printSchedule(jobs, solution)
    # prettyPrintSchedule(jobs, solution)

    # a solution for vorlesungsbeispiel
    # prettyPrintSchedule(jobs, [0, 0, 1, 2, 1, 1, 2, 2, 0])
