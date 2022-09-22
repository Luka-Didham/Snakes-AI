__author__ = "Luka Didham"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "<didlu343@student.otago.ac.nz>"

import numpy as np
import random
import copy as cp

agentName = "SmartSnake"
perceptFieldOfVision = 9   # Choose either 3,5,7 or 9
perceptFrames = 3          # Choose either 1,2,3 or 4
trainingSchedule = [("random", 500)]
# trainingSchedule = None

# This is the class for your snake/agent
class Snake:

    # This is the init method which sets up a random new Snake. Each Snake is initially set with random values for its
    # chromosomes. After creation of the snakes the chromosomes are over written with parents chromosomes when applicable.
    # The structure of the chromosomes is an array as large as percepts and each chromosome is now a [3x1] inner array
    # representing each possible action [left, straight, right]. Bias is also set and stored so can be passed on to children snakes.
    def __init__(self, nPercepts, actions):
        self.nPercepts = nPercepts
        self.actions = actions
        self.bias = np.random.uniform(-50 ,50, 3)
        self.chromosome = [] #Individual chromosomes holding [x,x,x] values representing each action [left, straight, right]
        for c in range(self.nPercepts): #filling all three values within each chromosome.
            # Found wide range of chromosomes makes better results
            self.chromosome.append(np.random.uniform(-50 ,50, 3)) #inner variable chromosome values for each action (left, straight, right).

    #This method translates the 'percepts' to 'actions' by adjusting the magnitude and +/- of each possible item in percepts
    # For food we keep this positive (as we want to move towards food) and increase its magnitude by 10. Same species and
    # enemy species we make negative as we want to move away from these percepts and also increase their magnitudes by 10.
    # We increase the magnitude if each percept in order to encourage the snake to objectives.
    # 0 - move left
    # 1 - move forward
    # 2 - move right
    def AgentFunction(self, percepts):
        actions = [0.0,0.0,0.0]
        percepts_flatten = percepts.flatten()
        for p in range(len(percepts_flatten)):
            if(percepts_flatten[p]==2):
                percepts_flatten[p] = percepts_flatten[p] * 10 #Weighting food very positivly
            if (percepts_flatten[p] == 1):
                percepts_flatten[p] = percepts_flatten[p] * -10 #Weighting self negativly
            if (percepts_flatten[p] == -1):
                percepts_flatten[p] = percepts_flatten[p] * 10 #Weighting enemys negativly
        #
        # Different 'percepts' values should lead to different 'actions'.  This way the agent
        # reacts differently to different situations.
        #
        # Different 'self.chromosome' should lead to different 'actions'.  This way different
        # # agents can exhibit different behaviour.
        for c in range(len(self.chromosome)):  # each individual nested array
            array = self.chromosome[c]
            for a in range(len(array)):  # each individual chromosome value for each nested array relating to each action
                actions[a] = actions[a] + percepts_flatten[c] * array[a] #action valuing deciding on percepts

        for c in range(len(actions)):
            actions[c] = actions[c] + self.bias[c] #bias added at the end
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

# Method responsible for creating the next and improved generation of snakes
# Implements roulette wheel selection with scaling elitism and k-point crossover. Has 1% chance of mutation per chromosome copy
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


    # keep selecting until next generation full
    while(len(new_population)<N):
        #start doing roulette wheel breeding
        rand1 = random.uniform(0,1)
        rand2 = random.uniform(0,1)
        parent1_set = False
        parent2_set = False
        parent1 = Snake(nPercepts, actions)
        parent2 = Snake(nPercepts, actions)
        child = Snake(nPercepts, actions)
        mutation = 0.01

        #picking parents
        for c in range(N-1):
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

        for action_counter in range(3): #loop 3 for each action
            rand = random.uniform(0, 1.00)
            if rand < 0.5:  # take parent1 chromosome of specific action
                for chromo_counter in range(len(child.chromosome)):
                    rand_mut = random.uniform(0, 1.00)
                    child_chromo = child.chromosome[chromo_counter]
                    if rand_mut < 0.01:  # do random mutation
                        child_chromo[action_counter] = random.uniform(-50, 50)
                    else:
                        p1_chromo = parent1.chromosome[chromo_counter]
                        child_chromo[action_counter] = p1_chromo[action_counter]
                        child.chromosome[chromo_counter] = child_chromo
                child.bias[action_counter] = parent1.bias[action_counter]
            else:  # take parent2 chromosome of specific action
                for chromo_counter in range(len(child.chromosome)):
                    rand_mut = random.uniform(0, 1.00)
                    child_chromo = child.chromosome[chromo_counter]
                    if rand_mut < 0.01:  # do random mutation
                        child_chromo[action_counter] = random.uniform(-50, 50)
                    else:
                        p2_chromo = parent2.chromosome[chromo_counter]
                        child_chromo[action_counter] = p2_chromo[action_counter]
                        child.chromosome[chromo_counter] = child_chromo
                child.bias[action_counter] = parent1.bias[action_counter]
        new_population.append(child)
    return (new_population, avg_fitness)








