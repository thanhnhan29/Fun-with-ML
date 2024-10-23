import gymnasium
import numpy as np

env = gymnasium.make("MountainCar-v0", render_mode=None)
env1 = gymnasium.make("MountainCar-v0", render_mode="human")
# env.reset()

size = [20, 20]
size_table = (env.observation_space.high - env.observation_space.low) / size


def convert_qtable(value):
    q_state = (value - env.observation_space.low) // size_table
    return tuple(q_state.astype(np.int64))


def render(list_action):
    env1.reset()
    for e in list_action:
        env1.step(e)
    env1.render()


c_learning_rate = 0.9
c_discount_value = 0.9
ep = 10000
c_show_each = 1000

epsilon = 0.9
c_start_ep_epsilon_decay = 1
c_end_ep_epsilon_decay = ep // 2
v_epsilon_decay = epsilon / (c_end_ep_epsilon_decay - c_start_ep_epsilon_decay)
q_table = np.random.uniform(low=-2, high=0, size=(size + [env.action_space.n]))

nmin = -500
action_min = []

for i in range(ep):
    state_reset = env.reset()[0]
    current_state = convert_qtable(state_reset)

    done = False
    list_action = []
    ep_reward = 0
    show = False

    # print(i)
    while not done:
        if i >= ep // 2:
            action = np.argmax(q_table[current_state])
        else:
            if np.random.random() > epsilon:
                action = np.argmax(q_table[current_state])
            else:
                action = np.random.randint(0, env.action_space.n)
        list_action.append(action)
        environment = env.step(action)

        future_state = environment[0]
        reward = environment[1]
        done = environment[2]
        ep_reward += reward
        if done:
            if current_state[0] >= 0.5:

                print("oke {}, reward {}".format(i, ep_reward))
                if nmin < ep_reward:
                    nmin = ep_reward
                    action_min = list_action
                # env.render_mode = "human"
                if ep_reward > -110:
                    render(list_action)
                # env.render_mode = None
        else:
            if ep_reward < -500:
                print("not oke    {} {}".format(i, ep_reward))
                break
            next_state = convert_qtable(future_state)
            q_current = q_table[current_state + (action,)]
            new_q_value = (1 - c_learning_rate) * q_current + c_learning_rate * (
                    reward + c_discount_value * np.max(q_table[next_state]))
            q_table[current_state + (action,)] = new_q_value
            current_state = next_state
        if c_end_ep_epsilon_decay >= i > c_start_ep_epsilon_decay:
            epsilon = epsilon - v_epsilon_decay

print("min: {}".format(nmin))
render(action_min)
