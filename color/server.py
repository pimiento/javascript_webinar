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

@route("/color/json")
def getrandomcolor():
    fg_style = Style()
    bg_style = Style()
    new_fg = fg_style.color
    new_bg = bg_style.color
    while new_bg in fg_style.stack:
        new_bg = bg_style.color
    return dict(
        fg_value=new_fg,
        bg_value=new_bg
    )

run(host='localhost', port=8000, reloader=True)
