"""
This script is used to test random aspects
of the 'null-cue gaze bias' experiment.

made by Anna van Harmelen, 2023
"""

from psychopy import visual
from math import atan2, degrees
import time
import random
#from set_up import set_up
import pandas as pd
import datetime as dt

monitor = {
        "resolution": (1920, 1080),  # in pixels
        "Hz": 239,  # screen refresh rate in Hz
        "width": 53,  # in cm
        "distance": 70,  # in cm
    }

degrees_per_pixel = degrees(atan2(0.5 * monitor["width"], monitor["distance"])) / (
    0.5 * monitor["resolution"][0]
)

print(degrees_per_pixel)

# stop here
import sys
sys.exit()

current_block = 3
blocks_left = 1
print(f"You just finished block {current_block}, you{' only' if blocks_left == 1 else ''} have {blocks_left} block{'s' if blocks_left != 1 else ''} left.")


og_start = time.time()
time.sleep(1)
start = time.time()
time.sleep(1)
trial1_done = time.time()
time.sleep(1)
trial2_done = time.time()

trial1_length = trial1_done - start
trial2_length = trial2_done - trial1_done
print(dt.timedelta(seconds = trial1_length))
print(dt.timedelta(seconds = trial2_length))
print(dt.timedelta(seconds = (time.time() - og_start)))



temp = random.sample([[0, 0.6, 1], [0.8, 0.2, 0.2], [0, 0.8, 0.4], [0.9, 0.8, 0.3]], 2)
print(temp)
print(type(temp))


test_data = pd.DataFrame({"number": [1, 2, 3], "fruits": ['apples', 'bananas', 'cactus']})
print(test_data)

#test_data.fruits.iloc[-1] = 'citroen'
#test_data.loc[:, ('one', 'second')] = value
test_data.loc[test_data.index[-1], "fruits"] = "citroen"
print(test_data)




set_up(True)

from set_up import global_state

print(global_state)


def deg2pix(deg):
    dpix = degrees(atan2(0.5 * 17.5, 50)) / (0.5 * 1080)
    return int(deg / dpix)
# bovenstaande waardes geven een dpix waarde van 0.018381...
# en dat is een logische waarde voor aantal visual degrees per pixel op het scherm
# Dat is ook logisch als je zegt dat de stimulus 1 visual degree moet zijn (see below)
# want dan bereken je nu het aantal pixels dat daarmee overeenkomt.


# window = visual.Window(color=[0, 0.6, 1], size=[1920, 1080], units="pix", fullscr=True)

fixation_size = {
    "size": deg2pix(0.2),
    "line": deg2pix(0.2),
    "basecol": (0.2, 0.2, 0.2),
    "probecol": (0.9, 0.9, 0.9),
}

fixation_cross = visual.ShapeStim(
    win=window,
    vertices=(
        (0, -fixation_size["size"]),
        (0, fixation_size["size"]),
        (0, 0),
        (-fixation_size["size"], 0),
        (fixation_size["size"], 0),
    ),
    lineColor=[0, 0, 0],
    lineWidth=fixation_size["line"],
    closeShape=False,
    units="pix",
)

bar_stimulus_right = visual.Rect(
    win=window,
    units="pix",
    width=deg2pix(0.4),
    height=deg2pix(3),
    pos=[deg2pix(6), 0],
    fillColor="black",
    ori=random.randint(0,360),
)

bar_stimulus_left = visual.Rect(
    win=window,
    units="pix",
    width=deg2pix(0.4),
    height=deg2pix(3),
    pos=[-deg2pix(6), 0],
    fillColor="black",
    ori=random.randint(0,360),
)

fixation_cross.draw()
bar_stimulus_right.draw()
bar_stimulus_left.draw()
window.flip()
time.sleep(1)


fixation_cross.draw()

capture_cue = visual.Rect(
    win=window,
    units='pix',
    width=deg2pix(2),
    height=deg2pix(2),
    pos=(0,0),
    lineColor = 'red',
    lineWidth = deg2pix(0.1),
    fillColor = None,
)

capture_cue.draw()
window.flip()
time.sleep(2)
