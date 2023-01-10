import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple
pygame.init()
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
Point = namedtuple('Point', 'x, y')
SIZE_OF_BLOCK = 20
font = pygame.font.Font('ComicMono.ttf', 25)
class SnakeGameApplication:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.SPEED = 5
        
        #Display Game Screen:
        self.screen_color = (60,85,67)
        self.snake_color1 = (120,140,180)
        self.snake_color2 = (201,230,210)
        self.food_color = (255,255,255)
        
        self.display = pygame.display.set_mode(size = (self.width, self.height))
        pygame.display.set_caption('Snake Game!')
        self.clock = pygame.time.Clock()
        
        #Game State:
        self.direction = Direction.RIGHT
        self.head = Point(self.width/2, self.height/2) #coordinated of head
        self.snake_body = [self.head, Point(self.head.x-(SIZE_OF_BLOCK), self.head.y),
                          Point(self.head.x-2*(SIZE_OF_BLOCK), self.head.y)]
        self.score = 0
        self.food = None
        self.place_food()
        self.initial_game_ui()

    def initial_game_ui(self):
        
        screen_color = self.screen_color
        snake_color1 = self.snake_color1
        snake_color2 = self.snake_color2
        food_color = self.food_color

        
        #Screen:
        self.display.fill(screen_color)
        
        
        #Snake:
        for i in self.snake_body:
            pygame.draw.rect(self.display, snake_color1, [i.x, i.y, SIZE_OF_BLOCK, SIZE_OF_BLOCK], 0)
            pygame.draw.rect(self.display, snake_color2, [i.x, i.y, 20, 20], 0)
            
        #Food:
        pygame.draw.rect(self.display, food_color, [self.food.x, self.food.y, SIZE_OF_BLOCK, SIZE_OF_BLOCK], 4)
        
        #Score:
        text = font.render("SCORE: " + str(self.score), True, snake_color1)
        self.display.blit(text, (0,0))
        pygame.display.flip()
        
        
        
    def place_food(self):
        x = random.randint(0, (self.width - SIZE_OF_BLOCK)//SIZE_OF_BLOCK) * SIZE_OF_BLOCK
        y = random.randint(0, (self.height - SIZE_OF_BLOCK)//SIZE_OF_BLOCK) * SIZE_OF_BLOCK
        self.food = Point(x,y)
        if self.food in self.snake_body:
            self.place_food()
            
    
        
    def update_game_ui(self):
        self.screen_color = tuple(np.random.choice(range(0,95), size=3))
        self.snake_color1 = tuple(np.random.choice(range(96,195), size=3))
        self.snake_color2 = tuple(np.random.choice(range(196,240), size=3))
        self.food_color = tuple(np.random.choice(range(241,255), size=3))
        
        screen_color = self.screen_color
        snake_color1 = self.snake_color1
        snake_color2 = self.snake_color2
        food_color = self.food_color
        
        #Screen:
        self.display.fill(screen_color)
        
        
        #Snake:
        for i in self.snake_body:
            pygame.draw.rect(self.display, snake_color1, [i.x, i.y, SIZE_OF_BLOCK, SIZE_OF_BLOCK], 0)
            pygame.draw.rect(self.display, snake_color2, [i.x, i.y, 20, 20], 0)
            
        #Food:
        pygame.draw.rect(self.display, food_color, [self.food.x, self.food.y, SIZE_OF_BLOCK, SIZE_OF_BLOCK], 4)
        
        #Score:
        text = font.render("SCORE: " + str(self.score), True, snake_color1)
        self.display.blit(text, (0,0))
        pygame.display.flip()
        
    
    def move(self,direction):
        x = self.head.x
        y = self.head.y
        
        if direction == Direction.RIGHT:
            x += SIZE_OF_BLOCK

        elif direction == Direction.LEFT:
            x -= SIZE_OF_BLOCK
            
        elif direction == Direction.DOWN:
            y += SIZE_OF_BLOCK

        elif direction == Direction.UP:
            y -= SIZE_OF_BLOCK
        
        self.head = Point(x,y)
        
    def collision(self):
        if self.head.x > self.width - SIZE_OF_BLOCK or self.head.x < 0 or self.head.y > self.height - SIZE_OF_BLOCK or self.head.y < 0:
            return True
        
        if self.head in self.snake_body[1:]:
            return True
        
        return False
            
        
            
        
    def step_of_game(self):
        #Step 1: Input of user (what key is pressed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
                    
        #Step 2: Just Move
        self.move(self.direction)
        self.snake_body.insert(0, self.head)
        
        #Step 3: Condition of game over
        game_over = False
        if self.collision():
            game_over = True
            return game_over, self.score
        
        #Step 4:Place food / just move
        if self.head == self.food:
            self.score += 1
            self.SPEED += 1
            self.place_food()
            self.update_game_ui()
        else:
            self.initial_game_ui()
            
            self.snake_body.pop()
            
            
        #Step 5: UI is updated
        
        self.clock.tick(self.SPEED)
        
        #Step 6: Game over and score
        game_over = False
        return game_over, self.score
        
        
if __name__ == '__main__':
    snakeGame = SnakeGameApplication(640,480)
    
    while True:
        game_over, score = snakeGame.step_of_game()
        if game_over == True:
            break
        
    pygame.quit()        