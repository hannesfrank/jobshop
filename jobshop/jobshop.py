import fileinput
import random
import time

"""
Job Shop Scheduling
===================

Let j be the number of jobs and m be the number of machines/tasks.
A solution is a sequence of instructions to construct a schedule.
An instruction i \in [0..j-1] means to schedule the next task
for job i as early as possible (after the previous task of the
job and the previous task on the required machine is completed).
Thus a schedule is a permutation of 0^m 1^m ... (j-1)^m.

Example
-------

Let the following be an instance with j = 3 jobs (rows)
and m = 3 machines. For example, the pair "0 4" means that the
first task of the first job (job 0) has to be executed
on machine 0 and takes 4 timesteps:

3 3
0 4  1 3  2 5
2 4  1 3  0 4
0 6  2 3  1 3

The schedules
 - 220011012
 - 202101021
 - ...
would all result in the schedule

[ 2  ][0 ]      [1 ]
          [0][1][2]
      [2][1 ][ 0 ]

The schedule 002111220 (and others) result in the optimal

[0 ][ 2  ][1 ]
    [0][1]   [2]
[1 ]      [2][ 0 ]

The advantage of this representation is, that all
permutations result in a valid schedule.
This simplifies the computation of a neighborhood but
many permutations correspont to the same schedule
and the solution space could be (?) not as smooth.

Other possible representations:
  - order of tasks for each machine
      - advantage: more meaningful neighborhood
      - disadvantage: not every schedule is valid
  - directed graph and use (multi color) flow algorithms


Partial schedules
-----------------

For the recombination step of genetic algorithms it may
be practical to relax some of the properties of schedules.

A *partial schedule* is just a sequence of jobs.
It may contain a job more or less often as needed and
thus be longer or shorter than a valid schedule
of length m*j.

When evaluating the makespan of a schedule with
a cost function or computing the timetable we extend
a partial schedule *deterministically* by
 1. ignoring instructions for already finished jobs
 2. completing unfinished jobs after all instructions
    are processed

It is important that this is done deterministically
(and therefore in a smart way) because if we have found
a best partial schedule we want to recompute the
corresponding timetable when the search terminated.

One strategy to finish jobs is to queue the job with
the most missing tasks first (using a priorityQueue).
The problem here is that if one job has far more
unfinished task than the second job, it will fill up
many machines.
Maybe we could iterate through the k most unfinished
jobs, scheduling one task of each at a time.
The best solution would be to run a separate optimization
algorithm to complete a schedule. This can of cause
not be done in the cost function which must be as
fast as possible.
"""

# TODO IMPORTANT: find a problem instance which is larger than
#                 the vorlesungsbeispiel, but small enough to be examined manually
# TODO write a (one step) local search to explore
#       the immediate neighborhood of a schedule:
#       find better/best neighbor by swappint two instructions (O(n^2)...)
#       maybe there is a way to discover good/incluencial swaps, e.g. by (partially)
#       creating the real machine schedule and swap two jobs on the same machine
# TODO write a class which provides a framework for search algorithms
#       (see similarities of randomSearch and geneticSearch)
# TODO consider other representations
# TODO use numpy arrays for faster performance
# TODO reuse arrays in frequently called functions (e.g. in cost function)
# TODO if the algorithm works: implement in C++
# TODO evaluate recombination and mutation strategies
#       (by using a learning algorithm to find the best parameters)
# TODO evaluate normalization strategies for partial schedules
# TODO can we make localSearch = geneticSearchTemplate(
#           populationSize=1,
#           select=identity,   # do not throw away individuals
#           recombine=None,    # do not need this since we do not select
#           mutate=findBestNeighbor   # return best neighbor or random if local optimum is reached
#      )

def readJobs(path=None):
    """
    Returns a problem instance specified in a textfile at path
    or from stdin when no path is given.
    """
    with fileinput.input(files=path) as f:
        next(f)
        jobs = [[(int(machine), int(time)) for machine, time in zip(*[iter(line.split())]*2)]
                    for line in f if line.strip()]
    return jobs


def printJobs(jobs):
    """Print a problem instance."""
    print(len(jobs), len(jobs[0]))
    for job in jobs:
        for machine, time in job:
            print(machine, time, end=" ")
        print()


def cost(jobs, schedule):
    """Calculate the makespan of a schedule for a problem instance jobs."""
    j = len(jobs)
    m = len(jobs[0])

    tj = [0]*j   # end of previous task for each job
    tm = [0]*m   # end of previous task on each machine

    ij = [0]*j   # task to schedule next for each job

    for i in schedule:
        machine, time = jobs[i][ij[i]]
        ij[i] += 1

        # TODO The estimation of the start time is very rough.
        # A better (?) but slower approach would be to look just for the end
        # of the previous task of the job and search a free slot in the
        # timetable for the machine.
        start = max(tj[i], tm[machine])
        end = start + time
        tj[i] = end
        tm[machine] = end

    return max(tm)


def costPartial(jobs, partialSchedule):
    """
    Calculate the makespan of a partial schedule.
    """
    # (1) Ignore instructions for already finished jobs.
    # (2) Deterministically complete unfinished jobs after

    # TODO this can be done more efficiently
    return cost(jobs, normalizeSchedule(partialSchedule))



def normalizeSchedule(jobs, partialSchedule):
    """
    Extend a partial schedule to a valid schedule.
    """
    # Process Schedule as in cost function with.

    # TODO when implementing in C think about a clever algorithm
    # because ignoring instructions means, that the schedule is
    # longer than j*m, so static arrays are problematic.
    # Maybe use 2 arrays and read one and write to the other.

    j = len(jobs)
    m = len(jobs[0])

    occurences = [0] * j
    normalizedSchedule = []

    for t in partialSchedule:
        if occurences[t] < m:
            normalizedSchedule.append(t)
            occurences[t] += 1
        else:
            # ignore job for now
            pass

    # TODO finish schedule greedy for better performance
    # this has to be done in the same way as in costPartial
    for t, count in enumerate(occurences):
        if count < m:
            normalizedSchedule.extend([t] * (m - count))

    return normalizedSchedule

class OutOfTime(Exception):
    pass


def randomSchedule(j, m):
    """
    Returns a random schedule for j jobs and m machines,
    i.e. a permutation of 0^m 1^m ... (j-1)^m = (012...(j-1))^m.
    """
    schedule = [i for i in list(range(j)) for _ in range(m)]
    random.shuffle(schedule)
    return schedule


def printSchedule(jobs, schedule):
    # TODO code duplication with cost()
    j = len(jobs)
    m = len(jobs[0])

    tj = [0]*j   # end of previous task for job
    tm = [0]*m   # end of previous task on machine

    ij = [0]*j   # task to schedule next for each job

    for i in schedule:
        machine, time = jobs[i][ij[i]]
        ij[i] += 1
        start = max(tj[i], tm[machine])
        end = start + time
        tj[i] = end
        tm[machine] = end

        print("Start job {} on machine {} at {} ending {}.".format(i, machine, start, end))

    print("Total time:", max(tm))

def prettyPrintSchedule(jobs, schedule):
    # TODO code duplication with cost
    # TODO Generate an image where each job has a different color
    #      and a timestep is a pixel. This way even schedules with
    #      time ~1000 have a useful representation.
    def format_job(time, jobnr):
        if time == 1:
            return '#'
        if time == 2:
            return '[]'

        js = str(jobnr)

        # TODO number should be repeated for long times
        # but these may not be nice to print anyways...
        # if 2 + len(js) <= time and time < 10:
        if 2 + len(js) <= time:
            return ('[{:^' + str(time - 2) + '}]').format(jobnr)

        return '#' * time

    j = len(jobs)
    m = len(jobs[0])

    tj = [0]*j   # end of previous task for job
    tm = [0]*m   # end of previous task on machine

    ij = [0]*j   # task to schedule next for each job

    output = [""]*m

    for i in schedule:
        machine, time = jobs[i][ij[i]]
        ij[i] += 1
        start = max(tj[i], tm[machine])
        space = start - tm[machine]
        end = start + time
        tj[i] = end
        tm[machine] = end

        output[machine] += ' ' * space + format_job(time, i)

    [print(machine_schedule) for machine_schedule in output]

    print("Total Time: ", max(tm))


def lowerBound(jobs):
    """Returns a lower bound for the problem instance jobs."""
    def lower0():
        # max min time of jobs
        # each job has to be executed sequentially
        return max(sum(time for _, time in job) for job in jobs)
    def lower1():
        # max min time of machines
        # a machine must process all its tasks
        mtimes = [0]*numMachines(jobs)

        for job in jobs:
            for machine, time in job:
                mtimes[machine] += time

        return max(mtimes)

    return max(lower0(), lower1())


def numMachines(jobs):
    return len(jobs[0])


def numJobs(jobs):
    return len(jobs)


def shuffle(x, start=0, stop=None):
    """Shuffle part of x without copy. See also random.shuffle()."""
    # TODO see also numpy.random.shuffle which does not copy data
    if stop is None or stop > len(x):
        stop = len(x)

    for i in reversed(range(start + 1, stop)):
        # pick an element in x[start: i+1] with which to exchange x[i]
        j = random.randint(start, i)
        x[i], x[j] = x[j], x[i]

