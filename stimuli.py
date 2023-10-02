"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'microsaccade bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from psychopy import visual
from numpy import zeros

ECCENTRICITY = 3
VERTICAL_POSITION = -3
GABOR_SIZE = 2  # diameter of Gabor
CAPTURE_CUE_SIZE = 0.7  # diameter of circle


def create_fixation_cross(settings, colour="#eaeaea"):
    # Determine size of fixation cross
    fixation_size = settings["deg2pix"](0.1)

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
            -settings["deg2pix"](ECCENTRICITY),
            settings["deg2pix"](VERTICAL_POSITION),
        )
    elif position == "right":
        pos = (
            settings["deg2pix"](ECCENTRICITY),
            settings["deg2pix"](VERTICAL_POSITION),
        )
    elif position == "middle":
        pos = (0, 0)
    else:
        raise Exception(f"Expected 'left' or 'right', but received {position!r}. :(")

    # Create texture for Gabor stimulus
    gabor_texture = zeros(
        [256, 256, 4], "f"
    )
    gabor_texture[:, :, 0] = colour[0]
    gabor_texture[:, :, 1] = colour[1]
    gabor_texture[:, :, 2] = colour[2]
    gabor_texture[:, :, 3] = -visual.filters.makeGrating(
        256, gratType="sin", cycles=10.5, ori=orientation
    )

    # Create Gabor grating stimulus
    gabor_stimulus = visual.GratingStim(
        win=settings["window"],
        units="pix",
        size=(256, 256),
        pos=pos,
        tex=gabor_texture,
        mask="raisedCos",
        maskParams={"fringeWidth": 0.5},
    )

    return gabor_stimulus


def create_stimuli_frame(left_orientation, right_orientation, stim_colours, settings, fix_colour="#eaeaea"):
    create_fixation_cross(settings, fix_colour)
    make_one_gabor(left_orientation, stim_colours[0], "left", settings).draw()
    make_one_gabor(right_orientation, stim_colours[1], "right", settings).draw()


def create_cue_frame(colour, settings):
    capture_cue = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](CAPTURE_CUE_SIZE / 2),
        pos=(0, 0),
        fillColor=colour,
    )

    capture_cue.draw()
    create_fixation_cross(settings)
