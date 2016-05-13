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
would all result in the scedule

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
    """Calculate the cost of a schedule for a problem instance jobs."""
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


if __name__ == '__main__':
    abz5 = 'instances/abz5' 
    vorlesungsbeispiel = 'instances/vorlesungsbeispiel'
    tai01 = 'instances/tai01'  # upper boulnd: 1231, lower bound 1005

    jobs = readJobs(abz5)

    m = len(jobs[0])
    j = len(jobs)

    print("Number of machines:", m)
    print("Number of jobs:", j)
    # printJobs(jobs)
    
    # rs = randomSchedule(j, m)
    # print(cost(jobs, rs))
    
    cost, solution = randomSearch(jobs, 3)
    # cost, solution = evoSearch(jobs, maxTime=4)

    # printSchedule(jobs, solution)
    # prettyPrintSchedule(jobs, solution)
    
    # a solution for vorlesungsbeispiel
    # prettyPrintSchedule(jobs, [0, 0, 1, 2, 1, 1, 2, 2, 0])

