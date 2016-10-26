import gym
import time
import sys

SKIP_CONTROL = 0    # Use previous control decision SKIP_CONTROL times, that's how you
                    # can test what skip is still usable.

incremental_action_games = []
         
def controller_mapping(game_name):
    if 'LunarLander' in game_name:
        return {ord('s'):2, ord('a'):3, ord('d'):1}
    elif 'Breakout' in game_name:
        return {ord('a'):3, ord('d'):2}
    elif 'Asteroids' in game_name:
        return {ord('a'):4, ord('w'):2, ord('d'):3, ord('s'):5, 32:1 }
    elif 'CarRacing' in game_name:
        return {(ord('a'),0): -1.0, (ord('w'),1):+1.0, (ord('d'),0):+1.0, (ord('s'),2):+0.8}
    
game_name = str(sys.argv[1])
env = gym.make(game_name)
keybinds = controller_mapping(game_name)

#Get type of action for env
human_agent_action = env.action_space.sample()
action_islist = hasattr(human_agent_action,'__contains__');
action_isIncremental = len([s for s in incremental_action_games if s in game_name])>0
human_agent_action = [0]*len(human_agent_action) if action_islist else 0
    
def zero_actions(key):
    global keybinds, human_agent_action, action_islist, action_isIncremental
    if action_isIncremental:
        return
    if action_islist:
        for k,i in keybinds.keys():
            if key == k:
                human_agent_action[i] = 0
                return
    else:
        human_agent_action = 0

def do_action(key):
    global keybinds, action_islist, action_isIncremental, human_agent_action
    if action_isIncremental:
        if action_islist:
            for k,i in keybinds.keys():
                if k == key:
                    human_agent_action[i] += keybinds[(k,i)]
                    return
        else:
            human_agent_action += keybinds[key]
    else:
        if action_islist:
            for k,i in keybinds.keys():
                if k == key:
                    human_agent_action[i] = keybinds[(k,i)]
                    return
        else:
            if key in keybinds.keys():
                human_agent_action = keybinds[key]                            

def key_press(key,mod):
    do_action(key)

def key_release(key,mod):
    zero_actions(key)

env.reset()
env.render()
env.viewer.window.on_key_press = key_press
env.viewer.window.on_key_release = key_release

done = False
skip = 0

while not done:
    if not skip:
        a = human_agent_action
        skip = SKIP_CONTROL
    else:
        skip -= 1
        
    obser,r,done,info = env.step(a)
    env.render()
    time.sleep(0.033)
    
