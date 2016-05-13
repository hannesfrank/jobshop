from .jobshop import *

import random
import time


def randomSearch(jobs, maxTime=None):
    """
    Perform random search for problem instance jobs.
    Set maxTime to limit the computation time or raise
    a KeyboardInterrupt (Ctrl+C) to stop.
    """

    numExperiments = 100    # experiments performed per loop
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
                random.shuffle(rs)
                c = cost(jobs, rs)

                if c < best:
                    best = c
                    solutions.append((c, rs))

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

