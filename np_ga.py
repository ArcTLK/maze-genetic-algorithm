import time
import numpy as np
from numba import njit, prange

# constants
MOVE_LIMIT = 100
POPULATION_SIZE = 2000000
MUTATION_CHANCE = 0.01 # 1% chance at mutation
# we need a "no move" operation for the case when the chromosome is already optimal
# for example, if the chromosome succeeded in the most optimal moves say 40, 
# the remaining 100 - 40 moves should be no moves
GENE_MIN = 0
GENE_MAX = 4
MAX_GENERATIONS = 50

@njit(parallel=True)
def fitnessFunction(population):
    board = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 3, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    goalX = 14
    goalY = 10

    fitness = np.empty(POPULATION_SIZE)

    for j in prange(POPULATION_SIZE):
        penalties = 0
        steps = 0
        x = 1
        y = 1

        for move in population[j]:
            if move == 1:
                if board[y - 1][x] == 1:
                    penalties += 1
                else:
                    y -= 1
                    steps += 1
            elif move == 2:
                if board[y + 1][x] == 1:
                    penalties += 1
                else:
                    y += 1
                    steps += 1
            elif move == 3:
                if board[y][x - 1] == 1:
                    penalties += 1
                else:
                    x -= 1
                    steps += 1
            elif move == 4:
                if board[y][x + 1] == 1:
                    penalties += 1
                else:
                    x += 1
                    steps += 1

        # distance
        distance = abs(x - goalX) + abs(y - goalY)

        # compensate for unexplored areas
        xLocked = False
        yLocked = False

        if x < goalX:
            for i in range(x + 1, goalX + 1):
                if board[y][i] == 1:
                    xLocked = True
                    break
        
        elif x > goalX:
            for i in range(x - 1, goalX - 1, -1):
                if board[y][i] == 1:
                    xLocked = True
                    break

        if y < goalY:
            for i in range(y + 1, goalY + 1):
                if board[i][x] == 1:
                    yLocked = True
                    break
        
        elif y > goalY:
            for i in range(y - 1, goalY - 1, -1):
                if board[i][x] == 1:
                    yLocked = True
                    break

        # penalty
        extra_penalty = 2
        if xLocked and yLocked:
            extra_penalty = 3
        elif x == goalX and yLocked:
            extra_penalty = 4
        elif y == goalY and xLocked:
            extra_penalty = 4

        # minimize this score!
        fitness[j] = distance * extra_penalty + penalties
    
    return fitness

@njit(parallel=True)
def crossover(population):
    newPopulation = np.empty((POPULATION_SIZE, MOVE_LIMIT))

    # consider 25% fittest population
    subset = population[:POPULATION_SIZE // 4]
    subsetSize = subset.shape[0]

    # calculate randoms
    rand_parents = np.random.randint(0, subsetSize, (POPULATION_SIZE, 2))
    rand_points = np.random.randint(0, MOVE_LIMIT, POPULATION_SIZE)
    rand_mutations = np.random.random(POPULATION_SIZE)
    rand_mutation_points = np.random.randint(0, MOVE_LIMIT, POPULATION_SIZE)
    rand_mutation_genes = np.random.randint(GENE_MIN, GENE_MAX + 1, POPULATION_SIZE)

    for i in range(POPULATION_SIZE):
        firstParent = subset[rand_parents[i][0]][:]
        secondParent = subset[rand_parents[i][1]][:]

        # select a random crossover point in the genespace
        crossoverPoint = rand_points[i]

        newPopulation[i] = np.append(firstParent[:crossoverPoint], secondParent[crossoverPoint:])

        # mutate
        if rand_mutations[i] < MUTATION_CHANCE:
            newPopulation[i][rand_mutation_points[i]] = rand_mutation_genes[i]
    
    return newPopulation

@njit(parallel=True)
def getRandomPopulation():
    return np.random.randint(GENE_MIN, GENE_MAX + 1, (POPULATION_SIZE, MOVE_LIMIT))

@njit()
def sortUsingFitness(population):
    fitness = fitnessFunction(population)
    fitnessIndices = fitness.argsort()

    return (population[fitnessIndices], fitness, fitnessIndices)

def printGenerationalBest(generation, best, fitness, fitnessIndices, startTime):
    print('Generation {} Time taken - {}s'.format(generation, time.monotonic() - startTime))
    
    for i, item in enumerate(best):
        moves = ''
        for move in item.astype('int32'):
            if move == 0:
                moves += 'N'
            elif move == 1:
                moves += 'W'
            elif move == 2:
                moves += 'S'
            elif move == 3:
                moves += 'A'
            elif move == 4:
                moves += 'D'

        print(moves, '(Score: {})'.format(int(fitness[fitnessIndices[i]])))

if __name__ == '__main__':
    generation = 1

    t = time.monotonic()
    # create base population
    population = getRandomPopulation()

    population, fitness, fitnessIndices = sortUsingFitness(population)
    printGenerationalBest(generation, population[:3], fitness, fitnessIndices, t)


    for i in range(1, MAX_GENERATIONS):
        t = time.monotonic()
        generation += 1

        population = crossover(population)

        population, fitness, fitnessIndices = sortUsingFitness(population)
        printGenerationalBest(generation, population[:3], fitness, fitnessIndices, t)

