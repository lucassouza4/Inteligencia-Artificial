import copy
import math
import numpy as np
import random


def ColumnViolations(sol):

    conflicts = 0

    for i in range(len(sol)):
        for j in range(len(sol)):
            if (i != j) and (sol[i] == sol[j]):
                conflicts += 1

    return conflicts


def DiagonalViolations(sol):

    conflicts = 0
    for i in range(len(sol)):
        for j in range(len(sol)):
            y = abs(sol[i]-sol[j])
            x = abs(i - j)
            if (y == x and i != j):
                conflicts += 1

    return conflicts


def eval(sol):

    return DiagonalViolations(sol) + ColumnViolations(sol)


def generatePopulation(var, domains, popSize):

    pop = []
    size = len(domains)

    for _ in range(popSize):
        if (size > 1):
            pop.append([random.choice(domains[j]) for j in range(len(var))])
        else:
            pop.append([random.choice(domains[0]) for _ in range(len(var))])

    return pop


def checkConstraints(individual, constraints):

    for constraint in constraints:
        if (constraint(individual)):
            return False

    return True


def select(population, iteration, eval):

    while True:

        for individual in population:
            randomNumber = abs(random.random())

            if (randomNumber < math.exp(-1 * eval(individual) / iteration)):
                return individual


def crossover(fstividual, sndividual):

    popSize = len(fstividual)
    mask = np.random.randint(2, size=popSize)  

    child1 = copy.deepcopy(fstividual)
    child2 = copy.deepcopy(sndividual)

    for i in range(popSize):
        if not mask[i]:
            child1[i] = sndividual[i]
            child2[i] = fstividual[i]

    return child1, child2


def mutate(individual, percentage):

    percentage = percentage / 100 if (percentage > 0) else percentage
    neighbor = copy.deepcopy(individual)

    for _ in range(math.ceil(percentage)):
        idx1 = np.random.randint(0, len(individual))
        idx2 = np.random.randint(0, len(individual))
        neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]

    return neighbor


def BestSolution(population, constraints):

    bestSol = copy.deepcopy(population[0])
    bestVal = eval(bestSol)

    for i in population:
        val = eval(i)

        if (val < bestVal and checkConstraints(i, constraints)):
            bestVal = val
            bestSol = i

    return bestSol, bestVal


def GS(var, domains, constraints, iterMax, popSize, eval):
    population = generatePopulation(var, domains, popSize)

    for i in range(1, iterMax+1):

        for individual in population:
            if (checkConstraints(individual, constraints)):
                return BestSolution(population, constraints)

        newPopulation = []
        for _ in range(math.floor(popSize / 2)):

            fst = select(population, i, eval)
            snd = select(population, i, eval)

            newFst, newSnd = crossover(fst, snd)
            newPopulation.append(mutate(newFst, 40))
            newPopulation.append(mutate(newSnd, 40))

        population = newPopulation

    return BestSolution(population, constraints)


if __name__ == "__main__":
    n = 4
    var = [i for i in range(n)]
    domain = [[i for i in range(n)] for j in range(n)]
    constraints = [ColumnViolations, DiagonalViolations]
    sol, val = GS(var, domain, constraints, 10000, 1000, eval)
    print(sol)
    print(val)