# implementation of card game - Memory

# Originally written in CodeSkulptor, saved at
# http://www.codeskulptor.org/#user40_6jxwCTs7lS6VRG0.py

import simplegui
import random

card_width = 50
card_height = 100
turns = 0 

# helper function to initialize globals
def new_game():
    global state, card_nums, card_index, exposed, turns, selected1, selected2
    state = 0
    card_nums = range(0, 8) * 2
    random.shuffle(card_nums)
    card_index = range(0, 16)
    exposed = [False] * 16 
    selected1 = 0
    selected2 = 0
    turns = 0
    label.set_text("Turns = " + str(turns))

# define event handlers    
def mouseclick(pos):
    global state, card_nums, selected1, selected2, turns
    selected_card = pos[0] / card_width
    if not exposed[selected_card]: 
        if state == 0: # no cards exposed
            selected1 = selected_card
            exposed[selected1] = True
            state = 1
        elif state == 1: # 1 card exposed and turn counter
            selected2 = selected_card
            exposed[selected2] = True
            state = 2
            turns = turns + 1
            label.set_text("Turns = " + str(turns))
        else: # 2 cards exposed, if equal keep them exposed, otherwise hide cards and flip new choice 
            if card_nums[selected1] != card_nums[selected2]:
                exposed[selected1], exposed[selected2] = False, False
                selected1 = selected2 = 0
            selected1 = selected_card
            exposed[selected1] = True
            state = 1  
            return turns

# test if card is exposed and draw number or card accordingly
def draw(canvas):
    global card_nums, exposed
    card_pos = 0
    for i in card_index:
        if exposed[i] == True:
                canvas.draw_text(str(card_nums[i]), (15 + (card_pos * card_width), 60),
                                 40, "Red")
        elif exposed[i] == False:
                canvas.draw_line((25 + (card_pos * card_width), 0),
                                (25 + (card_pos * card_width), card_height),
                                 49, "Green")
        card_pos = card_pos + 1

# create frame and add a button and labels        
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


