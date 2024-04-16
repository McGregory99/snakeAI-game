import torch
import random
import numpy as np
from collections import deque # Para almacenar memoria para nuestro agente
import matplotlib.pyplot as plt

from game import SnakeGameAI, Direction, Point, BLOCK_SIZE
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001 # LEARNING RATE

class Agent:

    def __init__(self):
        self.num_games = 0
        self.epsilon = 0 # para controlar la aleatoriedad
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # Si sobrepasamos la memoria, se eliminan los más antiguos
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    # state(11 valores): [peligro recto, peligro derecha, peligro izquierda
    #                     dir izquierda, dir derecha, dir arriba, dir abajo
    #                     comida izquierda, comida derecha, comida arriba, comida abajo]
    def get_state(self, game):
        head = game.snake[0]
        # La siguiente celda en cada dirección
        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)
        # La dirección actual de la serpiente
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Check peligro arriba
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Check peligro derecha
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Check peligro izqueirda
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
        
            # Dirección de movimiento
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Comida dirección
            game.food.x < game.head.x, # Comida izquierda
            game.food.x > game.head.x, # Comida derecha
            game.food.y > game.head.y, # Comida arriba
            game.food.y > game.head.y # Comida abajo
        ]
        
        return np.array(state, dtype=int) # con dtype convertimos de True/False a 0/1

    # Almacenamos como un único elemento toda la información. Un elemento de la tupla
    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    # para el entrenamiento basado en una gran cantidad de movimientos
    def train_long_memory(self):

        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # nos devuelve una lista de tuplas
        else:
            mini_sample = self.memory

        # Ponemos juntos todos los states, actions, rewards... (otra opcion es hacer un loop e ir agregando pero el zip es más elegante)
        states, actions, rewards, next_states, games_over = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, games_over)

    # para el entrenamiento de un unico cambio de estado
    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        # A medida que se va jugando, epsilon es más pequeño
        self.epsilon = 80 - self.num_games
        final_move = [0,0,0]
        # Cuando más pequeño sea epsilon más baja será la posibilidad de que se cumpla este if
        if random.randint(0, 200) < self.epsilon:
            idx = random.randint(0,2)
            final_move[idx] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0) 
            # es posible que prediction sea por ej [5.2, 3.4, 1.1] asi que lo convertimos a nuestro formato
            idx = torch.argmax(prediction).item()
            final_move[idx] = 1
        
        return final_move
    

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record_score = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # get the current state
        state_old = agent.get_state(game)

        # get move based on the current state
        final_move = agent.get_action(state_old)

        # hacer el movimiento y obtener nuevo estado
        reward, game_over, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            # train long memory and plot result
            game.reset()
            agent.num_games += 1
            agent.train_long_memory()

            if score > record_score:
                record_score = score
                agent.model.save()
            
            print(f"\n\nGame {agent.num_games} \nScore {score} \nRecord {record_score}")
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score/agent.num_games
            plot_mean_scores.append(mean_score)
            if agent.num_games%50==0:
                print("IMAGE SAVED")
                plot(plot_scores, plot_mean_scores, agent.num_games)


if __name__ == '__main__':
    train()
