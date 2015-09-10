# Mini-project #6 - Blackjack

# Originally written in CodeSkulptor, saved at
# http://www.codeskulptor.org/#user40_LPg1mEIH8gfL0OC.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
outcome_text = "Hit Deal to play"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self): # create Hand object
        self.hand_cards = []

    def __str__(self):# return a string representation of a hand
        s = "Hand contains "
        for i in range(len(self.hand_cards)):
            s += str(self.hand_cards[i]) + " "
        return s
    
    def add_card(self, card): # add a card object to a hand
        self.hand_cards.append(card) 
                    
    def get_value(self): #add values of cards, determine if ace is 1 or 10
        self.hand_value = 0
        self.ace_count = 0
        for i in self.hand_cards:
            self.card_rank = i.get_rank()
            self.card_value = VALUES[self.card_rank]
            self.hand_value += self.card_value
            if self.card_rank == 'A':
                self.ace_count += 1
        if self.ace_count == 0:
            return self.hand_value
        elif self.ace_count >= 1 and self.hand_value + 10 <= 21:
            return self.hand_value + 10
        else: 
            return self.hand_value
             
    def draw(self, canvas, pos): # draw hand on canvas using draw method for cards
        hand_list_rank = 0
        for i in self.hand_cards:
            i.draw(canvas, [pos[0] + hand_list_rank * (CARD_SIZE[0] + 5), pos[1]])
            hand_list_rank += 1
            
# define deck class 
class Deck:
    def __init__(self): # create a Deck object
        self.deck_cards = []	
        for suit in SUITS:
            for ranks in RANKS:
                self.deck_cards.append(Card(suit, ranks))

    def shuffle(self): # shuffle the deck         
        random.shuffle(self.deck_cards)

    def deal_card(self):
        return self.deck_cards.pop()	# deal a card object from the deck
        
    def __str__(self): # return a string representing the deck
        s = "Deck contains "
        for i in range(len(self.deck_cards)):
            s += str(self.deck_cards[i]) + " "
        return s
            
#define event handlers for buttons
def deal(): #hitting deal in play forfeits round
    global player_hand, dealer_hand, deck_in_play, outcome, in_play, outcome_text, score 
    if in_play == True: 
        outcome_text = "Forfeited round. Hit or stand?"
        score -= 1
        player_hand = Hand() #create new Hand objects for player and dealer
        dealer_hand = Hand()
        deck_in_play = Deck() #create new Deck object and shuffle
        deck_in_play.shuffle()
        player_hand.add_card(deck_in_play.deal_card()) #add first cards
        dealer_hand.add_card(deck_in_play.deal_card())
        player_hand.add_card(deck_in_play.deal_card()) #add second cards
        dealer_hand.add_card(deck_in_play.deal_card())
    if in_play == False:    
        outcome_text = "Hit or Stand?"
        player_hand = Hand() #create new Hand objects for player and dealer
        dealer_hand = Hand()
        deck_in_play = Deck() #create new Deck object and shuffle
        deck_in_play.shuffle()
        player_hand.add_card(deck_in_play.deal_card()) #add first cards
        dealer_hand.add_card(deck_in_play.deal_card())
        player_hand.add_card(deck_in_play.deal_card()) #add second cards
        dealer_hand.add_card(deck_in_play.deal_card())
    in_play = True
            
def hit():
    global player_hand, dealer_hand, deck_in_play, score, outcome, outcome_text, in_play
    # if the hand is in play, hit the player
    if in_play == True and player_hand.get_value() < 21:
        player_hand.add_card(deck_in_play.deal_card())
        if player_hand.get_value() > 21:
            outcome = "Busted"
            outcome_text = "You busted. New deal?"
            score -= 1
            in_play = False             
        return outcome_text, in_play
        
def stand():
    global player_hand, dealer_hand, deck_in_play, outcome, in_play, outcome_text, score
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck_in_play.deal_card())
        # assign a message to outcome, update in_play and score
    while in_play == True:
        if dealer_hand.get_value() > 21 and player_hand.get_value() <= 21:
            outcome_text = "Dealer busted, so you win! New deal?"
            score += 1
            in_play = False
        elif player_hand.get_value() == 21 and dealer_hand.get_value() != 21:
            outcome_text = "You hit 21, you win! New deal?"
            score += 1
            in_play = False
        elif dealer_hand.get_value() < player_hand.get_value() < 21:
            outcome_text = "You're closer to 21, you win! New deal?"
            score += 1
            in_play = False
        elif player_hand.get_value() == dealer_hand.get_value() <= 21:
            outcome_text = "You tied, but dealer wins. New deal?"
            score -= 1
            in_play = False
        elif player_hand.get_value() > 21:
            outcome_text = "You busted. Dealer wins. New deal?"
            in_play = False
        elif dealer_hand.get_value() == 21:
            outcome_text = "Dealer hit 21, you lose. New deal?"
            score -= 1
            in_play = False
        elif player_hand.get_value() < dealer_hand.get_value() < 21:
            outcome_text = "Dealer's closer to 21, you lose. New deal?"
            score -= 1
            in_play = False
       
    # draw handler    
def draw(canvas):
    global player_hand, dealer_hand, deck_in_play, outcome, in_play, score, outcome_text
    canvas.draw_text("BLACKJACK", (180, 35), 42, "Yellow")
    canvas.draw_text("Score: " + str(score), (275, 75), 20, "Black")
    canvas.draw_text(outcome_text, (50, 350), 32, "Orange")
    player_hand.draw(canvas, [200, 400])
    dealer_hand.draw(canvas, [100, 100]) 
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (136, 147.5), CARD_SIZE)

#reset score to 0    
def reset():
    global score
    score = 0
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Reset Score", reset, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
