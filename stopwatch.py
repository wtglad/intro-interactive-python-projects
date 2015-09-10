# "Stopwatch: The Game"

# Originally written in CodeSkulptor, saved at
# http://www.codeskulptor.org/#user40_CzXZU6JxSE8D6Zk.py

import simplegui


# define global variables
time = 0
stop_count = 0
win_count = 0


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    minute = t // 600
    sec_1 = (t % 600) // 100
    sec_2 = (t % 100) // 10
    tenth_sec = t % 10
    formatted = str(minute) + ":" + str(sec_1) + str(sec_2) + "." + str(tenth_sec)
    return formatted
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()

def stop():
    global stop_count, win_count, time
    if timer.is_running() == True:
        stop_count = stop_count + 1
        timer.stop()
        if time % 10 == 0:
            win_count = win_count + 1
    return stop_count, win_count

def reset():
    global time, stop_count, win_count
    time = 0
    stop_count = 0
    win_count = 0
    return time, stop_count, win_count

# define event handler for timer with 0.1 sec interval
def time_handler():
    global time
    time = time + 1 
    return time

# define draw handler
def text_handler(canvas):
    global time
    canvas.draw_text(str(format(time)), [120,150], 36, "White") 
    canvas.draw_text(str(win_count) + " / " + str(stop_count), [240, 30], 24, "Green")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 300)

# register event handlers
frame.set_draw_handler(text_handler)
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset) 
timer = simplegui.create_timer(100, time_handler)

# start frame
frame.start()




