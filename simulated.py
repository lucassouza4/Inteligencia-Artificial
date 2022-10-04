import math
import random
import numpy as np
import copy


def acceptanceProbability(delta, T):
    return math.exp((-1*delta) / T)


def differentColumnViolations(sol):

    conflicts = 0

    for i in range(len(sol)):
        for j in range(len(sol)):
            if (i != j) and (sol[i] == sol[j]):
                conflicts += 1

    return conflicts


def differentDiagonalViolations(sol):

    conflicts = 0
    for i in range(len(sol)):
        for j in range(len(sol)):
            deltay = abs(sol[i]-sol[j])
            deltax = abs(i - j)
            if (deltay == deltax and i != j):
                conflicts += 1

    return conflicts


def evalSol(sol):

    return differentDiagonalViolations(sol) + differentColumnViolations(sol)


def swap(sol):

    neighbor = copy.copy(sol)

    idx1 = np.random.randint(0, len(sol))
    idx2 = np.random.randint(0, len(sol))

    neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]

    return neighbor


def simulatedAnnealing(sol, evalSol, move, itermax, T0, cooling, noImprovement=0):

    if noImprovement == 0:
        noImprovement = itermax * 0.5

    iterationsWithNoImprovements = 0
    bestVal = evalSol(sol)
    bestSol = copy.deepcopy(sol)
    currentVal = evalSol(sol)
    currentSol = copy.deepcopy(sol)
    T = T0

    for i in range(0, itermax):
        neighbor = move(copy.deepcopy(currentSol))
        newVal = evalSol(neighbor)
        iterationsWithNoImprovements += 1

        if (newVal - currentVal < 0):
            iterationsWithNoImprovements = 0
            currentSol = copy.deepcopy(neighbor)
            currentVal = newVal

            if (currentVal < bestVal):
                bestSol = copy.deepcopy(currentSol)
                bestVal = currentVal

        else:
            x = abs(random.random())
            if (x < acceptanceProbability(newVal - currentVal, T)):
                currentSol = copy.deepcopy(neighbor)
                currentVal = newVal

        T *= cooling

        if (iterationsWithNoImprovements > noImprovement):
            iterationsWithNoImprovements = 0
            T = T0

    return bestSol, bestVal


if __name__ == '__main__':

    sol = list(range(8))
    val = evalSol(sol)
    sol, val = simulatedAnnealing(sol=sol, evalSol=evalSol, move=swap, itermax=1000, T0=100, cooling=0.90)

    print(sol)
    print(val)