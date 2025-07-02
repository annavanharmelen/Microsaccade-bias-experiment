"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'microsaccade bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from psychopy import visual
from numpy import zeros
from math import sqrt

ECCENTRICITY = 5
DOT_SIZE = 0.1  # radius of fixation dot


def create_fixation_dot(settings, colour="#eaeaea"):
    # Determine size of fixation cross
    fixation_size = settings["deg2pix"](DOT_SIZE)

    # Make fixation dot
    fixation_dot = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=fixation_size,
        pos=(0, 0),
        fillColor=colour,
    )

    fixation_dot.draw()


def make_one_gabor(orientation, colour, position, settings):
    # Check input
    if position == "left":
        pos = (
            -settings["deg2pix"](sqrt(1 / 2 * ECCENTRICITY**2)),
            -settings["deg2pix"](sqrt(1 / 2 * ECCENTRICITY**2)),
        )
    elif position == "right":
        pos = (
            settings["deg2pix"](sqrt(1 / 2 * ECCENTRICITY**2)),
            -settings["deg2pix"](sqrt(1 / 2 * ECCENTRICITY**2)),
        )
    elif position == "middle":
        pos = (0, -settings["deg2pix"](sqrt(1 / 2 * ECCENTRICITY**2)))
    else:
        raise Exception(f"Expected 'left' or 'right', but received {position!r}. :(")

    # Create texture for Gabor stimulus
    gabor_texture = zeros([settings["gabor_size"], settings["gabor_size"], 4], "f")
    gabor_texture[:, :, 0] = colour[0]
    gabor_texture[:, :, 1] = colour[1]
    gabor_texture[:, :, 2] = colour[2]
    gabor_texture[:, :, 3] = -visual.filters.makeGrating(
        settings["gabor_size"], gratType="sin", cycles=7.5, ori=orientation
    )

    # Create Gabor grating stimulus
    gabor_stimulus = visual.GratingStim(
        win=settings["window"],
        units="pix",
        size=(settings["gabor_size"], settings["gabor_size"]),
        pos=pos,
        tex=gabor_texture,
        mask="raisedCos",
        maskParams={"fringeWidth": 0.5},
    )

    return gabor_stimulus


def create_stimuli_frame(
    left_orientation, right_orientation, stim_colours, settings, fix_colour="#eaeaea"
):
    create_fixation_dot(settings, fix_colour)
    make_one_gabor(left_orientation, stim_colours[0], "left", settings).draw()
    make_one_gabor(right_orientation, stim_colours[1], "right", settings).draw()


def show_text(input, window, pos=(0, 0), colour="#ffffff"):
    textstim = visual.TextStim(
        win=window, font="Courier New", text=input, color=colour, pos=pos, height=22
    )

    textstim.draw()
