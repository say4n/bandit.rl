from collections import defaultdict
import numpy as np
import random


class Agent:
    def __init__(self, arms=10, turns=1000):
        self.arms = arms
        self.turns = turns

    def play(self, game):
        raise NotImplementedError

    def __repr__(self):
        return "Abstract Base Class Agent"


class RandomAgent(Agent):
    def __init__(self, arms=10, turns=1000):
        super().__init__(arms, turns)

    def play(self, game):
        actions, rewards = [], []

        for turn in range(self.turns):
            action = np.random.choice(game.get_action_space())
            reward = game.step(action)

            actions.append(action)
            rewards.append(action)

        return actions, rewards

    def __repr__(self):
        return "Random Agent"


class GreedyAgent(Agent):
    def __init__(self, arms=10, turns=1000):
        super().__init__(arms, turns)

        self.action_value = np.random.normal(0, 1, arms)

    def play(self, game):
        actions, rewards = [], []

        action_tracker = defaultdict(int)
        reward_tracker = defaultdict(float)

        for turn in range(self.turns):
            action = np.argmax(self.action_value)
            reward = game.step(action)

            action_tracker[action] += 1
            reward_tracker[action] += reward

            self.action_value[action] = reward_tracker[action] / action_tracker[action]

            actions.append(action)
            rewards.append(action)

        return actions, rewards

    def get_action_values(self):
        return self.action_values

    def __repr__(self):
        return "Greedy Agent"


class EpsilonGreedyAgent(Agent):
    def __init__(self, epsilon=0.1, arms=10, turns=1000):
        super().__init__(arms, turns)

        self.action_value = np.random.normal(0, 1, arms)
        self.epsilon = epsilon

    def play(self, game):
        actions, rewards = [], []

        action_tracker = defaultdict(int)
        reward_tracker = defaultdict(float)

        for turn in range(self.turns):
            if random.random() < self.epsilon:
                # Take random action.
                action = np.random.choice(game.get_action_space())
                reward = game.step(action)
            else:
                # Take greedy action.
                action = np.argmax(self.action_value)
                reward = game.step(action)

            action_tracker[action] += 1
            reward_tracker[action] += reward

            self.action_value[action] = reward_tracker[action] / action_tracker[action]

            actions.append(action)
            rewards.append(action)

        return actions, rewards

    def get_action_values(self):
        return self.action_values

    def __repr__(self):
        return f"Epsilon-Greedy Agent ({self.epsilon})"