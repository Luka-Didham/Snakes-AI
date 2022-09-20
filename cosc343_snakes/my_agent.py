__author__ = "Luka Didham"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "<didlu343@student.otago.ac.nz>"

import numpy as np
import random
import copy as cp

agentName = "<SmartSnake>"
perceptFieldOfVision = 3  # Choose either 3,5,7 or 9
perceptFrames = 1          # Choose either 1,2,3 or 4
#trainingSchedule = [("self", 10), ("random", 10)]
trainingSchedule = None

# This is the class for your snake/agent
class Snake:

    def __init__(self, nPercepts, actions):
        # You should initialise self.chromosome member variable here (whatever you choose it
        # to be - a list/vector/matrix of numbers - and initialise it with some random
        # values)
        self.nPercepts = nPercepts
        self.actions = actions
        self.chromosome = []  # list of chromosomes holding [x,x,x] values representing each action
        for c in range(self.nPercepts):
            self.chromosome[c] = np.random.uniform(-1, 1, 3)


def AgentFunction(self, percepts):
    # You should implement a model here that translates from 'percepts' to 'actions'
    # through 'self.chromosome'.
    #
    # The 'actions' variable must be returned and it must be a 3-item list or 3-dim numpy vector
    #
    # The index of the largest numbers in the 'actions' vector/list is the action taken
    # with the following interpretation:
    # 0 - move left
    # 1 - move forward
    # 2 - move right
    #
    actions = [0.0, 0.0, 0.0]

    chomosome_split = np.array_split(self.chromosome, 3)
    percepts_flatten = percepts.flatten()
    #
    # Different 'percepts' values should lead to different 'actions'.  This way the agent
    # reacts differently to different situations.
    #
    # Different 'self.chromosome' should lead to different 'actions'.  This way different
    # agents can exhibit different behaviour.

    # .
    # .
    # .
    # # agents can exhibit different behaviour.
    count = 0
    while (count < 3):
        for c in chomosome_split[count]:
            for x in percepts_flatten:
                actions[count] = actions[count] + c * x
        actions[count] = actions[count]  # + random.uniform(0,1*perceptFieldOfVision) #random bias
        count = count + 1

    index = np.random.randint(low=0, high=len(self.actions))
    return self.actions[index]
    return self.actions[np.argmax(actions)]

def evalFitness(population):

    N = len(population)

    # Fitness initialiser for all agents
    fitness = np.zeros((N))
    # This loop iterates over your agents in the old population - the purpose of this boiler plate
    # code is to demonstrate how to fetch information from the old_population in order
    # to score fitness of each agent
    for n, snake in enumerate(population):
        # snake is an instance of Snake class that you implemented above, therefore you can access any attributes
        # (such as `self.chromosome').  Additionally, the object has the following attributes provided by the
        # game engine:
        #
        # snake.size - list of snake sizes over the game turns
        # .
        # .
        # .
        maxSize = np.max(snake.sizes)
        turnsAlive = np.sum(snake.sizes > 0)
        maxTurns = len(snake.sizes)

        # This fitness functions considers snake size plus the fraction of turns the snake
        # lasted for.  It should be a reasonable fitness function, though you're free
        # to augment it with information from other stats as well
        fitness[n] = maxSize + turnsAlive / maxTurns
    return fitness


def newGeneration(old_population):

    # This function should return a tuple consisting of:
    # - a list of the new_population of snakes that is of the same length as the old_population,
    # - the average fitness of the old population

    N = len(old_population)

    nPercepts = old_population[0].nPercepts
    actions = old_population[0].actions

    fitness = evalFitness(old_population)

    # At the end you need to compute the average fitness and return it along with your new population
    avg_fitness = np.mean(fitness)
    sum_fitness = np.sum(fitness)

    # At this point you should sort the old_population snakes according to fitness, setting it up for parent
    # selection.



    # Create new population list...
    new_population = list()


    #elitism selection which selects nSnakes-(nSnakes-average fitness) while < nSnakes
    elite_count = 0
    temp_old_population = cp.deepcopy(old_population)
    temp_fitness = cp.deepcopy(fitness)
    while elite_count < (N-(N-avg_fitness)):
        # Create a new elite snake
        # new_snake = Snake(nPercepts, actions) usual way but doing pure elitisim for some
        new_snake = temp_old_population[np.argmax(temp_fitness)]
        new_population.append(new_snake)
        temp_old_population.remove(new_snake)
        temp_fitness = np.delete(temp_fitness, np.argmax(temp_fitness))
        elite_count = elite_count + 1

    #normalizing for roulette selection
    normalised_snakes = np.zeros(N)
    for c in range(N):
        sum = 0
        count = 0
        while(count <= c):

            sum = sum + fitness[count] #normalising
            count = count + 1
        normalised_snakes[c] = sum/sum_fitness



    while(len(new_population)<N): #start doing roulette wheel breeding
        rand1 = random.uniform(0,1)
        rand2 = random.uniform(0,1)
        parent1_set = False
        parent2_set = False
        parent1 = Snake(nPercepts, actions)
        parent2 = Snake(nPercepts, actions)
        child = Snake(nPercepts, actions)
        child_chromosome = np.zeros(nPercepts*3)
        mutation = 0.05

        for c in range(N-1):
            print(len(old_population))
            print(N)
            if (not parent1_set):
                if(rand1<normalised_snakes[c]):
                    parent1 = old_population[c]
                    parent1_set = True
            if (not parent2_set):
                if(rand2<normalised_snakes[c]):
                    parent2 = old_population[c]
                    parent2_set = True
            if(parent1_set and parent2_set):
                break
            #got parents now do cross over

        for c in range(len(child_chromosome)/3):
            rand = random.uniform(0, 1.05)
            if rand < mutation:  # do random mutation
                child_chromosome[c] = random.uniform(-1, 1)
            elif rand < 0.55:  # take parent1 chromosome
                child_chromosome[c] = parent1.chromosome[c]
            else:  # take parent2 chromosome
                child_chromosome[c] = parent2.chromosome[c]
        child.chromosome = child_chromosome
        new_population.append(child)




        # Here you should modify the new snakes chromosome by selecting two parents (based on their
        # fitness) and crossing their chromosome to overwrite new_snake.chromosome

        # Consider implementing elitism, mutation and various other
        # strategies for producing a new creature.

        #new_snake = Snake(nPercepts, actions)


        # Add the new snake to the new population
        #new_population.append(new_snake)



    return (new_population, avg_fitness)




