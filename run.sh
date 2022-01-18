#!/bin/bash

export PYTHONPATH=$PYTHONPATH:./bot \
&& pip install -r requirements.txt \
&& python3 -m playwright install chromium \
&& python3 bot/runemaster.py
