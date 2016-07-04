from jobshop import *
from jobshop import geneticSearch

from functools import partial

# TODO: make command line program

if __name__ == '__main__':
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
    # cost, solution = simulatedAnnealingSearch(jobs, maxTime=20)

    select = geneticSearch.select_best
    recombine = geneticSearch.recombine_simpleCrossover
    # mutate = partial(geneticSearch.mutate_swap, num_swaps=10)
    mutate = partial(geneticSearch.mutate_permuteSubsequence, max_shuffle_fraction=8)

    cost, solution = geneticSearchTemplate(jobs, select=select, recombine=recombine, mutate=mutate, maxTime=20)


    # printSchedule(jobs, solution)
    # prettyPrintSchedule(jobs, solution)

    # a solution for vorlesungsbeispiel
    # prettyPrintSchedule(jobs, [0, 0, 1, 2, 1, 1, 2, 2, 0])
