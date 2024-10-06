import random
import re
from collections import namedtuple

import requests

api_path = 'http://localhost:8000'

action = namedtuple('action', ['action', 'path'])

paths = requests.get(f'{api_path}/openapi.json').json().get('paths')
actions = []
for path, methods in paths.items():
    methods = methods.keys()

    if 'get' in methods:
        actions.append(action(requests.get, path))

    if 'post' in methods:
        actions.append(action(requests.post, path))

    if 'put' in methods:
        actions.append(action(requests.put, path))

    if 'patch' in methods:
        actions.append(action(requests.patch, path))

    if 'delete' in methods:
        actions.append(action(requests.delete, path))

while True:
    action = random.choice(actions)
    action_path = api_path + re.sub(r'{[\w_]*}', lambda _: str(random.randint(0, 100)), action.path)

    action.action(action_path)
