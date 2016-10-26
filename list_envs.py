import sys
import gym

query = str(sys.argv[1]) if len(sys.argv)>1 else ''

envlist = []
for entry in gym.envs.registry.all():
    envlist.append(entry.id)

envlist.sort()

for envid in envlist:
    if query in envid:
        print envid
