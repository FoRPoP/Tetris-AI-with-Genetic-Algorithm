import random
import tetrisGameAlGenetic
import _thread as thread
#### Genetic Algorithm ####

PARAMETERS_SIZE = 10
POPULATION_SIZE = 10
ELITISM_SIZE = 2
TOURNAMENT_SIZE = 4
MUTATION_PROBABILITY = 0.05
ITERATIONS = 25

class Individual:

    def __init__ (self):
        self.parameters = []
        for i in range(PARAMETERS_SIZE):
            self.parameters.append(random.uniform(-5, 5))
        self.fitness = tetrisGameAlGenetic.playTetris(self.parameters)

    def __lt__ (self, other):
        return self.fitness < other.fitness 

    def fitnessFunction(self):
        score = 0
        #score = tetrisGameAlGenetic.playTetris(self.parameters)
        for _ in range(5):
            score += tetrisGameAlGenetic.playTetris(self.parameters)

        self.fitness =  score / 5
        #self.fitness = score


def selection(population):
    min = float('-inf')
    for i in range(TOURNAMENT_SIZE):
        j = random.randrange(POPULATION_SIZE)
        if population[j].fitness > min:
            min = population[j].fitness
            selected = j

    return selected

def crossover(parent1, parent2, child1, child2):
    i = random.randrange(PARAMETERS_SIZE)
    for j in range(i):
        child1.parameters[j] = parent1.parameters[j]
        child2.parameters[j] = parent2.parameters[j]
    for j in range(i, PARAMETERS_SIZE):
        child1.parameters[j] = parent2.parameters[j]
        child2.parameters[j] = parent1.parameters[j]

def mutation(individual):
    for i in range(PARAMETERS_SIZE):
        if random.random() <= MUTATION_PROBABILITY:
            individual.parameters[i] = random.uniform(-5, 5)

population = []
newPopulation = []

for i in range(POPULATION_SIZE):
    population.append(Individual())
    newPopulation.append(Individual())

for iteration in range(ITERATIONS):
    print("Iteration: ", iteration)
    population.sort(reverse=True)

    with open ("tetrisData.txt", 'a') as file:
        file.write("Iteration: {}\n Top Individual Parameters: {}\n Top Individual Fitness: {}\n Bottom Individual Parameters: {}\n Bottom Individual Fitness: {}\n\n\n\n".format(iteration, population[0].parameters, population[0].fitness, population[-1].parameters, population[-1].fitness))

    for i in range(ELITISM_SIZE):
        newPopulation[i] = population[i]
    
    for i in range(ELITISM_SIZE, POPULATION_SIZE, 2):
        parent1 = selection(population)
        parent2 = selection(population)
        
        crossover(population[parent1], population[parent2], newPopulation[i], newPopulation[i + 1])
        
        mutation(newPopulation[i])
        mutation(newPopulation[i + 1])

        print("Individual:", i)
        newPopulation[i].fitnessFunction()
        newPopulation[i + 1].fitnessFunction()

    #fitnesses
    #for i in range(len(newPopulation)):
        #print(newPopulation[i])
        #thread.start_new_thread(newPopulation[i].fitnessFunction, ())
    population = newPopulation

population.sort(reverse=True)
for individual in population:
    print(individual.fitness, individual.parameters, "\n")
            