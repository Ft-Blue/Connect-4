from RLAgent import DQNAgent
from Bot import OneStepBot

from Game import Game
from Interface import Interface

import random as rd
import numpy as np
from tqdm import tqdm

DISCOUNT = 0.99
LEARNING_RATE = 0.01
UPDATE_TARGET_EVERY = 5  # Terminal states (end of episodes)
SHOW_EVERY = 100
#MEMORY_FRACTION = 0.20

# Environment settings
EPISODES = 50
ep_rewards = []

# Exploration settings
epsilon = 1  # not a constant, going to be decayed
EPSILON_DECAY = 0.99975
MIN_EPSILON = 0.001


alice = OneStepBot(1, 1)
bob = DQNAgent(-1, DISCOUNT, LEARNING_RATE)
MARGIN			= 20
RADIUS			= 35
interface		= Interface(margin=MARGIN, radius=RADIUS)

# Iterate over episodes
for episode in tqdm(range(1, EPISODES + 1), ascii=True, unit='episodes'):
    # Restarting episode - reset episode reward and step number
    episode_reward = 0
    game = Game()
    current_state = np.reshape(np.ndarray.flatten(np.array(game.board)), (1, 42))
    step = 1

    # Reset flag and start iterating until episode ends
    done = False
    while not done:
        if game.player_turn == bob.turn:
            # This part stays mostly the same, the change is to query a model for Q values
            if np.random.random() > epsilon:
                # Get action from Q table
                action = bob.make_move(game.board)
                if action not in game.free_columns:
                    action = rd.choice(game.free_columns)
            else:
                # Get random action
                action = rd.choice(game.free_columns)
        elif game.player_turn == alice.turn:
            action = alice.make_move(game.board)

        game.place_piece(action)
        new_state = np.reshape(np.ndarray.flatten(np.array(game.board)), (1, 42))
        done = game.gameover
        if done:
            if game.winner == bob.turn: reward = 1
            elif game.winner == alice.turn: reward = -1
            else: reward = 0
        else:
            reward = -0.5

        

        # Transform new continous state to new discrete state and count reward
        episode_reward += reward

        if (episode-1)%SHOW_EVERY == 0:
            interface.draw(game.board)

        # Every step we update replay memory and train main network
        bob.add_to_memory((current_state, action, reward, new_state, done))
        bob.train(done, step)

        current_state = new_state
        step += 1
        game.next_player()
        


    # Append episode reward to a list and log stats (every given number of episodes)
    ep_rewards.append(episode_reward)

    # Decay epsilon
    if epsilon > MIN_EPSILON:
        epsilon *= EPSILON_DECAY
        epsilon = max(MIN_EPSILON, epsilon)
    bob.model.save(f'./bob.model')