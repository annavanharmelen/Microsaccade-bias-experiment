"""
This script is used to test random aspects
of the 'microsaccade bias' experiment.

made by Anna van Harmelen, 2023
"""

from psychopy import visual
from psychopy.hardware.keyboard import Keyboard
from math import atan2, degrees, sqrt
import time
import random
from numpy import ones, zeros, unique
from block import create_trial_list, create_blocks
from set_up import get_monitor_and_dir, get_settings

# from set_up import set_up
import pandas as pd
import datetime as dt

testing = False

monitor, directory = get_monitor_and_dir(testing)
settings = get_settings(monitor, directory)

middle_x = settings["monitor"]["resolution"][0] // 2
middle_y = settings["monitor"]["resolution"][1] // 2
allowed_radius = settings["deg2pix"](1)

print(middle_x)
print(middle_y)
print(allowed_radius)

# stop here
import sys

sys.exit()
