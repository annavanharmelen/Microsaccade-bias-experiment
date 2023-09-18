"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'microsaccade bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from psychopy import visual

ECCENTRICITY = 6
GABOR_SIZE = [4, 4]  # width, height
CAPTURE_CUE_SIZE = 0.7  # diameter of circle


def create_fixation_cross(settings, colour="#eaeaea"):
    # Determine size of fixation cross
    fixation_size = settings["deg2pix"](0.22)

    # Make fixation cross
    fixation_cross = visual.ShapeStim(
        win=settings["window"],
        vertices=(
            (0, -fixation_size),
            (0, fixation_size),
            (0, 0),
            (-fixation_size, 0),
            (fixation_size, 0),
        ),
        lineWidth=settings["deg2pix"](0.06),
        lineColor=colour,
        closeShape=False,
        units="pix",
    )

    fixation_cross.draw()


def make_one_gabor(orientation, colour, position, settings):
    # Check input
    if position == "left":
        pos = (-settings["deg2pix"](ECCENTRICITY), 0)
    elif position == "right":
        pos = (settings["deg2pix"](ECCENTRICITY), 0)
    elif position == "middle":
        pos = (0, 0)
    else:
        raise Exception(f"Expected 'left' or 'right', but received {position!r}. :(")

    # Create gabor grating stimulus
    gabor_stimulus = visual.GratingStim(
        win=settings["window"],
        units="pix",
        size=(settings["deg2pix"](GABOR_SIZE[0]), settings["deg2pix"](GABOR_SIZE[1])),
        pos=pos,
        color=colour,
        ori=orientation,
        tex="sin",
        mask="gauss",
        sf=(settings["deg2pix"](GABOR_SIZE[0])/10000, settings["deg2pix"](GABOR_SIZE[0])/2500000),
    )

    return gabor_stimulus


def create_stimuli_frame(left_orientation, right_orientation, colours, settings):
    create_fixation_cross(settings)
    make_one_gabor(left_orientation, colours[0], "left", settings).draw()
    make_one_gabor(right_orientation, colours[1], "right", settings).draw()


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
