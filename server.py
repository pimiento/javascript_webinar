#!/usr/bin/env python3
import random
import numpy as np
from bottle import route, run, view, static_file

prev_values = {
    "fg": np.array([]),
    "bg": np.array([])
}

@route("/")
@view("index_template")
def index():
    return {}

@route("/dice")
def dice():
    prev_fg = prev_values["fg"]
    new_fg = prev_fg
    prev_bg = prev_values["bg"]
    new_bg = prev_bg
    dice_value = random.randint(1, 6)
    while np.array_equal(prev_fg, new_fg):
        new_fg = np.random.choice(range(20, 256), size=3)
    prev_values["fg"] = new_fg
    while np.array_equal(prev_bg, new_bg) or np.array_equal(new_fg, new_bg):
        new_bg = np.random.choice(range(20, 256), size=3)
    prev_values["bg"] = new_bg
    return dict(
        dice_value=dice_value,
        fg_value=new_fg.tolist(),
        bg_value=new_bg.tolist()
    )

@route("/<filename:re:\w*\.js>")
def send_js(filename):
    return static_file(filename, root="/home/pimiento/yap/javascript_webinar")

@route("/favicon.ico")
def favicon():
    return static_file(
        "favicon.ico",
        root="/home/pimiento/yap/javascript_webinar"
    )

run(host='localhost', port=8000)
