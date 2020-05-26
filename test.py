import json

with open('commands.json') as f:
    commands = json.load(f)
for command in commands:
    print(command+'\n')
    print(commands[command]["value"])
