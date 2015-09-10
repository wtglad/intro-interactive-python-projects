# Implementation of classic arcade game Pong

# Originally written in CodeSkulptor, saved at
# http://www.codeskulptor.org/#user40_e3aTMyqCgqqHjfk.py

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

paddle1_pos = [1, HEIGHT / 2]
paddle2_pos = [WIDTH - 1, HEIGHT/2]
paddle1_vel = [0, 0]
paddle2_vel = [0,0]


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    if direction == "left":
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        ball_vel = [-random.randrange(2, 4), -random.randrange(1, 3)]   
    
    elif direction == "right":
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        ball_vel = [random.randrange(2, 4), -random.randrange(1, 3)]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints 
    spawn_ball("right")
    score1 = 0
    score2 = 0
    
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, init_pos, BALL_RADIUS, WIDTH, HEIGHT
      
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #bounce and respawn functions
    if ball_pos[1] >= (HEIGHT- BALL_RADIUS - 1):
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    if ball_pos[0] <= PAD_WIDTH - 1:
        spawn_ball("right")
        score2 = score2 + 1
    elif ball_pos[0] >= WIDTH - PAD_WIDTH:
        spawn_ball("left")
        score1 = score1 + 1
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
 
    # update paddle's vertical position, keep paddle on the screen
    #update paddle 1
    if paddle1_pos[1] - HALF_PAD_HEIGHT > 0 and paddle1_pos[1] + HALF_PAD_HEIGHT < HEIGHT - 1:
        paddle1_pos[1] += paddle1_vel[1]
    
    #update paddle 2
    if paddle2_pos[1] - HALF_PAD_HEIGHT > 0 and paddle2_pos[1] + HALF_PAD_HEIGHT < HEIGHT - 1:
        paddle2_pos[1] += paddle2_vel[1]
    
    # draw paddles
    canvas.draw_line([paddle1_pos[0], paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0], paddle1_pos[1] + HALF_PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line([paddle2_pos[0], paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0], paddle2_pos[1] + HALF_PAD_HEIGHT], PAD_WIDTH, "White")
    
    # determine whether paddle and ball collide    
    if ball_pos[0] - BALL_RADIUS < PAD_WIDTH and (paddle1_pos[1] - HALF_PAD_HEIGHT) <  ball_pos[1]  < (paddle1_pos[1] + HALF_PAD_HEIGHT):
        ball_vel[0] = 1.1 * -ball_vel[0]
    if ball_pos[0] + BALL_RADIUS > WIDTH - 1 - PAD_WIDTH and (paddle2_pos[1] - HALF_PAD_HEIGHT) <  ball_pos[1] < (paddle2_pos[1] + HALF_PAD_HEIGHT):
        ball_vel[0] = 1.1 * -ball_vel[0]
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/4, HEIGHT/8], 24, "White")
    canvas.draw_text(str(score2), [.75 * WIDTH, HEIGHT/8], 24, "White")

    
def keydown(key):
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"] and paddle1_pos[1] - HALF_PAD_HEIGHT > 0:
        paddle1_vel = [0, -5]
        paddle1_pos[1] += paddle1_vel[1]
    elif key == simplegui.KEY_MAP["s"] and paddle1_pos[1] + HALF_PAD_HEIGHT < HEIGHT - 1:
        paddle1_vel = [0, 5]
        paddle1_pos[1] += paddle1_vel[1]
    elif key == simplegui.KEY_MAP["up"] and paddle2_pos[1] - HALF_PAD_HEIGHT > 0:
        paddle2_vel = [0, -5]
        paddle2_pos[1] += paddle2_vel[1]
    elif key == simplegui.KEY_MAP["down"] and paddle2_pos[1] + HALF_PAD_HEIGHT < HEIGHT - 1:
        paddle2_vel = [0, 5]
        paddle2_pos[1] += paddle2_vel[1]
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0] 

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
reset = frame.add_button("Reset", new_game, 50)

# start frame
new_game()
frame.start()



