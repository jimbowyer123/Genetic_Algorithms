from Genetic_Algorithms import Genetic_Algorithm as GA
import random

def create_prisoner_strategy(): #Want to generate a random strategy for the prisoners dillema problem
    prisoner_strategy=GA.Person([],0)   #Start with an empty template of a person
    for i in range(3):  #Add Alleles to determine what the strategy does for the first three moves
        new_allele=GA.Allele('Turn ' + str(i+1),random.randint(0,1),[0,1])
        prisoner_strategy.Alleles.append(new_allele)
    for result_1 in [1,0]:  #Create Alleles representing what to do given the other programs past responses
        for result_2 in [1,0]:
            for result_3 in [1,0]:
                new_allele=GA.Allele(str(result_1)+str(result_2)+str(result_3),random.randint(0,1),[0,1])
                prisoner_strategy.Alleles.append(new_allele)
    return(prisoner_strategy)

def create_prisoner_strategy_population(number_people): #Create a population with a given number of strategies in
    new_population=GA.Population([],function_0)
    for i in range(number_people):
        new_population.People.append(create_prisoner_strategy())
    return(new_population)

def past_list_to_string(past_list): #Function that turns the list of past moves to a string form like in the name of the allele
    string=''
    for i in range(len(past_list)):
        string=string+str(past_list[i])
    return(string)

def function_0(strategy):   #Created a function to fill in the population function as I had to adjust how the population function worked
    return(0)

def play_first_round(person_1,person_2):    #Function returns the results of the first round of the prisoners dillema problem
    results=(person_1.Alleles[0].Value,person_2.Alleles[0].Value)
    return(results)

def play_second_round(person_1,person_2):   #Function returns the second round of the prisoners dillema problem
    return((person_1.Alleles[1].Value,person_2.Alleles[1].Value))

def play_third_round(person_1,person_2):    #Function returns the third round of the prisoners dillema problem
    return((person_1.Alleles[2].Value,person_2.Alleles[2].Value))

def play_round(person_1,person_2,person_1_past,person_2_past):  #Function returns of the results of later rounds of the prisoners dillema problem base on the other strategies result
    person_1_play=0
    person_2_play=0
    person_1_past_string=past_list_to_string(person_1_past)
    person_2_past_string=past_list_to_string(person_2_past)
    for i in range(3,len(person_1.Alleles)):
        if person_2_past_string==person_1.Alleles[i].Name:
            person_1_play=person_1.Alleles[i].Value
            break
    for i in range(3,len(person_2.Alleles)):
        if person_1_past_string==person_2.Alleles[i].Name:
            person_2_play=person_2.Alleles[i].Value
            break
    return((person_1_play,person_2_play))


def play_prisoners_dilemma(person_1,person_2,number_rounds=100):    #Plays the prisoners dillema between two 'people' for a certain number of rounds
    results=(0,0)
    person_1_past=[]
    person_2_past=[]
    for i in range(number_rounds):
        if i==0:
            results=play_first_round(person_1,person_2)
        if i==1:
            results=play_second_round(person_1,person_2)
        if i==2:
            results=play_third_round(person_1,person_2)
        if i>2:
            results=play_round(person_1,person_2,person_1_past,person_2_past)
        if len(person_1_past)>=3:
            person_1_past.pop(0)
            person_1_past.append(results[0])
            person_2_past.pop(0)
            person_2_past.append(results[1])
        if len(person_1_past)<3:
            person_1_past.append(results[0])
            person_2_past.append(results[1])
        if results[0]==1:
            person_2.Utility_Score -= 10
        if results[1]==1:
            person_1.Utility_Score -=10
        if results==(0,0):
            person_1.Utility_Score -=6
            person_2.Utility_Score -=6


def prisoner_utility_function(population):  #Utility function runs on the population since different strategies play each other
    for i in range(len(population.People)-1):
        for j in range(i+1,len(population.People)):
            play_prisoners_dilemma(population.People[i],population.People[j])

population=create_prisoner_strategy_population(20)
average_scores=[]
while population.Generation<100:
    prisoner_utility_function(population)
    average_scores.append(population.average_score())
    population.transform_scores()
    population.normalise_scores()
    Mating_Pool = population.create_mating_pool()
    population = Mating_Pool.crossbreed()
    population = population.mutate()

print('end')

