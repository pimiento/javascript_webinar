#!/usr/bin/env python3
import random
import numpy as np
from bottle import route, run, view, static_file


class Style:
    def __init__(self, n=5):
        self.__stack = []
        self.n = n

    @property
    def color(self):
        MAX_TRIES = 10
        new_color = np.random.choice(np.arange(20, 256), size=3).tolist()
        while new_color in self.__stack:
            MAX_TRIES -= 1
            new_color = np.random.choice(np.arange(20, 256), size=3).tolist()
            if MAX_TRIES < 0:
                print(new_color, self.__stack)
                raise RuntimeError("Your code is shameless!")
        self.__stack.append(new_color)
        self.__stack = self.__stack[:-self.n]
        return new_color

    @property
    def stack(self):
        return self.__stack[::]

@route("/dice")
def index():
    return {}

@route("/dice/json")
def dice():
    dice_value = random.randint(1, 6)
    return {'dice_value': dice_value}


run(host='0.0.0.0', port=8000, reloader=True)
