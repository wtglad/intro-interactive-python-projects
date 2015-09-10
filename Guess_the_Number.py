# "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

# Written in CodeSkulptor, originally saved at 
# http://www.codeskulptor.org/#user40_VSo6q7fOTX5pmAW.py

import random
import simplegui
import math

#initialize globals
guess = 0 
num_range = 100
secret_number = random.randrange(1, num_range)
n_guesses = 7

# helper function to start and restart the game
def new_game():
    global guess, num_range, secret_number, n_guesses
    secret_number = random.randrange(1, num_range)
    if num_range == 100:
        n_guesses = 7
    elif num_range == 1000:
        n_guesses = 10
    return secret_number, n_guesses
 
# define event handlers for control panel
def range100():
    # Changes the range to [0,100) and starts a new game 
    global num_range, secret_number, n_guesses
    num_range = 100
    n_guesses = 7
    secret_number = random.randrange(0, num_range)
    return secret_number
       
def range1000():
    # Changes the range to [0,1000) and starts a new game     
    global num_range, secret_number, n_guesses
    num_range = 1000
    n_guesses = 10
    secret_number = random.randrange(0, num_range)
    return secret_number
        
def input_guess(inp):
    #Compare input with secret number for allowed number of guesses
    global guess, num_range, secret_number, n_guesses
    guess = int(inp)
    print "Guess was "+ str(guess)
    if guess == secret_number:
        print "Correct! \n"
        new_game()
    elif n_guesses > 1 and guess < secret_number:
        print "Guess higher"
        n_guesses = n_guesses - 1
        print "Guesses remaining: " + str(n_guesses) +" \n"
    elif n_guesses > 1 and guess > secret_number:
        print "Guess lower"
        n_guesses = n_guesses - 1
        print "Guesses remaining: " + str(n_guesses) + " \n"
    elif n_guesses == 1 and guess != secret_number:
        print "You ran out of guesses! The number was "+ str(secret_number) +". Try again. \n \n"
        new_game()
    
# create frame
frame = simplegui.create_frame("Guess the Number", 300, 300)

# register event handlers for control elements and start frame
frame.add_button("Set number range 0-100", range100)
frame.add_button("Set number range 0-1000", range1000)
frame.add_input("Guess a number", input_guess, 50) 
frame.start()


# call new_game 
new_game()





