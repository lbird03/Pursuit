import pygame
from pygame.locals import *
import time
import random

# size of snake unit/grid unit
SIZE = 50
BACKGRND_COL = (16,115,235)

# standard food activity
class Food:
    def __init__(self, parent_screen):
        self.image = pygame.image.load('Snake_game/food.png')
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

# Player Activity
class Player:
    def __init__(self, parent_screen):
        self.image = pygame.image.load('Snake_game/food.png')
        self.parent_screen = parent_screen
        self.direction = "right"
        self.x = 400
        self.y = 400
    
    # draw player
    def draw(self):
        # self.parent_screen.fill(BACKGRND_COL)
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'

    # teleport player to opposite side depending on which wall is hit
    def hit_limit(self):
        if self.x >= 1000:
            self.x = 0
        if self.x < 0:
            self.x = 1000
        if self.y >= 800:
            self.y = 0
        if self.y < 0:
            self.y = 800

    # keep player moving in current direction
    def walk(self):
        if self.direction == 'left':
            self.x -= 50
        if self.direction == 'right':
            self.x += 50
        if self.direction == 'up':
            self.y -= 50
        if self.direction == 'down':
            self.y += 50
        self.draw()


class Snake:
    def __init__(self, surface, length, x, y):
        self.length = length
        self.parent_screen = surface
        self.block = pygame.image.load("Snake_game/block.png")
        self.y = [x]*length
        self.x = [y]*length
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

    def pursue(self, targ_x, targ_y):

        x_dist = abs(targ_x - self.x[0])
        y_dist = abs(targ_y - self.y[0])

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.x[0] < targ_x and x_dist >= y_dist:
            self.x[0] += 50
        if self.x[0] > targ_x and x_dist >= y_dist:
            self.x[0] -= 50
        if self.y[0] < targ_y and x_dist < y_dist:
            self.y[0] += 50
        if self.y[0] > targ_y and x_dist < y_dist:
            self.y[0] -= 50
        self.draw()
        

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill(BACKGRND_COL)
        self.snake = Snake(self.surface, 2, 900, 700)
        self.snake.draw()
        # self.food = Food(self.surface)
        # self.food.draw()
        self.player = Player(self.surface)
        self.player.draw()
        self.score = 0
        

    # takes location of food and snake head and returns true upon collision
    def is_collision(self, x1, y1, x2, y2, x3, y3):
        # if x1 >= x2 and x1 < x2 + SIZE:
        #     if y1 >= y2 and y1 < y2 + SIZE:
        if x1 == x3 or x2 == x3:
            if y1 == y3 or y2 == y3:
                return True
        return False

    # updates screen (food location, snake location, score)
    def play(self):
        self.snake.pursue(self.player.x, self.player.y)
        self.player.walk()
        # self.food.draw()
        self.display_score()
        pygame.display.flip()

        # snake collision with player
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[1], self.snake.y[1], self.player.x, self.player.y):
            self.snake.increase_length()
            raise "Collision Occured"
            #  self.food.move()

        # snake collision with self
        for i in range(2,self.snake.length):
             if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                 raise Exception("Collision Occured")
             else: pass

    # displays current score in top right corner
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.surface.blit(score, (800,10))

    # display game over and final score
    def show_game_over(self):
        self.surface.fill(BACKGRND_COL)
        font = pygame.font.SysFont('arial',30)
        msg = font.render(f"Game over! Your score is {self.score}", True, (255, 255, 255))
        self.surface.blit(msg, (200,300))
        msg2 = font.render("To play again press Enter/Return. To exit, press Esc", True, (255, 255, 255))
        self.surface.blit(msg2, (200, 350))

        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 2, 900, 700)
        # self.food = Food(self.surface)
        self.player = Player(self.surface)
        self.score = 0

    # defines movement, button actions, and movement speed
    # constantly happening loop
    def run(self):
        
        running = True
        pause = False
        i = 0
        while running:
            i += 1
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # Escape Key
                    if event.key == K_ESCAPE:
                        running = False
                    
                    # Enter Key
                    if event.key == K_RETURN:
                        pause = False
                    
                    # Movement keys
                    if not pause:
                        if event.key == K_UP:
                            self.player.move_up()

                        if event.key == K_DOWN:
                            self.player.move_down()

                        if event.key == K_LEFT:
                            self.player.move_left()

                        if event.key == K_RIGHT:
                            self.player.move_right()

                # if player clicks X in corner
                elif event.type == QUIT:
                    running = False
                
            #if player runs into wall
            if self.player.x >= 1000 or self.player.x < 0 or self.player.y >= 800 or self.player.y < 0:
                self.player.hit_limit()

            # update actor positions if not game over
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            # increment score every second
            if i % 5 == 0:
                self.score += 1
            time.sleep(0.2)


    
# main
if __name__ == "__main__":
    game = Game()
    game.run()
    
    