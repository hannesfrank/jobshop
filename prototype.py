from jobshop import * 

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
    
    cost, solution = randomSearch(jobs, maxTime=20)
    # cost, solution = geneticSearchTemplate(jobs, mutate_permuteSubsequence, recombine_dummy, maxTime=20)

    # printSchedule(jobs, solution)
    # prettyPrintSchedule(jobs, solution)
    
    # a solution for vorlesungsbeispiel
    # prettyPrintSchedule(jobs, [0, 0, 1, 2, 1, 1, 2, 2, 0])