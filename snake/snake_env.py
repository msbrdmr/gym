import random
import time
import pygame
import gym
from gym import spaces
import numpy as np

WIDTH, HEIGHT = 630, 480
ROW, COLUMN = 30, 40
FPS = 30


def snake_generating(SnakeList, SnakeDir):
    if len(SnakeList) == 0:
        x = random.randrange(3, COLUMN - 1)
        y = random.randrange(3, ROW - 1)
        SnakeList.append([x, y])
        SnakeList.append(random.choice(
            [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]))
        x = SnakeList[-1][0]
        y = SnakeList[-1][1]
        temp = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
        temp.remove([SnakeList[0][0], SnakeList[0][1]])
        SnakeList.append(random.choice(temp))

    if len(SnakeDir) == 0:
        dir_list = ['right', 'left', 'up', 'down']
        if SnakeList[0][0] > SnakeList[1][0]:
            dir_list.remove('left')
        if SnakeList[0][1] > SnakeList[1][1]:
            dir_list.remove('up')
        if SnakeList[0][0] < SnakeList[1][0]:
            dir_list.remove('right')
        if SnakeList[0][1] < SnakeList[1][1]:
            dir_list.remove('down')
        SnakeDir = random.choice(dir_list)

    return SnakeList, SnakeDir


def apple_generating(SnakeList, ApplePos):
    if len(ApplePos) == 0:
        x = random.randrange(1, COLUMN + 1)
        y = random.randrange(1, ROW + 1)
        while [x, y] in SnakeList:
            x = random.randrange(1, COLUMN + 1)
            y = random.randrange(1, ROW + 1)
        ApplePos = [x, y]

    return ApplePos


def updating_snake(SnakeDir, SnakeList, SnakeEat, SnakeDead):
    if not SnakeDead:
        if not SnakeEat:
            SnakeList.pop(-1)
        else:
            SnakeEat = False

        if SnakeDir == 'up':
            SnakeList.insert(0, [SnakeList[0][0], SnakeList[0][1] - 1])
        if SnakeDir == 'down':
            SnakeList.insert(0, [SnakeList[0][0], SnakeList[0][1] + 1])
        if SnakeDir == 'right':
            SnakeList.insert(0, [SnakeList[0][0] + 1, SnakeList[0][1]])
        if SnakeDir == 'left':
            SnakeList.insert(0, [SnakeList[0][0] - 1, SnakeList[0][1]])

    return SnakeList, SnakeEat


def collision(SnakeList, ApplePos, SnakeDir, SnakeEat, SnakeDead, Score):
    if SnakeList[0] == ApplePos:
        SnakeEat = True
        Score += 1
        ApplePos = []

    if SnakeList[0][1] == 1 and SnakeDir == 'up':
        SnakeDead = True
    if SnakeList[0][1] == 30 and SnakeDir == 'down':
        SnakeDead = True
    if SnakeList[0][0] == 1 and SnakeDir == 'left':
        SnakeDead = True
    if SnakeList[0][0] == 40 and SnakeDir == 'right':
        SnakeDead = True

    if SnakeList[0] in SnakeList[1:]:
        SnakeDead = True

    return SnakeEat, SnakeDead, Score, ApplePos


class SnakeEnv(gym.Env):
    def __init__(self):
        # Set to none initially because we will set it once we want to render the game
        self.render_mode = None
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(
            low=0, high=40, shape=(5,), dtype=np.float32)
        # observation space is a 5x5 grid with the agent in the center. low and high are the min and max values for the grid.

    def step(self, action):
        self.snake_eat, self.snake_dead, self.score, self.apple_pos = collision(
            self.snake_list, self.apple_pos, self.snake_dir, self.snake_eat, self.snake_dead, self.score)

        self.snake_list, self.snake_eat = updating_snake(
            self.snake_dir, self.snake_list, self.snake_eat, self.snake_dead)

        self.apple_pos = apple_generating(self.snake_list, self.apple_pos)

        if action == 0:
            self.snake_dir = 'up'
        if action == 1:
            self.snake_dir = 'down'
        if action == 2:
            self.snake_dir = 'right'
        if action == 3:
            self.snake_dir = 'left'

        self.observation = [self.snake_list[0][0], self.snake_list[0]
                            [1], self.apple_pos[0], self.apple_pos[1], action]
        # State(observation) is a 5 element array with head x and y position, apple x and y position, and direction of snake as num_dir.
        self.observation = np.array(self.observation)
        if self.snake_dead:
            self.done = True

        # reward
        # 1. reward for dying
        if self.done:
            reward_1 = -100
        else:
            reward_1 = 0
        # 2. reward for eating apple
        if self.prevscore < self.score:
            reward_2 = 10
            self.timestep_passed_since_last_reward = 0
            self.valid_moves += 1
            self.prevscore = self.score
        else:
            self.timestep_passed_since_last_reward += 1
            reward_2 = 0
        # 3. reward for moving towards apple
        self.dist = abs(self.snake_list[0][0] - self.apple_pos[0]) + \
            abs(self.snake_list[0][1] - self.apple_pos[1])
        if self.dist > self.prevdist:
            reward_3 = -1
        elif self.dist < self.prevdist:
            reward_3 = 1
        else:
            reward_3 = 0
        self.prevdist = self.dist

        # 5. reward for valid moves. Punishment for wasting time
        reward_4 = self.timestep_passed_since_last_reward // self.valid_moves

        # Calculating total reward
        self.reward = reward_1 + reward_2 + reward_3 + reward_4
        self.info = {}

        if self.render_mode == "human":
            self.render()

        return self.observation, self.reward, self.done, self.info

    def reset(self):
        self.done = False  # used to end episode
        self.snake_dir = ''
        self.snake_list = []
        self.apple_pos = []
        self.snake_eat = False
        self.snake_dead = False

        # snake and apple genereation should be done here because we want to reset the game
        self.snake_list, self.snake_dir = snake_generating(
            self.snake_list, self.snake_dir)
        self.apple_pos = apple_generating(self.snake_list, self.apple_pos)

        # initialize the observation
        if self.snake_dir == 'up':
            self.num_dir = 0
        if self.snake_dir == 'down':
            self.num_dir = 1
        if self.snake_dir == 'right':
            self.num_dir = 2
        if self.snake_dir == 'left':
            self.num_dir = 3

        self.observation = [self.snake_list[0][0], self.snake_list[0]
                            [1], self.apple_pos[0], self.apple_pos[1], self.num_dir]
        # State(observation) is a 5 element array with head x and y position, apple x and y position, and direction of snake as num_dir.
        self.observation = np.array(self.observation)

        # reward
        self.reward = 0
        self.score = 0
        self.prevscore = 0
        self.dist = abs(self.snake_list[0][0] - self.apple_pos[0]) + \
            abs(self.snake_list[0][1] - self.apple_pos[1])
        self.prevdist = self.dist
        self.valid_moves = 30+40+3
        self.timestep_passed_since_last_reward = 0

        if self.render_mode == "human":
            pygame.init()
            pygame.display.set_caption('Snake RL')
            self.display = pygame.display.set_mode((WIDTH, HEIGHT))
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont('Arial_bold', 380)

            self.render()

        return self.observation

    def render(self, render_mode="human"):
        # draw background
        self.display.fill((67, 70, 75))

        # borders: top, bottom, right, left
        pygame.draw.rect(self.display, 'WHITE', (15, 15, 40 * 15, 1))
        pygame.draw.rect(self.display, 'WHITE', (15, 31 * 15, 40 * 15, 1))
        pygame.draw.rect(self.display, 'WHITE', (41 * 15, 15, 1, 30 * 15))
        pygame.draw.rect(self.display, 'WHITE', (15, 15, 1, 30 * 15))

        # score text
        if self.snake_dead:
            # This code is used to display the score on the screen.
            img = self.font.render(str(self.score), True, (125, 85, 85))
        else:
            img = self.font.render(str(self.score), True, (57, 60, 65))
        self.display.blit(img, img.get_rect(
            center=(20 * 15 + 15, 15 * 15 + 15)).topleft)

        # apple
        if len(self.apple_pos) > 0:
            pygame.draw.rect(
                self.display, 'RED', (self.apple_pos[0] * 15 + 1, self.apple_pos[1] * 15 + 1, 13, 13))

        # snake body
        for part in self.snake_list[1:]:
            pygame.draw.rect(self.display, (180, 180, 180),
                             (part[0] * 15 + 1, part[1] * 15 + 1, 13, 13))
        # snake head
        pygame.draw.rect(
            self.display, 'WHITE', (self.snake_list[0][0] * 15 + 1, self.snake_list[0][1] * 15 + 1, 13, 13))

        pygame.display.update()
        # This code is used to set the frame rate of the game. The clock.tick function will pause the game until the time since the last call to clock.tick is equal to 1/FPS seconds. So, if FPS is 10, then the game will run at 10 frames per second.
        self.clock.tick(FPS)

        if self.done:
            time.sleep(0.5)

    def close(self):
        pygame.quit()
