# Week 8 Mini-Project: RiceRocks/Asteroids

# Originally written in CodeSkulptor, saved at
# http://www.codeskulptor.org/#user40_fHyxmYpChNnotgw.py

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
thrust = False
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 75)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

#process sprite group
def process_sprite_group(sprite_group, canvas):
    for sprite in set(sprite_group):
        sprite.draw(canvas)
        sprite.update()
        if sprite.update():
            sprite_group.remove(sprite)

#helper function to determine group collisions        
def group_collide(group, other_object):
    global explosion_group
    for i in set(group):
        if i.collide(other_object):
            group.remove(i)
            new_explosion = Sprite(i.pos, [0, 0], 0, 0, explosion_image, explosion_info) 
            explosion_group.add(new_explosion)
            explosion_sound.play()
            return True

#helper function to determine group-group collisions
def group_group_collide(group1, group2):
    num = 0
    for j in set(group1):
        if group_collide(group2, j):
            group1.remove(j)
            num += 1 
    return num 
         
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
               
    def draw(self,canvas):
        if thrust:
            canvas.draw_image(self.image, (self.image_center[0] + self.image_size[0], self.image_center[1]),
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, 
                              self.image_size, self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        self.vector = angle_to_vector(self.angle)
        friction = [0, 0]
        friction[0] = -0.01 * self.vel[0]
        friction[1] = -0.01 * self.vel[1]
        
        #accelerate ship if thrusters firing; have friction decelerate if not
        if thrust:
            self.vel[0] += 0.1 * self.vector[0]
            self.vel[1] += 0.1 * self.vector[1]
        else:
            self.vel[0] += friction[0]
            self.vel[1] += friction[1]
        
        #wrap ship around if it reaches edge of canvas    
        if self.pos[0] < 0:
            self.pos[0] = WIDTH - 1
        elif self.pos[0] > WIDTH:
            self.pos[0] = 1
        if self.pos[1] < 0:
            self.pos[1] = HEIGHT - 1
        elif self.pos[1] > HEIGHT:
            self.pos[1] = 0
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def thrusters(self, thrust):
        if thrust:
            ship_thrust_sound.play()
    
    def shoot(self):
        global missile_group
        a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
        a_missile.pos[0] = self.pos[0] + math.cos(self.angle) * self.radius
        a_missile.pos[1] = self.pos[1] + math.sin(self.angle) * self.radius
        a_missile.vel[0] = self.vel[0] + 4 * math.cos(self.angle)
        a_missile.vel[1] = self.vel[1] + 4 * math.sin(self.angle)
        missile_sound.play()
        missile_group.add(a_missile)
        return missile_group
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        global time
        if not self.animated:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        elif self.animated:
            current_center = [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, current_center, self.image_size, self.pos, self.image_size, self.angle)
                              
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel        
        self.age += 1
           
        #wrap sprite
        if self.pos[0] < 0:
            self.pos[0] = WIDTH - 1
        elif self.pos[0]  > WIDTH:
            self.pos[0] = 1
        if self.pos[1] < 0:
            self.pos[1] = HEIGHT - 1
        elif self.pos[1] > HEIGHT:
            self.pos[1] = 0   
        
        #determine if sprite is younger than lifespan
        if self.age < self.lifespan:
            return False
        elif self.age >= self.lifespan:
            return True  
            
    def collide(self, other_object):
        if self.get_radius() + other_object.get_radius() >= dist(self.get_position(), other_object.get_position()):
            return True
        else:
            return False
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius    

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, rock_group, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True  
        lives = 3
        score = 0
        soundtrack.rewind()
        soundtrack.play()
        rock_group = set([])
        missile_group = set([])

def draw(canvas):
    global time, lives, score, explosion_group, rock_group, my_ship, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw explosions, ship, and sprites
    my_ship.draw(canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # update ship and sprites
    my_ship.update()
        
    #test for ship collision with asteroids
    if group_collide(rock_group, my_ship):
        lives -= 1 
    
    #test for missile collisions with asteroids
    if group_group_collide(rock_group, missile_group):
        score += 10
    
    # draw lives and score
    canvas.draw_text("Lives: " + str(lives), (WIDTH * .2, 40), 30, "White", "sans-serif")
    canvas.draw_text("Score: " + str(score), (WIDTH * .7, 40), 30, "White", "sans-serif")
    
    if lives == 0:
        rock_group = ([])
        started = False
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    if len(rock_group) < 12 and started:
        a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.01, asteroid_image, asteroid_info)
        a_rock.vel[0] = random.randrange(-2, 2)
        a_rock.vel[1] = random.randrange(-2, 2)
        a_rock.ang = random.randrange(-1, 1)
        a_rock.ang_vel = random.randrange(0, 2)
        a_rock.pos[0] = random.randrange(0, WIDTH)
        a_rock.pos[1] = random.randrange(0, HEIGHT)
        if dist(a_rock.pos, my_ship.get_position()) > 2 * my_ship.get_radius():
            rock_group.add(a_rock)
    return rock_group

# keyup and keydown handlers
def ship_controls_keydown(key):
    global my_ship, thrust
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = -0.15
        my_ship.update()
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0.15
        my_ship.update()
    if key == simplegui.KEY_MAP["up"]:
        thrust = True
        my_ship.thrusters(thrust)
        my_ship.update()
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        
        
def ship_controls_keyup(key):
    global my_ship, thrust
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:	
        my_ship.angle_vel = 0
        my_ship.update()
    if key == simplegui.KEY_MAP["up"]:
        thrust = False
        ship_thrust_sound.rewind()
        my_ship.update()
    if key == simplegui.KEY_MAP["space"]:
        missile_sound.rewind()
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(ship_controls_keydown)
frame.set_keyup_handler(ship_controls_keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
