#!/bin/bash

sudo apt install libnspr4 libatk1.0-0 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libatspi2.0-0 \
&& export PYTHONPATH=$PYTHONPATH:./bot \
&& pip install -r requirements.txt \
&& python -m playwright install chromium \
&& python bot/runemaster.py
