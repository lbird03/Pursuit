import pygame
from pygame.locals import *
import time
import random

#Top Possible Score = 320
# size of snake unit/grid unit
SIZE = 50
BACKGRND_COL = (16,115,235)

class Food:
    def __init__(self, parent_screen):
        self.image = pygame.image.load('food.png')
        self.parent_screen = parent_screen
        self.x = 150
        self.y = 150

    # draws food based on position
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    # moves food to random location inside of boundaries
    def move(self):
        self.x = random.randint(0,19)*SIZE
        self.y = random.randint(0,15)*SIZE

class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        self.block = pygame.image.load("block.png")
        self.y = [SIZE]*length
        self.x = [SIZE]*length
        self.direction = "right"

    # adds 1 to snake length
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    # draws snake on screen based on current position
    def draw(self):
        self.parent_screen.fill(BACKGRND_COL)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.direction == 'left':
            self.x[0] -= 50
        if self.direction == 'right':
            self.x[0] += 50
        if self.direction == 'up':
            self.y[0] -= 50
        if self.direction == 'down':
            self.y[0] += 50
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill(BACKGRND_COL)
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.food = Food(self.surface)
        self.food.draw()

    # takes location of food and snake head and returns true upon collision
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    # updates screen (food location, snake location, score)
    def play(self):
        self.snake.walk()
        self.food.draw()
        self.display_score()
        pygame.display.flip()

        # snake collision with food
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.snake.increase_length()
            self.food.move()

        #snake collision with self
        for i in range(2,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision Occured"
            else: pass

    #
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800,10))

    def show_game_over(self):
        self.surface.fill(BACKGRND_COL)
        font = pygame.font.SysFont('arial',30)
        msg = font.render(f"Game over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(msg, (200,300))
        msg2 = font.render("To play again press enter. To exit, press Esc", True, (255, 255, 255))
        self.surface.blit(msg2, (200, 350))

        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.food = Food(self.surface)
    # defines movement, button actions, and snake speed
    # constantly happening loop
    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
                
                if self.snake.x[0] >= 1000 or self.snake.x[0] < 0 or self.snake.y[0] >= 800 or self.snake.y[0] < 0:
                    self.show_game_over()
                    pause = True
                    self.reset()
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.1)


    
# main
if __name__ == "__main__":
    game = Game()
    game.run()
    
    