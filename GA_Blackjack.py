from Genetic_Algorithms import Genetic_Algorithm as GA
import random


def create_random_strategy(): #Creating a random playing strategy
    strategy=GA.Person([],0)    #Create a blank template for our strategy
    for your_hand_total in range(1,22): #Add an allele for each combination of dealer value and playe value
        for dealer_hand_total in range(2,12):
            new_allele_name=str(your_hand_total)+'-'+str(dealer_hand_total)
            potential_values=['Hit','Stand']
            value=potential_values[random.randint(0,1)]
            new_chromosome=GA.Allele(new_allele_name,value,potential_values)
            strategy.Alleles.append(new_chromosome)
    return (strategy)

def create_strategy_population(number_people):  #Create a population of random strategies
    population=GA.Population([],genetic_algorithm_blackjack_utility_function)   #Start with a blank population
    for n in range(number_people):  #Add random strategies to the population
        population.People.append(create_random_strategy())
    return(population)

def genetic_algorithm_blackjack_utility_function(strategy, repeats=100):    #This is our utility functions for the blackjack strategy which plays a certain number of rounds and sees what the score is
    score=0     #Start on a score of zero
    for n in range(repeats):    #Run n iterations
        result=play_blackjack_round(strategy)   #Checks what happens after a round of Blackjack
        if result=='Win':
            score+=1    #Assumes a bet of 1 on each round winning ine if you win
        if result=='Lose':
            score-=1    #Losing 1 if you lose
    return(score)

# Create a class to represent a card
class Card:
    # Each card is uniquely defined by a suit and value
    def __init__(self,suit,value):
        self.Suit=suit
        self.Number=value

    def blackjack_values_list(self):    #Function returns the value of a given card in blackjack
        if self.Number=='Jack' or self.Number=='Queen' or self.Number=='King':
            return([10])
        if self.Number=='Ace':
            return([1,11])
        else:
            return([self.Number])

    def __repr__(self):
        return(str(self.Number) + ' of ' + str(self.Suit))

class Deck:
    # A deck is just aa collection of cards
    def __init__(self,cards_list):
        self.Cards=cards_list

    # Function returns the top card from a deck whilst
    # removing it from the list
    def draw(self):
        drawn_card=self.Cards.pop()
        return(drawn_card)

    def shuffle(self):
        # Create a list for the new card list
        shuffled_deck=[]


        while len(self.Cards) > 0:  #Repeat following process till all card in the old deck are used
            n=random.randint(0, len(self.Cards) - 1)    #Choose a random card in the deck, place it at the beginning of the new deck and remove it from the old
            shuffled_deck.append(self.Cards[n])
            self.Cards.remove(self.Cards[n])

        self.Cards=shuffled_deck

    def remove_from_deck(self,card):    #Removes a card from the deck
        new_deck=Deck([])
        for deck_card in self.Cards:
            if deck_card.Suit==card.Suit and deck_card.Number==card.Number:
                pass
            else:
                new_deck.Cards.append(deck_card)
        return(new_deck)

    def remove_hand_from_deck(self,hand):   #Removes all the cards in a hand from the deck
        new_deck=Deck(self.Cards)
        for hand_card in hand.Cards:
            new_deck=new_deck.remove_from_deck(hand_card)
        return(new_deck)

class Blackjack_Hand:   #Class for blackjack specific hands

    def __init__(self,cards):
        self.Cards=cards

    def values_list(self):
        if len(self.Cards)==1:
            return(self.Cards[0].blackjack_values_list())
        else:
            old_blackjack_hand=Blackjack_Hand([])
            for n in range(len(self.Cards)-1):
                old_blackjack_hand.Cards.append(self.Cards[n])
            old_hand_values=old_blackjack_hand.values_list()
            last_card_values=self.Cards[-1].blackjack_values_list()
            new_hand_values=[]
            for old_value in old_hand_values:
                for new_value in last_card_values:
                    if new_value + old_value < 22:
                        new_hand_values.append(new_value+old_value)
        return(new_hand_values)

    def add_card(self,card):
        new_hand=Blackjack_Hand([])
        for old_card in self.Cards:
            new_hand.Cards.append(old_card)
        new_hand.Cards.append(card)
        return(new_hand)


def create_standard_deck(): #Create a deck of cards
    suits=['Hearts','Diamonds','Clubs','Spades']    #List of possible suits
    numbers=[2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']    #List of possible values
    cards=[]    #Create a list to put the cards in
    for suit in suits:
        for number in numbers:
            cards.append(Card(suit,number)) #Add one of every card to our deck
    standard_deck=Deck(cards)   #Turn our list to a deck class
    return(standard_deck)




def play_blackjack_round(strategy):     #Plays a round of blackjack using selected strategy
    deck=create_standard_deck()         #Create a deck to play with
    deck.shuffle()                      #Shuffle the deck
    player_hand=Blackjack_Hand([])
    player_hand=player_hand.add_card(deck.draw())
    player_hand=player_hand.add_card(deck.draw())
    dealer_hand=Blackjack_Hand([])
    dealer_hand=dealer_hand.add_card(deck.draw())
    return(play_blackjack_from(strategy,deck,dealer_hand,player_hand))


def play_blackjack_from(strategy, deck, dealer_hand, player_hand):
    if len(player_hand.values_list())==0:
        return('Lose')
    choice=what_to_do(strategy,dealer_hand.values_list()[-1],player_hand.values_list()[-1])
    if choice=='Stand':
        return (play_blackjack_from_stand(dealer_hand,player_hand,deck))
    if choice=='Hit':
        new_player_hand=player_hand.add_card(deck.draw())
        return(play_blackjack_from(strategy, deck, dealer_hand, new_player_hand))

def what_to_do(person, dealer_value, player_value):
    for alleles in person.Alleles:
        if alleles.Name == str(player_value) + '-' + str(dealer_value):
            return (alleles.Value)

def play_blackjack_from_stand(dealer_hand,player_hand,deck):
    if len(player_hand.values_list())==0:
        return('Lose')
    if len(dealer_hand.values_list())==0:
        return('Win')
    if dealer_hand.values_list()[-1]>=17:
        if who_wins(dealer_hand,player_hand)=='Dealer':
            return('Lose')
        if who_wins(dealer_hand,player_hand)=='Player':
            return('Win')
        if who_wins(dealer_hand,player_hand)=='Draw':
            return('Draw')
    if dealer_hand.values_list()[-1]<17:
        new_dealer_hand=dealer_hand.add_card(deck.draw())
        return(play_blackjack_from_stand(new_dealer_hand,player_hand,deck))

def who_wins(dealer_hand,player_hand):
    if len(player_hand.values_list())==0:
        return('Dealer')
    if len(dealer_hand.values_list())==0:
        return('Player')
    if player_hand.values_list()[-1]>dealer_hand.values_list()[-1]:
        return('Player')
    if player_hand.values_list()[-1]==dealer_hand.values_list()[-1]:
        return('Draw')
    if player_hand.values_list()[-1]<dealer_hand.values_list()[-1]:
        return('Dealer')

Blackjack_Population=create_strategy_population(50)
GA.run_genetic_algorithm_1(Blackjack_Population)

print('end')