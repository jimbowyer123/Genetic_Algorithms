import random
import Genetic_Algorithms
from Genetic_Algorithms import Genetic_Algorithm as GA



def create_person():
    Person=GA.Person([],0)
    for i in range(5):
        Allele=GA.Allele('',random.randint(0,1),[0,1])
        Person.Alleles.append(Allele)
    return(Person)

def x_squared_utility_function(Person):
    score=0
    for i in range(len(Person.Alleles)):
        score=score+(2**i)*Person.Alleles[i].Value
    return(score)

def create_population(number_people):
    Population=GA.Population([],x_squared_utility_function)
    for i in range(number_people):
        Population.People.append(create_person())
    return(Population)

GA.run_genetic_algorithm_1(create_population(50),1000)

print('end')
