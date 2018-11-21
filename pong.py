# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 100
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
    
# spawns a ball in middle of table, moving up and left if LEFT, else up and right.
def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    if direction == LEFT:
        ball_vel[0] = -random.randrange(3, 8)
        ball_vel[1] = -random.randrange(2, 5)
        return
    elif direction == RIGHT:
        ball_vel[0] = random.randrange(3, 8)
        ball_vel[1] = -random.randrange(2, 5)
        return
    return

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball(LEFT)
    #add code to make it go towards the point-scorer's gutter
    pass

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
        #bounce ball off top and bottom walls
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        return
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        return
    pass

    # draw ball
    canvas.draw_circle([ball_pos[0], ball_pos[1]], BALL_RADIUS, 1, "White", "White")
            
    # update paddle's vertical position, keep paddle on the screen
    if ((paddle1_pos + paddle1_vel) > HALF_PAD_HEIGHT) and ((paddle1_pos + paddle1_vel + HALF_PAD_HEIGHT) < HEIGHT):
        paddle1_pos += paddle1_vel
    if ((paddle2_pos + paddle2_vel) > HALF_PAD_HEIGHT) and ((paddle2_pos + paddle2_vel + HALF_PAD_HEIGHT) < HEIGHT):
        paddle2_pos += paddle2_vel
    pass

    # draw paddles
    canvas.draw_polygon(([0, paddle1_pos - HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], [0, paddle1_pos + HALF_PAD_HEIGHT]), 1, "Blue", "Blue")
    canvas.draw_polygon(([WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]),  1, "Blue", "Blue")
    
    # determine whether paddle and ball collide
    if (ball_pos[0] - BALL_RADIUS <= PAD_WIDTH) and ((ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT) and (ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT)):
        ball_vel[0] = -ball_vel[0] * 1.1
    if (ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH) and ((ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT) and (ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT)):
        ball_vel[0] = -ball_vel[0] * 1.1
        #add point to opposite player
    elif (ball_pos[0] - BALL_RADIUS <= PAD_WIDTH) and not ((ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT) and (ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT)):
        score2 += 1
        spawn_ball(RIGHT)
    elif (ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH) and not ((ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT) and (ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT)):
        score1 += 1
        spawn_ball(LEFT)
    
    # draw scores
    canvas.draw_text(str(score1), [150, 50], 50, "Fuchsia")
    canvas.draw_text(str(score2), [450, 50], 50, "Fuchsia")
    return
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['W']:
        paddle1_vel += -5
        return
    elif key == simplegui.KEY_MAP['S']:
        paddle1_vel += 5
        return
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel += -5
        return
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel += 5
        return
    return

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['W']:
        paddle1_vel = 0
        return
    elif key == simplegui.KEY_MAP['S']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
        return
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
        return
    return

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("New Game", new_game)

# start frame
new_game()
frame.start()
