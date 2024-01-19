"""
This file contains the functions necessary for
creating and running a single trial start-to-finish,
including eyetracker triggers.
To run the 'microsaccade bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from psychopy import visual
from time import time, sleep
from response import get_response, check_quit, sample_while_wait
from stimuli import (
    create_fixation_dot,
    create_stimuli_frame,
)
from eyetracker import get_trigger
import random

# COLOURS = [[21, 165, 234], [133, 193, 18], [197, 21, 234], [234, 74, 21]]
COLOURS = [[19, 146, 206], [217, 103, 241], [101, 148, 14], [238, 104, 60]]
COLOURS = [
    [(rgb_value / 128 - 1) for rgb_value in rgb_triplet] for rgb_triplet in COLOURS
]
ORIENTATION_TURN = 2


def generate_trial_characteristics(
    condition: str, target_bar: str, duration, direction: str
):
    # Decide on random colours of stimulus
    stimuli_colours = random.sample(COLOURS, 2)

    # Create random original orientations
    orientations = [
        random.choice([-1, 1]) * random.randint(5, 85),
        random.choice([-1, 1]) * random.randint(5, 85),
    ]

    post_orientations = list(orientations)

    # Make orientation change in predetermined direction
    if direction == "clockwise":
        orientation_change = ORIENTATION_TURN
    if direction == "anticlockwise":
        orientation_change = -ORIENTATION_TURN

    # Determine both stimuli orientations after orientation change
    if target_bar == "left":
        target_colour, distractor_colour = stimuli_colours
        target_pre_orientation = orientations[0]
        target_post_orientation = post_orientations[0] = (
            post_orientations[0] + orientation_change
        )
    else:
        distractor_colour, target_colour = stimuli_colours
        target_pre_orientation = orientations[1]
        target_post_orientation = post_orientations[1] = (
            orientations[1] + orientation_change
        )

    # Determine colour of cue
    if condition == "valid":
        capture_colour = target_colour
    elif condition == "invalid":
        capture_colour = distractor_colour

    return {
        "static_duration": duration,
        "ITI": random.randint(500, 800),
        "change_direction": direction,
        "stimuli_colours": stimuli_colours,
        "capture_colour": capture_colour,
        "trial_condition": condition,
        "left_orientation": orientations[0],
        "right_orientation": orientations[1],
        "left_orientation_2": post_orientations[0],
        "right_orientation_2": post_orientations[1],
        "target_bar": target_bar,
        "target_colour": target_colour,
        "target_pre_orientation": target_pre_orientation,
        "target_post_orientation": target_post_orientation,
    }


def do_while_showing(waiting_time, something_to_do, settings, eyetracker=None):
    """
    Show whatever is drawn to the screen for exactly `waiting_time` period,
    while doing `something_to_do` in the mean time.
    """
    settings["window"].flip()
    start = time()
    something_to_do()

    sample_while_wait(start, waiting_time, eyetracker, settings)

def single_trial(
    static_duration,
    ITI,
    change_direction,
    left_orientation,
    right_orientation,
    left_orientation_2,
    right_orientation_2,
    target_bar,
    target_colour,
    target_pre_orientation,
    target_post_orientation,
    stimuli_colours,
    capture_colour,
    trial_condition,
    settings,
    testing,
    eyetracker=None,
):

    # Initial fixation cross to eliminate jitter caused by for loop
    create_fixation_dot(settings)

    screens = [
        (0, lambda: 0 / 0, None),  # initial one to make life easier
        (ITI, lambda: create_fixation_dot(settings), None),
        (
            750,
            lambda: create_stimuli_frame(
                left_orientation, right_orientation, stimuli_colours, settings
            ),
            "stimuli_onset",
        ),
        (
            static_duration,
            lambda: create_stimuli_frame(
                left_orientation,
                right_orientation,
                stimuli_colours,
                settings,
                capture_colour,
            ),
            "cue_onset",
        ),
        (
            None,
            lambda: create_stimuli_frame(
                left_orientation_2,
                right_orientation_2,
                stimuli_colours,
                settings,
                capture_colour,
            ),
        ),
    ]

    # !!! The timing you pass to do_while_showing is the timing for the previously drawn screen. !!!
    for index, (duration, _, frame) in enumerate(screens[:-1]):
        # Check for pressed 'q'
        check_quit(settings["keyboard"])

        # Send trigger if not testing
        if not testing and frame:
            trigger = get_trigger(frame, trial_condition, target_bar, change_direction)
            eyetracker.tracker.send_message(f"trig{trigger}")

        # Draw the next screen while showing the current one
        do_while_showing(duration, screens[index + 1][1], settings, eyetracker)
    
    # The for loop only draws the last frame, never shows it
    # So show it here
    if not testing:
        trigger = get_trigger(
            "orientation_change", trial_condition, target_bar, change_direction
        )
        eyetracker.tracker.send_message(f"trig{trigger}")

    settings["window"].flip()

    response = get_response(
        settings,
        testing,
        eyetracker,
        trial_condition,
        change_direction,
        target_bar,
    )

    # Show performance (and feedback on premature key usage if necessary)
    create_fixation_dot(settings)
    show_text(response["feedback"], settings["window"], (0, settings["deg2pix"](0.3)))
    
    if response["premature_pressed"] == True:
        show_text("!", settings["window"], (0, -settings["deg2pix"](0.3)))
    
    settings["window"].flip()
    sleep(0.25)

    return {
        "condition_code": get_trigger(
            "stimuli_onset", trial_condition, target_bar, change_direction
        ),
        **response,
    }


def show_text(input, window, pos=(0, 0), colour="#ffffff"):
    textstim = visual.TextStim(
        win=window, font="Courier New", text=input, color=colour, pos=pos, height=22
    )

    textstim.draw()
