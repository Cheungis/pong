# Pong
# version 3
# this program does the following:
# Create window
# Create game
# Play game
# End game

from uagame import Window
import pygame, time
from pygame.locals import *

# main algorithm
def main():
    # create window
    window_width = 500
    window_height = 400
    window_title = 'Pong'
    window = Window(window_title, window_width, window_height)
    
    # create game object
    game = Game(window)
    
    # play the game
    game.play()
    
    # close the window
    window.close()

# user defined classes
class Game:
    # handles general gameplay
    # initializer
    def __init__(self, window):
        pygame.key.set_repeat(20, 20)
        self.score = [0,0]
        self.max_score = 10
        self.window = window
        self.close_clicked = False
        self.continue_game = True
        self.pause_time = 0.01
        self.surface = window.get_surface()
        window.set_auto_update(False)
        center_ball = [250,200]
        radius_ball = 5
        velocity_ball = [2,1]
        color_ball = pygame.Color('white')
        surface_ball = window.get_surface()
        paddle_colour = pygame.Color('white')
        left_paddle_dimension = [100,175,10,50]
        right_paddle_dimension = [self.window.get_width() - 100,175,10,50] 
        #left_paddle 
        self.left_paddle = Paddle(self.surface,paddle_colour,left_paddle_dimension)
        #right_paddle
        self.right_paddle = Paddle(self.surface,paddle_colour,right_paddle_dimension)
        #ball
        self.ball = Ball(surface_ball,color_ball,center_ball,radius_ball,velocity_ball,self.left_paddle,self.right_paddle)
    # play game    
    def play(self):
        # play game until players hits exit box
        while not self.close_clicked:
            # play a frame
            self.handle_event()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
            time.sleep(self.pause_time)
      
    # handle event        
    def handle_event(self):
        # Handle one user event by changing the game state appropriately
        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
        if event.type == KEYDOWN:
            list_of_keys = pygame.key.get_pressed()
            if list_of_keys[K_q] == True:
                movement = 'up'
                self.left_paddle.move(movement)
                
            if list_of_keys[K_a] == True:
                movement = 'down'
                self.left_paddle.move(movement)
                
            if list_of_keys[K_p] == True:
                movement = 'up'
                self.right_paddle.move(movement)
                
            if list_of_keys[K_l] == True:
                movement = 'down'
                self.right_paddle.move(movement)
    # draw frame        
    def draw(self):
        # Draw all game objects
        self.window.clear()
        self.left_paddle.draw()
        self.right_paddle.draw()
        self.ball.draw()
        self.draw_score()
        self.window.update()
    # update game objects
    def update(self):
        # Update all game objects
        self.ball.move()
        if self.ball.edge_collision():
            if self.ball.velocity[0] > 0:
                self.score[1] += 1
            elif self.ball.velocity[0] < 0:
                self.score[0] += 1  
                        
    def draw_score(self):
        left_score = str(self.score[0])
        right_score = str(self.score[1])
        x = 0
        y = 0
        window_width = self.window.get_width()
        font_width = self.window.get_string_width(right_score)
        font_size = 60
        fg_colour = 'white'
        self.window.set_font_size(font_size)
        self.window.set_font_color(fg_colour)
        self.window.draw_string(left_score,x,y)
        self.window.draw_string(right_score,window_width - font_width,y)
        
    # decide if game should continue    
    def decide_continue(self):
        # Determine if game should continue
        if self.score[0] > self.max_score or self.score[1] > self.max_score:
            self.continue_game = False
    
class Ball:
    # handles ball movement and collision detection
    def __init__(self,surface,color,center,radius,velocity,left_paddle,right_paddle):
        self.surface = surface
        self.color = color
        self.center = center
        self.radius = radius
        self.velocity = velocity
        self.left_paddle = left_paddle
        self.right_paddle = right_paddle
    def draw(self):
        pygame.draw.circle(self.surface, self.color, self.center, self.radius)
        
    def move(self):
        size_of_surface = self.surface.get_size()
        for coord in range(2):
            self.center[coord] = (self.center[coord] + self.velocity[coord])%size_of_surface[coord]
            if self.center[coord] + self.radius >= size_of_surface[coord] or self.center[coord] - self.radius <= 0:
                self.velocity[coord] = -self.velocity[coord]
            if self.paddle_collision() == True:
                self.velocity[coord] = -self.velocity[coord]
    def edge_collision(self):
        window_width = self.surface.get_width()
        return self.center[0] + self.radius >= window_width or self.center[0] - self.radius <= 0 
    
    def paddle_collision(self):
        return (self.velocity[0] > 0 and self.right_paddle.collision(self.center)) or (self.velocity[0] < 0 and self.left_paddle.collision(self.center))
        
class Paddle:
    # handles paddle position
    def __init__(self, surface, paddle_colour, paddle_dimension):
        self.surface = surface
        self.paddle_colour = paddle_colour
        self.paddle_dimension = paddle_dimension
        
    def draw(self):
        pygame.draw.rect(self.surface,self.paddle_colour,self.paddle_dimension)
    
    def collision(self, ball_center):
        rect = pygame.Rect(self.paddle_dimension[0],self.paddle_dimension[1],self.paddle_dimension[2],self.paddle_dimension[3])
        return rect.collidepoint(ball_center)
    
    def move(self, command):
        if command == 'up' and self.paddle_dimension[1] > 0:
            self.paddle_dimension[1] -= 5
        if command == 'down' and self.paddle_dimension[1] < self.surface.get_height() - self.paddle_dimension[3]:
            self.paddle_dimension[1] += 5

main()