import gym
import numpy as np
import sys
import copy
import random
import time

env = gym.make("Taxi-v3")
env.reset()

n_states = 500
n_actions = 6
gamma = 0.9
theta = 0.1

V = np.zeros(n_states)
pi = np.zeros((500,), dtype=int)


def value_iteration():
    delta = np.inf
    iter_count = 0
    while delta > theta:
        delta = 0
        for s in range(n_states):
            v = copy.deepcopy(V[s])

            test_actions = np.zeros((6,))
            for a in range(n_actions):
                # env is deterministic (only one successor state)
                # get successor state
                env.env.s = s  # set state
                next_state, reward, _, _ = env.step(a)

                test_actions[a] = reward + gamma * V[next_state]
            a_max = test_actions.max()
            indices = [i for i, e in enumerate(test_actions) if e == a_max]
            action = random.choice(indices)

            V[s] = test_actions[action]

            delta = max(delta, np.linalg.norm(v - V[s]))

        iter_count = iter_count + 1

        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write(f'Iteration: {iter_count}')
        sys.stdout.flush()

    print('\n')

    # ------------ OUTPUT DETERMINISTIC POLICY ------------------------------ #

    for s in range(n_states):
        test_actions = np.zeros((6,))
        for a in range(n_actions):
            # env is deterministic (only one successor state)
            # get successor state
            env.env.s = s  # set state
            next_state, reward, _, _ = env.step(a)

            test_actions[a] = reward + gamma * V[next_state]
        a_max = test_actions.max()
        indices = [i for i, e in enumerate(test_actions) if e == a_max]
        action = random.choice(indices)

        pi[s] = action

    return pi


pi = value_iteration()

print(f'# --------- VALUES ----------- #')
print(V)
print(f'# --------- POLICY ---------- #')
print(pi)

# ------------------------ TESTING ------------------------------------------ #

state = env.reset()
env.render()

for c in range(10):
    done = False
    total_reward = 0
    while not done:
        action = pi[state]
        print(action)
        state, reward, done, _ = env.step(action)
        total_reward += reward
        env.render()
        time.sleep(3)
    print(f'Total reward: {total_reward}\n')
    time.sleep(5)
    print(f'------------------------------')
    print(f'          NEW ROUND           ')
    print(f'------------------------------\n')

    state = env.reset()
    env.render()


