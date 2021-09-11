import time
from random import randint, random
from copy import deepcopy
from maze import MazeGame
from utils import getManhattanDistance

class GA():
    MOVE_LIMIT = 100
    POPULATION_SIZE = 100000
    MUTATION_CHANCE = 0.1 # 10% chance at mutation
    # we need a "no move" operation for the case when the chromosome is already optimal
    # for example, if the chromosome succeeded in the most optimal moves say 40, 
    # the remaining 100 - 40 moves should be no moves
    GENES_NAMES = ['N', 'W', 'S', 'A', 'D'] # no move, up, down, left, right
    GENES = [0, 1, 2, 3, 4]
    MAX_GENERATIONS = 50

    def __init__(self):
        self.population = []
        self.generation = 1

    def run(self):
        t = time.monotonic()

        self.createBasePopulation()
        self.getGenerationalBest(t)

        for i in range(1, self.MAX_GENERATIONS):
            t = time.monotonic()
            self.generation += 1

            self.crossover()
            self.getGenerationalBest(t)

    def getGenerationalBest(self, startTime):
        best = deepcopy(sorted(
            self.population, key=lambda chromosome: self.fitnessFunction(chromosome)
        )[:3])

        for i in range(len(best)):
            for j in range(self.MOVE_LIMIT):
                best[i][j] = self.GENES_NAMES[best[i][j]]

        print('Generation {} Time taken - {}s'.format(self.generation, time.monotonic() - startTime))
        for item in best:
            score = self.fitnessFunction(item)
            print(''.join(item), '(Score: {})'.format(score[0]))

    
    def createBasePopulation(self):
        self.population = [
            [
                randint(self.GENES[0], self.GENES[-1]) for y in range(self.MOVE_LIMIT)
            ] for x in range(self.POPULATION_SIZE)
        ]

    def fitnessFunction(self, chromosome):
        game = MazeGame()

        # play the game
        for move in chromosome:
            if move == 1 or move == 'W':
                game.moveUp()
            elif move == 2 or move == 'S':
                game.moveDown()
            elif move == 3 or move == 'A':
                game.moveLeft()
            elif move == 4 or move == 'D':
                game.moveRight()

        # distance
        distance = getManhattanDistance(game.x, game.y, game.goalX, game.goalY)

        # add penalty if there is a wall between current position and goal
        extra_penalty = game.isWallBetweenPositionAndGoal()

        # minimize this score! tuple(score, moves)
        return (distance * extra_penalty + game.penalties, game.steps)

    # crossover applies on a subset of the population that are fittest
    def crossover(self):
        newPopulation = []

        # sort population by fitness value then number of moves
        self.population.sort(key=lambda chromosome: self.fitnessFunction(chromosome))

        # consider 25% fittest population
        subset = self.population[:self.POPULATION_SIZE // 4]
        subsetSize = len(subset)

        for i in range(self.POPULATION_SIZE):
            firstParent = subset[randint(0, subsetSize - 1)]
            secondParent = subset[randint(0, subsetSize - 1)]

            # select a random crossover point in the genespace
            crossoverPoint = randint(0, self.MOVE_LIMIT - 1)

            newPopulation.append(
                self.mutate(firstParent[:crossoverPoint] + secondParent[crossoverPoint:])
            )
        
        self.population = newPopulation

    def mutate(self, chromosome):
        if random() < self.MUTATION_CHANCE:
            chromosome[randint(0, self.MOVE_LIMIT - 1)] = randint(self.GENES[0], self.GENES[-1])
        
        return chromosome


if __name__ == '__main__':
    ga = GA()
    ga.run()