#Relevant imports for the simple genetic algorithm
import random

#Create a class called population which holds the items that we run the Algorithm on
class Population:
    def __init__(self,people,utility_function,generation=0):
        self.People=people          #A list of 'People' in our population
        self.Generation=generation  #A number to tell us which generation our population is up to
        self.Utility_Function=utility_function  #A Function that can be applied to the people of our population to give them a score
    def assign_scores(self):       #Creating a function to assign scores for the population
        for Person in self.People:  #Running a loop through the people in the population
            Person.Utility_Score=self.Utility_Function(Person)  #Sets the peron's score equal to its performance in the utility function

    def retrieve_scores_list(self):
        scores=[]       #Create a list that we can fill with the population scores
        for Person in self.People:  #Run through the people in the population
            scores.append(Person.Utility_Score) #Add their scores to the scores list
        return(scores)


    def transform_scores(self):    #To implement the algorithm we must make all the scores greater than or equal to zero but maintain the same order
        scores=self.retrieve_scores_list()  #Get the current list of scores
        min_score=min(scores)       #Find the minimum score in the list of sores
        if min_score<0:             #Check to see if the minimum is negative, If it is not then we do not need to do any transformations
            for i in range(len(scores)):
                self.People[i].Utility_Score=scores[i]-min_score  #If min score is negative then make a simple addition transformation so they are all non negative and set that as the new scores for the population

    def normalise_scores(self):     #Want to assign scores as proportions of total population score
        scores=self.retrieve_scores_list()  #Retrieve a current list of the scores for the population
        sum_scores=sum(scores)      #Find the sum of all scores
        for i in range(len(scores)):
            self.People[i].Utility_Score=scores[i]/sum_scores  #Reassign the scores as a proportion of the sum of the scores

    def create_mating_pool(self):
        population_size=len(self.People)    #Find how many people are in our population
        Mating_Pool=Population([],self.Utility_Function,self.Generation)  #Let the mating pool be a new population but with same generation count
        for i in range(population_size):        #Run iteration through population size to create mating pool of the same size
            random_number=random.random()       #produce psuedorandom number between 0 and 1 which will be used to choose who makes it to the mating pool
            score_count=0       #Start a score count to add up the scores till the random number is within the range of a persons score interval
            for Person in self.People:    #Run an iteration through the population to choose who gets added to the mating pool
                score_count=score_count+Person.Utility_Score    #Add new persons score to the score count creating an interval between last score count and new score count
                if random_number<score_count:   #See if the random number is within the relevant interval
                    Mating_Pool.People.append(Person)   #If it is within the interval then add said person to the mating pool
                    break       #Break so we do not add more people from this iteration
        return(Mating_Pool)


    def crossbreed(self):
        New_Population=Population([],self.Utility_Function,self.Generation+1)   #Create template for our new population with one higher generation
        while len(self.People)>0:   #While people are still in the mating pool continue the process
            new_people=mate(self.People.pop(),self.People.pop())    #Mate the two end people in the mating pool
            New_Population.People=New_Population.People+new_people  #Add the new offspring to the new population
        return(New_Population)

    def mutate(self,mutation_coefficient=0.01):
        new_people=[]
        for person in self.People:
            new_people.append(person.mutate(mutation_coefficient))
        return(Population(new_people,self.Utility_Function,self.Generation))

    def average_score(self):
        scores=self.retrieve_scores_list()
        average_score=sum(scores)/len(scores)
        return(average_score)


#Create a class for 'People' in our population
class Person:
    def __init__(self,alleles,utility_score):
        self.Alleles=alleles    #List of Alleles defining our 'Person'
        self.Utility_Score=utility_score    #A score for the fitness of our 'Person'

    def mutate(self,mutation_coefficient):
        new_alleles=[]
        for allele in self.Alleles:
            new_alleles.append(allele.mutate(mutation_coefficient))
        return(Person(new_alleles,self.Utility_Score))

    def __repr__(self):
        return_string='['
        for allele in self.Alleles:
            return_string=return_string+' '+str(allele.Value)+' '
        return(return_string+']')





#Create a class for our Alleles that define a characteristic of our 'Person'
class Allele:
    def __init__(self,name,value,possible_values):
        self.Name=name      #A string name describing the characteristic the Allele controls
        self.Value=value    #A value that determines the effect our Allele has
        self.Possible_Values=possible_values    #A list of the possible values our Allele could take


    def mutate(self,mutation_coefficient):   #Need to be able to mutate Alleles to avoid the algorithm getting stuck at local maximums
        random_number=random.random()  #Psuedorandom number to decide if the allele mutates
        new_value=self.Value
        if random_number<mutation_coefficient:
            new_value=self.Possible_Values[random.randint(0,len(self.Possible_Values)-1)]  #If the random number less than the mutation coefficient then mutate the allele to any of its possible values
        return(Allele(self.Name,new_value,self.Possible_Values))

    def __repr__(self):
        return(self.Name + ' = ' +str(self.Value))


def mate(Person_A,Person_B):        #Function that will mate two people classes
    number_alleles=len(Person_A.Alleles)    #Find the number of Alleles in each Person
    random_int=random.randint(1,number_alleles-1)   #Create a random integer which will represent where our people swap their alleles
    New_Person_One=Person([],0) #Create the template for our offspring
    New_Person_Two=Person([],0)
    for i in range(number_alleles): #Iterate through the number of alleles to chooses who gets which ones
        if i<random_int:    #All alleles less than are random integer are passed to our new people one way
            New_Person_One.Alleles.append(Person_A.Alleles[i])
            New_Person_Two.Alleles.append(Person_B.Alleles[i])
        else:               #All alleles after our the random integer are passed down the other way
            New_Person_One.Alleles.append(Person_B.Alleles[i])
            New_Person_Two.Alleles.append(Person_A.Alleles[i])
    return([New_Person_One,New_Person_Two]) #Return the list of the two new offspring



def run_genetic_algorithm_1(initial_population,number_generations=100):
    population=initial_population
    average_scores=[]
    while population.Generation<number_generations:
        population.assign_scores()
        average_scores.append(population.average_score())
        population.transform_scores()
        if max(population.retrieve_scores_list())==0:
            return(population)
        population.normalise_scores()
        Mating_Pool=population.create_mating_pool()
        population=Mating_Pool.crossbreed()
        population=population.mutate()
    return(population)
