from Bot import BasicBot
from Game import Game
import numpy as np #np.ndarray.flatten(np.array(board))
from collections import deque
import random as rd

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

class DQNAgent(BasicBot):
	
    def create_model(self):
        model = Sequential()

        model.add(Dense(128, activation='relu', input_shape=(42,)))
        model.add(Dropout(0.2))

        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.2))

        model.add(Dense(Game.nb_cols, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.LEARNING_RATE), metrics=['acc'])

        return model



    def __init__(self, turn, DISCOUNT_FACTOR=0.9, LEARNING_RATE=0.1, MEMORY_SIZE=50_000, MIN_MEMORY_SIZE=1_000, BATCH_SIZE=64, UPDATE_TARGET_INTERVAL=5):
        super().__init__(turn)
        self.DISCOUNT_FACTOR    = DISCOUNT_FACTOR
        self.LEARNING_RATE      = LEARNING_RATE

        # Main model
        self.model = self.create_model()

        # Target model
        self.target_model       = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        self.memory             = deque(maxlen=MEMORY_SIZE)
        self.MIN_MEMORY_SIZE    = MIN_MEMORY_SIZE
        self.MEMORY_SIZE        = MEMORY_SIZE
        self.BATCH_SIZE         = BATCH_SIZE
        self.UPDATE_TARGET_INTERVAL = UPDATE_TARGET_INTERVAL

        self.target_update_counter = 0


    def add_to_memory(self, transition):
        # transition is tuple (flattened_current_state, action, reward, flattened_next_state, done)
        self.memory.append(transition)

    def get_qs(self, flattened_board):
        flattened_board = np.reshape(flattened_board, (1, 42))
        return self.model.predict(flattened_board)

    
    def train(self, terminal_state, step):
        if len(self.memory) < self.MIN_MEMORY_SIZE:
            return

        training_batch  = rd.sample(self.memory, self.BATCH_SIZE)
        # transition is tuple (flattened_current_state, action, reward, flattened_next_state, done)
        current_states  = np.array([transition[0] for transition in training_batch])
        current_states  = np.reshape(current_states, (self.BATCH_SIZE, 42))
        current_qs_list = self.model.predict(current_states)

        future_states   = np.array([transition[3] for transition in training_batch])
        future_states  = np.reshape(future_states, (self.BATCH_SIZE, 42))
        future_qs_list  = self.target_model.predict(future_states)

        X, y = [], []

        for index, (current_state, action, reward, future_state, done) in enumerate(training_batch):
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + self.DISCOUNT_FACTOR * max_future_q
            else:
                new_q = reward

            # Update Q value for given state
            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            # And append to our training data
            X.append(current_state)
            y.append(current_qs)

        X  = np.reshape(X, (self.BATCH_SIZE, 42))
        self.model.fit(np.array(X), np.array(y), batch_size=self.BATCH_SIZE, verbose=0, shuffle=False)
        
        if terminal_state:
            self.target_update_counter += 1

        if self.target_update_counter > self.UPDATE_TARGET_INTERVAL:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0



    def make_move(self, board):
        board = np.array(board)
        state = np.ndarray.flatten(board)
        return np.argmax(self.get_qs(state))
