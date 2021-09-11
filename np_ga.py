import time
import numpy as np
from numba import njit

@njit()
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
    fitness = np.empty((population.shape[0], 2))

    i = 0
    for chromosome in population:
        penalties = 0
        steps = 0
        x = 1
        y = 1

        for move in chromosome:
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
        penalty = 2
        if xLocked and yLocked:
            penalty = 3
        elif x == goalX and yLocked:
            penalty = 4
        elif y == goalY and xLocked:
            penalty = 4

        # minimize this score! tuple(score, moves)
        fitness[i][0] = distance * penalty + penalties
        fitness[i][1] = steps
        i += 1
    
    return fitness

class GA():
    MOVE_LIMIT = 100
    POPULATION_SIZE = 100000
    MUTATION_CHANCE = 0.1 # 10% chance at mutation
    # we need a "no move" operation for the case when the chromosome is already optimal
    # for example, if the chromosome succeeded in the most optimal moves say 40, 
    # the remaining 100 - 40 moves should be no moves
    GENES = [0, 1, 2, 3, 4]
    MAX_GENERATIONS = 50

    def __init__(self):
        self.generation = 1

        t = time.monotonic()
        # create base population
        self.population = np.random.randint(self.GENES[0], self.GENES[-1] + 1, (self.POPULATION_SIZE, self.MOVE_LIMIT))
        self.getGenerationalBest(t)


        for i in range(1, self.MAX_GENERATIONS):
            t = time.monotonic()
            self.generation += 1

            self.crossover()
            self.getGenerationalBest(t)

    # crossover applies on a subset of the population that are fittest
    def crossover(self):
        newPopulation = np.empty((self.POPULATION_SIZE, self.MOVE_LIMIT))
        # sort population by fitness value then number of moves
        fitness = fitnessFunction(self.population)
        fitnessIndices = fitness.argsort(axis=0)
        self.population = self.population[fitnessIndices.T[0]]

        # consider 25% fittest population
        subset = self.population[:self.POPULATION_SIZE // 4]
        subsetSize = subset.shape[0]

        # calculate randoms
        rand_parents = np.random.randint(0, subsetSize, (self.POPULATION_SIZE, 2))
        rand_points = np.random.randint(0, self.MOVE_LIMIT, self.POPULATION_SIZE)
        rand_mutations = np.random.random(self.POPULATION_SIZE)
        rand_mutation_points = np.random.randint(0, self.MOVE_LIMIT, self.POPULATION_SIZE)
        rand_mutation_genes = np.random.randint(self.GENES[0], self.GENES[-1] + 1, self.POPULATION_SIZE)

        for i in range(self.POPULATION_SIZE):
            firstParent = subset[rand_parents[i][0]][:]
            secondParent = subset[rand_parents[i][1]][:]

            # select a random crossover point in the genespace
            crossoverPoint = rand_points[i]

            newPopulation[i] = np.append(firstParent[:crossoverPoint], secondParent[crossoverPoint:])

            # mutate
            if rand_mutations[i] < self.MUTATION_CHANCE:
                newPopulation[i][rand_mutation_points[i]] = rand_mutation_genes[i]
        
        self.population = newPopulation

    def getGenerationalBest(self, startTime):
        fitness = fitnessFunction(self.population)
        fitnessIndices = fitness.argsort()[:3]
        best = self.population[fitnessIndices]

        print('Generation {} Time taken - {}s'.format(self.generation, time.monotonic() - startTime))
        for i, item in enumerate(best):
            print(item, '(Score: {})'.format(fitness[fitnessIndices[i]][0]))

if __name__ == '__main__':
    GA()