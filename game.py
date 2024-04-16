#import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt

#pygame.init()
#font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20 # Tamaño de un bloque en px
SPEED = 20

class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        #self.display = pygame.display.set_mode((self.w, self.h))
        #pygame.display.set_caption('Snake')
        #self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, action):
        # Aumentamos en 1 el numero de pasos
        self.frame_iteration += 1

        # 1. collect user input
        #for event in pygame.event.get():
            #if event.type == pygame.QUIT:
                #pygame.quit()
                #quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0 
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            reward = -10
            game_over = True
            return reward, game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        #self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score
    
    # Return True si hay colisión, False en caso contrario
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head

        # choque con pared
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        
        # choque consigo misma
        if pt in self.snake[1:]:
            return True
        
        return False
    
    def _update_ui(self):
        fig, ax = plt.subplots()
        
        # Borra cualquier contenido previo
        ax.clear()
        
        # Dibuja el fondo negro
        ax.set_facecolor('black')
        
        # Dibuja la serpiente
        for pt in self.snake:
            ax.add_patch(plt.Rectangle((pt.x, pt.y), 20, 20, color='blue'))
            ax.add_patch(plt.Rectangle((pt.x + 4, pt.y + 4), 12, 12, color='lightblue'))
        
        # Dibuja la comida
        ax.add_patch(plt.Rectangle((self.food.x, self.food.y), 20, 20, color='red'))
        
        # Configura el texto del puntaje
        ax.text(0, 0, "Score: " + str(self.score), color='white')
        
        # Configura los límites de la figura para que coincidan con el tamaño de la pantalla
        #ax.set_xlim([0, SCREEN_WIDTH])
        #ax.set_ylim([0, SCREEN_HEIGHT])
        
        # Retorna la figura
        return fig


    #def _update_ui(self):
    #   pass
    #    self.display.fill(BLACK)
        
        #for pt in self.snake:
            #pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            #pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        #pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        #text = font.render("Score: " + str(self.score), True, WHITE)
        #self.display.blit(text, [0, 0])
        #pygame.display.flip()
        
    # Partiendo de action, se determina el siguiente movimiento 
    # [1,0,0] -> Recto || [0,1,0] -> Giro derecha || [0,0,1] -> Giro izquierda
    def _move(self, action):

        segun_orden_reloj = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = segun_orden_reloj.index(self.direction) # Sacamos el indice actual segun la dirección actual

        # action = [recto, derecha, izquierda]
        if np.array_equal(action, [1,0,0]):
            new_dir = segun_orden_reloj[idx] # Sigue misma dirección
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx + 1) % 4
            new_dir = segun_orden_reloj[next_idx] # Giro derecha
        else:
            next_idx = (idx - 1) % 4
            new_dir = segun_orden_reloj[next_idx] # Giro izquierda

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            