# %%
import numpy as np
import gym
import random
import time
from IPython.display import clear_output


env = gym.make("FrozenLake-v1", render_mode="rgb_array")

# %%
# Actions are going to be left, right, up and down. Movement direction.
actionSpaceSize = env.action_space.n
# States are going to be S,F,H and G. S is the starting point, F is frozen, H is a hole and G is the goal.
stateSpaceSize = env.observation_space.n

qtable = np.zeros((stateSpaceSize, actionSpaceSize))
# As you can see, for a 4x4 grid, we have 16 states and 4 actions for each state.
# So, our Q-table will have 16 rows and 4 columns, filled with zeros.
print(qtable)

# The rewards for each state are as follows:
# S: 0 (starting point)
# F: 0 (frozen surface)
# H: 0 (hole)
# G: 1 (goal)


# %%
# Create and initialize all the hyperparameters that will be used in the algorithm. These are the parameters that will be used to learn the Q-values for the actions in the environment.
# Total number of episodes. Episodes are basically the number of times we train the agent.
numEpisodes = 10000
maxStepsPerEpisode = 100  # Max steps allowed for each episode. If the agent falls in a hole, then the episode ends and we start a new episode.IF the agent reaches the goal, then the episode ends and we start a new episode. ıF the agent takes 100 steps BUT does not reach the goal, then the episode ends and we start a new episode.
learningRate = 0.1  # Learning rate
discountRate = 0.99  # Discount rate

explorationRate = 1  # Exploration rate. Is used to determine the probability of agent to take a random action. This is important because we want the agent to explore the environment and not just exploit it. exploitation is when the agent takes the action that has the highest Q-value for the current state. Exploration is when the agent takes a random action, so that it can discover new states and rewards.

maxExplorationRate = 1  # Exploration probability at start
minExplorationRate = 0.01  # Minimum exploration probability at the end.
explorationDecayRate = 0.001  # Exponential decay rate for exploration probability. This is used to reduce the exploration probability over time. This is done so that the agent lies more on exploiting the environment rather than exploring it. This is because we want the agent to explore the environment more at the start and then exploit it more towards the end. Greedy epsilon approach.

# %%
# I want to be able to play this game with arrow keys.
# So, I will create a dictionary that will map the arrow keys to the actions in the environment.
arrowKeys = {0: '←', 1: '↓', 2: '→', 3: '↑'}

# Logic to allow the user to play the game with arrow keys.


def playGame():
    for episode in range(3):
        state = env.reset()
        done = False
        print("Episode:", episode + 1)
        time.sleep(1)
        for step in range(maxStepsPerEpisode):
            clear_output(wait=True)
            env.render()
            time.sleep(0.3)

            # Get action from the user for human interaction
            print("Available actions: ", arrowKeys)
            user_action = int(input("Enter action (0-3): "))

            if user_action not in arrowKeys:
                print("Invalid action. Please choose from", arrowKeys)
                continue

            action = user_action  # Use the user-specified action

            state, reward, done, info = env.step(action)

            if done:
                clear_output(wait=True)
                env.render()

                if reward == 1:
                    print("You reached the goal!")
                else:
                    print("You fell through a hole!")

                time.sleep(3)
                clear_output(wait=True)
                break

    env.close()

# playGame()


# %%
# All of ther rewards from each episode is stored to keep track of how our game scores change over time.
TotalRewards = []

# Q learning algorithm
for episode in range(numEpisodes):
    # Reset the environment to start a new episode. State is the current state that the agent is in. In form of a number. For example, 0 is the starting point, 1 is the frozen surface, 2 is the hole and 3 is the goal. state is in form of (0, {'prob': 1}) where 0 is the state and {'prob': 1} is the probability of the agent being in that state. The probability is 1 because the agent is definitely in that state.
    state = env.reset()[0]

    print(state)
    done = False  # Boolean variable to check if the episode has ended or not.
    # Variable to store the total rewards for the current episode.
    episodeRewards = 0
    for step in range(maxStepsPerEpisode):
        rand = np.random.uniform(0, 1)  # Get a random number between 0 and 1.
        if rand > explorationRate:
            # Exploit the environment, use the q table to get the action that has the highest Q-value for the current state.
            action = np.argmax(qtable[state, :])
            # This is taking the action that has the highest Q-value for the current state by slicing the Q-table for the current state and then taking the action that has the highest Q-value. The colon means that we are taking all the actions for the current state, and then we are taking the action that has the highest Q-value by calling the argmax function.
        else:
            # Explore the environment, take a random action. A random action is taken because the random number is less than the exploration rate. This is done so that the agent can explore the environment.
            action = env.action_space.sample()
            # env.action_space.sample() returns a random action from the action space. The action space is the set of all the actions that the agent can take in the environment.In this case, the actions can be left, right, up and down.

        # We have defined the action. Now, with this action, we can get the new state, reward, done and info from the environment by playing the action in the environment.
        observation, reward, terminated, truncated, info = env.step(action)

        # We need to update the Q table with the new knowledge that we have gained from the environment. The formula for updating the Q table is,
        # Q(s,a) = Q(s,a) + learningRate * (reward + discountRate * maxQ(s',a') - Q(s,a))
        # where, s is the current state, a is the action that we took, s' is the new state that we reached after taking the action, a' is the action that we will take in the new state, learningRate is the learning rate, discountRate is the discount rate, reward is the reward that we got from the environment for taking the action and info is the information that we got from the environment for taking the action, Q(s,a) is the Q-value for the current state and action, Q(s',a') is the Q-value for the new state and action, maxQ(s',a') is the maximum Q-value for the new state and for all the actions that we can take in the new state.
        qtable[state, action] = qtable[state, action] + learningRate * \
            (reward + discountRate *
             np.max(qtable[observation, :]) - qtable[state, action])

        state = observation  # Update the current state to the new state.
        # Update the reward for the current episode. Episode reward is the total reward that we get from the environment for the current episode.
        episodeRewards += reward

        if terminated == True or truncated == True:
            break

    # We have finished playing the episode. Now, we need to update the exploration rate. We need to do this because we want the agent to explore the environment more at the start and then exploit it more towards the end. Greedy epsilon approach.
    explorationRate = minExplorationRate + \
        (maxExplorationRate - minExplorationRate) * \
        np.exp(-explorationDecayRate*episode)
    # Updating the exploration rate using the formula for exponential decay formula. The formula, generally is y = a + (b - a) * e^(-cx), where y is the value that we want to calculate, a is the minimum value that y can take, b is the maximum value that y can take, c is the decay rate and x is the current iteration(episode). In our case, y is the exploration rate, a is the minimum exploration rate, b is the maximum exploration rate, c is the decay rate and x is the current episode number. The exploration rate value is decreased proportionally to the episode number.

    # Append the episode reward to the list of rewards.
    TotalRewards.append(episodeRewards)

# Calculate and print the average reward per thousand episodes.
# This will get the rewards for every thousand episodes and put them in a list. TotalRewards is a list that contains total reward for each episode. We are converting it to a numpy array so that it contains the reards for each episode as a list. Then, we are splitting the numpy array into a list of numpy arrays, where each numpy array contains the rewards for every thousand episodes. We are doing this so that we can calculate the average reward for every thousand episodes. Finally, rewardsPerThousandEpisodes will be a list of numpy arrays, where each numpy array contains the rewards for every thousand episodes.
rewardsPerThousandEpisodes = np.split(np.array(TotalRewards), numEpisodes/1000)
# Structure of rewardsPerThousandEpisodes: [[1000 rewards], [1000 rewards], [1000 rewards], ...] with a total of 10 lists.
count = 1000
print("*********Average reward per thousand episodes*********\n")
for r in rewardsPerThousandEpisodes:
    print(count, ": ", str(sum(r/1000)))
    # Calculate the average reward for every thousand episodes by dividing the sum of rewards for every thousand episodes by 1000.

print("\n\n*********Q-table*********\n")
print(qtable)

# %%
