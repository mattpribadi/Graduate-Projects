#Name: Matt Pribadi
#Project: 1
#Title: Phom Card Game

from os import system, name
import sys
import random as rand

class HandSizeException(Exception):
    '''Placeholder for improper hand size exception'''
    pass

class DiscardException(Exception):
    '''Placeholder for improper discard user selection'''
    pass

class InvalidEntryException(Exception):
    '''Placeholder for general invalid user selection'''
    pass

class PlayingCard:
    '''
    A PlayingCard class with a specific suit and rank (number) 
    and raising an exception if an invalid suit or rank is entered.
    '''
    def __init__(self, rank, suit):
        
        self.__rankList = ['2','3','4','5','6','7',
                           '8','9','10','J','Q','K','A']
        
        self.__rankKey = {'J':'11', 'Q':'12', 'K':'13', 'A':'1'}
        
        self.__suitList = '♠♥♦♣'
        
        if rank.upper() in self.__rankList:
            self.rank = rank.upper()
        else:
            raise Exception('Invalid rank entered.')
        
        if suit in self.__suitList:
            self.suit = suit
        else:
            raise Exception('Invalid suit entered.')
    
    def getValue(self):
        '''
         Returns
        -------
        Int
            The value of the card as indicated by its number or rankKey.
        '''
        if self.rank not in self.__rankKey.keys():
            return int(self.rank)
        else:
            return int(self.__rankKey[self.rank])
    
    def __str__(self):
        return self.suit + ' ' + self.rank

    def __repr__(self):
        
        return self.suit + ' ' + self.rank
    
    def __lt__(self, card2):
        
        return self.getValue() < card2.getValue()

    def __gt__(self, card2):
        
        return self.getValue() > card2.getValue()
    
    def __le__(self, card2):
        
        return self.getValue() <= card2.getValue()

    def __ge__(self, card2):
        
        return self.getValue() >= card2.getValue()
    
    def __eq__(self, card2):
        
        if self.rank == card2.rank and self.suit == card2.suit:
            return True
        else:
            return False
        
    def __sub__(self, card2):
        
        return self.getValue() - card2.getValue()
    
class Hand:
    '''
    Instance of all the hand actions one can 
    perform when playing a card game.
    '''
    
    def __init__(self, cardList):
        self.cardList = cardList
        self.discard = []
        self.matches = []
        self.score = 0

    def dispMatches(self):
        '''
        Returns
        -------
        List
            List of matching sets of unique cards in the hand
            Also removes these cards from the cardList.
        '''
        
        self.cardList.sort()
        
        for i in range(len(self.cardList)-2):
            j = i + 1
            k = j + 1            
            card1 = self.cardList[i]
            card2 = self.cardList[j]
            card3 = self.cardList[k]
            
            matchSet = [card1, card2, card3]
            if card1.suit == card2.suit and card2.suit == card3.suit:
                diff1 = card3 - card2
                diff2 = card2 - card1
                if diff1 == 1 and diff2 == 1:
                    self.matches.extend(matchSet)
            elif card1.rank == card2.rank and card2.rank == card3.rank:
                    self.matches.extend(matchSet)
        self.cardList = [i for i in self.cardList if i not in self.matches]
        
        res = [] 
        [res.append(x) for x in self.matches if x not in res]         
        
        self.matches = res
        return self.matches
    
    def orderCards(self):
        ''' Sorts the cards in order based on PlayingCard value '''
        
        self.cardList.sort()
    
    def discardCard(self, cardIndex):
        ''' Removes a card based on its index in the cardList.
            Adds this discarded card to a discard List. '''
        
        self.discard.append(self.cardList[cardIndex])
        self.cardList.pop(cardIndex)
        
    def displayHand(self):
        '''
        
        Returns
        -------
        String
            Returns the Hand's cardList as a string

        '''
        
        self.orderCards()
        return str(self.cardList)  
    
    def getHand(self):
        '''
        
        Returns
        -------
        String
            Returns the Hand's cardList as a string

        '''
        
        self.orderCards()
        return self.cardList 
    
    def getDiscard(self):
        '''
        
        Returns
        -------
        List
            Returns the Hand's discard pile.

        '''
        
        return self.discard
    
    def popDiscard(self):
        '''
        Remove the hand's top discarded card and returns the discard pile.

        Returns
        -------
        List
            Returns the Hand's discard pile.

        '''
        
        if len(self.discard) > 0:
            self.discard.pop(-1)
        
        return self.discard
    
    def scoreHand(self):
        '''Adds up the number of points in the player’s hand.
        
        Returns
        -------
        Int
            Returns the Hand's score based on its card values.

        '''
        
        self.dispMatches()
        
        for i in self.cardList:
            self.score += i.getValue()
        return self.score
    
    def __str__(self):
        '''Properly displays a hand.'''
        
        return str(self.cardList)

    def __repr__(self):
        '''Properly displays a hand.'''
        return [i for i in self.cardList]

class Deck:
    '''
    A Deck class creates a list of PlayingCard objects that can be manipulated
    '''
    
    def __init__(self):
       
        self.__rankList = ['2','3','4','5','6','7',
                           '8','9','10','J','Q','K','A']
        self.__suitList = '♠♥♦♣'
        
        self.cards = [PlayingCard(rank,suit) for rank in self.__rankList 
                          for suit in self.__suitList]
        
        self.shuffle_deck()
        
    def shuffle_deck(self):
        '''Randomly shuffles the deck'''
        
        rand.shuffle(self.cards)
    
    def deal_card(self, cardCount = 1):
        '''

        Parameters
        ----------
        cardCount : Int, optional
            Number of cards to deal. The default is 1.

        Raises
        ------
        Exception
            Raises an error when dealing more cards than the deck has left.

        Returns
        -------
        dealtCards : List
            Returns cards dealt as a list.

        '''
        
        if cardCount > len(self.cards):
            raise Exception('Cannot deal ' 
                            + str(cardCount) 
                            + ' cards. The deck only has ' 
                            + str(len(self.cards)) 
                            + ' cards left!')
            
        else:
            dealtCards = []
            
            for i in range(0,cardCount):
                dealtCards.append(self.cards.pop(0))
        return dealtCards
     
    def __str__(self):
        
        return str(self.cards)
    
class CardGame():
    '''Creates a game instance'''
    
    def __init__(self, playerCount=4):
        self.playerCount = playerCount
        self.handDict = {}
        self.rounds = 1
        self.deck = Deck()
        
    def deal(self, num = 1):
        '''
		Deals a specific number of cards to the number of players. 
        Parameters
        ----------
        num : Int, optional
            The number of cards dealt to each player. The default is 11.

        '''
        for i in range(1, self.playerCount + 1):
            player = 'Player ' + str(i)
            hand = Hand(self.deck.deal_card(num))
            self.handDict[player] = hand
            
    def dispCards(self):
        '''Displays all the cards in each players' hands'''
        
        for key, value in self.handDict.items():
            print(key + ':', value)
            
    def incRound(self):
        '''Increments the number of rounds played'''
        
        self.rounds += 1
    
    def getRound(self): 
        '''
        Returns
        -------
        Int
            Returns the current round
        '''
        
        return self.rounds
    
    def deckLeft(self):
        '''
        Returns
        -------
        Int
            Returns the number of cards left in the deck
        '''
        return len(self.deck.cards)
    
    def gameEnd(self):
        '''Placeholder method for a game end condition.'''
        pass
    
    def __str__(self):
        return str(self.handDict)
    '''Placeholder for general user entry error'''
    
    pass

class Phom(CardGame):
    '''Creates a Phom game instance that extends a type of 
    CardGame with extra functions'''
    

    def __init__(self, playerCount=4):
        
        super().__init__(playerCount)
        super().deal(9)
        self.currentPlayer = 1
        self.meldDict = {}
        
        for key in self.handDict.keys():
            self.meldDict[key] = []
    
    def introduction(self):
        # Introduction
        print('-' * 80)
        print("Welcome to the Phom, a Rummy-style Card Game!")
        print('-' * 80)
        print("Instructions|")
        print('-' * 12)
        print('\n' * 1)
        print("A 52 card deck has been created and shuffled.")
        print("Each player has been dealt 9 cards to start off.")
        print('\n' * 1)
        print("Each player will take turns in drawing a card to complete a matching")
        print("set of cards (3-of-a-Kind, 3-Card-Suited-Straight, or more) and then")
        print("discarding a card in your hand.")
        print('\n' * 1)
        print("Scoring is based on card value. The LOWEST score wins! Good Luck!")
        print('-' * 80)
        print('\n' * 1)
        
    def dispChoice(self):
        '''
        Displays the previous opponent’s top discard card.

        Returns
        -------
        topDiscard : PlayingCard
            Returns the top discarded PlayingCard object.

        '''
               
        if self.currentPlayer == 1:
            prevPlayer = 'Player ' + str(4)
        else:
            prevPlayer = 'Player ' + str(self.currentPlayer - 1)
            
        prevHand = self.handDict[prevPlayer]
        prevDiscard = prevHand.getDiscard()
        
        if not prevDiscard:
            topDiscard = None
        else:
            topDiscard = prevDiscard[-1]
        
        if topDiscard is None:
            print(prevPlayer +  ' has no discards')
        else: 
            print(prevPlayer + '\'s top discard is [' + 
                  str(topDiscard) + ']')
        

        return topDiscard
    
    def dispPlayed(self):
        '''Displays all the discarded and melded cards.'''
        
        for key, value in self.handDict.items():
            print()
            print(key + '\'s discard pile: ', value.getDiscard())
            print(key + '\'s melded cards: ', self.meldDict[key])
            print('-' * 12)
            
    def dispCurrentHand(self):
        '''

        Returns
        -------
        currentHand : List
            Returns the currentPlayer's Hand as a list of PlayingCard objects.

        '''
        keyPlayer = 'Player ' + str(self.currentPlayer)
        currentHand = self.handDict[keyPlayer]
        # print(keyPlayer + '\'s current hand is:', currentHand.displayHand())
        
        return currentHand
        
    def hit(self):
        '''Calls the Deck class’s deal_card function and add's it to
            the current player's hand.'''
        
        keyPlayer = 'Player ' + str(self.currentPlayer)
        cardList = self.handDict[keyPlayer].getHand()
        cardList.extend(self.deck.deal_card())
    
    def meld(self):
        '''Takes the opponent’s top discard card, add's to current player's
            hand. Also adds this card to the melded cardlist.'''
        
        if self.currentPlayer == 1:
            prevPlayer = 'Player ' + str(4)
          
        else:
            prevPlayer = 'Player ' + str(self.currentPlayer - 1)
        

        prevHand = self.handDict[prevPlayer]
        getDiscard = prevHand.getDiscard()
        topDiscard = [getDiscard[-1]]
        
        keyPlayer = 'Player ' + str(self.currentPlayer)
        currentHand = self.handDict[keyPlayer].getHand()
        
        currentHand.extend(topDiscard)
        self.meldDict[keyPlayer].extend(topDiscard)
        
        prevHand.popDiscard()
    
    def discardOne(self, index):
        '''
        Discards one from the current player's hand.'
        
        Parameters
        ----------
        index : Int
            Index of the PlayingCard being removed from the current
            player's hand.

        '''

        keyPlayer = 'Player ' + str(self.currentPlayer)
        
        currentPlayer = self.handDict[keyPlayer]
        currentPlayer.discardCard(index)
        
        # print(currentPlayer.getDiscard())
        
    
    def finalScore(self):
        '''
        Determines the winner based on the lowest score

        Returns
        -------
        lowestKey : String
            The player(s) with the lowest score(s).

        '''
        lowestScore = 9999
        lowestKey = ''
        
        for key, value in self.handDict.items():
            currentScore = value.scoreHand()
            
            if currentScore < lowestScore:
                lowestScore = currentScore
                lowestKey = key
            elif currentScore == lowestScore:
                lowestKey = lowestKey + ' and ' + key
            
            
            print(key + '\'s matching sets are', value.dispMatches())
            print(key + '\'s final hand is', value.displayHand())
            print(key + '\'s final sore is', currentScore)
            print()
            
            
        return lowestKey
    
    def gameEnd(self):
        '''
        Checks for the game end condition. Then calls Hand.dispMatches,
            which display matches and score each hand in handDict.

        Returns
        -------
        bool
            Returns True if the Game End condition is achieved.

        '''
        
        for key, value in self.handDict.items():
            hand = Hand(value.cardList)
            if len(hand.dispMatches()) == 9:
                return True
        
        if self.rounds == 5:
            return True
        else:
            return False

    def clear(self): 
        '''Used to clear the window'''
    
        # Windows users 
        if name == 'nt': 
            _ = system('cls') 
            
        # Mac users
        else: 
            _ = system('clear')
            
#-------------------------MAIN------------------------------------------
if __name__ == "__main__":
    # Initialization
    # Used to check for valid inputs
    validIndex = [int(i) for i in '0123456789']
    run = True
    
    game = Phom()
    game.introduction()

    cmd = input("Play the game? (y/n): ").lower()
    if cmd != 'y':
        sys.exit()
    
    # Begin Gameplay
    game.hit()
    firstMove = True
    
    #Main user interface loop
    while run == True:
        
        validMove = False
        # Determines the current player and their hand
        currentPlayer = 'Player ' + str(game.currentPlayer)
        currentHand = game.dispCurrentHand()
        
        print('-' * 20 + 'Round ' + str(game.getRound()) + '-' * 18)
        print('-' * 10 + currentPlayer + ' it is your turn.' + '-' * 10)
        print('\n' * 15)
        
        # Displays the previous player's discarded card
        game.dispChoice()
        print('Cards left in the deck:', str(game.deckLeft()) + '\n')
        print(currentPlayer + '\'s current hand is',
                  currentHand.displayHand() + '\n')   
        
        # Ignores these actions during the first round of the first player
        if firstMove != True:   
            
            # Continues looping until a valid move is performed
            while validMove == False:
                print("Available Moves:")   
                print("[H] - Hit (Draw a card) from the deck")
                print('[M] - Meld (Take a card from the previous ' + 
                      'opponent\'s discard)')
                print("[C] - Current Hand")
                print("[S] - Show all Discard/Melded Cards")
                print("[Q] - Quit the game")
                
                try:
                    cmd = input("Please enter a command: ").lower()
                    
                    # 'Hit' game action
                    if cmd[0] == "h":
                        
                        if len(currentHand.getHand()) == 10:
                            raise HandSizeException()
                        else:
                            game.hit()
                            validMove = True
                    
                    # 'Meld' game action
                    elif cmd[0] == "m":
                        if game.dispChoice() is None:
                            raise DiscardException()
                        elif len(currentHand.getHand()) == 10:
                            raise HandSizeException()
                        else:
                            game.meld()
                            validMove = True
                    
                    # Show all cards that have been melded or discarded
                    elif cmd[0] == "s":
                            game.dispPlayed()
                            print('\n' * 2)
                      
                    # Show current hand
                    elif cmd[0] == "c":
                        print('\nCards left in the deck:', 
                              str(game.deckLeft()) + '\n')
                        
                        print(currentPlayer + '\'s current hand is',
                              currentHand.displayHand() + '\n')    
                    
                    # Used to quit the game
                    elif cmd[0] == "q":
                        confirm = input('Are you sure you want '
                                        + 'to end the game? (Y/N): ')
                        
                        if confirm.lower() == 'y':
                            sys.exit()
                            run = False
                    
                    #Sends the user an error when an invalid entry is made.
                    else:
                        raise InvalidEntryException()
                        
                except HandSizeException:
                    print()
                    print('-' * 10 + 'Error' + '-' * 10)
                    print('You cannot draw another card, you already have 10')
                    print('-' *25)
                except DiscardException:
                    print()
                    print('-' * 10 + 'Error' + '-' * 10)
                    print('The previous opponent has not discarded a card')
                    print('-' * 25)
                except InvalidEntryException:
                    print('-' * 10 + 'Error' + '-' * 10)
                    print('Please enter a valid command')
                    print('-' *25)
        
        # Continues looping until this second action recieves a valid move.
        secondMove = False
        
        while secondMove == False:
            print('\n' * 2)
            print(currentPlayer + '\'s current hand is',
                  currentHand.displayHand())  
            
            # Displays the index for easy user viewing.
            print('Index number:              ' +
                  '[  0,   1,   2,   3,   4,   5,   6,   7,   8,   9]')
            print()
            
            try:
                index = input("Choose a card to discard" +
                              " (enter a number from 0 to 9) " + 
                              "or enter [s] to show discards: ").lower()
                
                if index[0] == "s":
                    game.dispPlayed()
                    print('\n' * 2)
                    continue
                
                currentCards = currentHand.getHand()
                chosenCard = currentCards[int(index)]
                
                if chosenCard in game.meldDict[currentPlayer]:
                    raise DiscardException()
                elif  0 <= int(index) < 10:
                    game.discardOne(int(index))
                    secondMove = True
                else:
                    raise ValueError()
            
            except DiscardException:
                    print()
                    print('-' * 10 + 'Error' + '-' * 10)
                    print('You cannot discard a card you melded')
                    print('-' * 25)
            except:
                    print()
                    print('-' * 10 + 'Error' + '-' * 10)
                    print('Please enter an integer from 0 to 9.')
                    print('-' * 25)
            
    
        firstMove = False
        print('\n' * 20)
        game.clear()
        
        # Cycles through the rounds
        if game.currentPlayer == 4:
            game.incRound()
        
            if game.gameEnd() == True:
                break
        
        # Cycles through the current players
        if game.currentPlayer == 4:
            game.currentPlayer = 1
        else:
            game.currentPlayer += 1
        
    
    # Does the final scoring calculation and checks the winner
    winner = game.finalScore()

    print('\nCongratulations!', winner + ' wins!\n')
    replay = input('Press enter to close the file:')

