"""
This file contains the functions necessary for
creating the interactive response dial at the end of a trial.
To run the 'microsaccade bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from psychopy import event
from psychopy.core import wait
from psychopy.hardware.keyboard import Keyboard
from time import time
from eyetracker import get_trigger
from math import sqrt

SAMPLE_DELAY = 15
"""Time to wait in between eyetracking samples in milliseconds"""


def evaluate_response(change_direction, response):
    if (
        change_direction == response == "clockwise"
        or change_direction == response == "anticlockwise"
    ):
        correct_key = True
    else:
        correct_key = False

    if not response:
        feedback = "missed"
    else:
        feedback = "correct" if correct_key else "incorrect"

    return {
        "correct_key": correct_key,
        "feedback": feedback,
    }


def get_response(
    settings,
    testing,
    eyetracker,
    trial_condition,
    change_direction,
    target_bar,
):
    keyboard: Keyboard = settings["keyboard"]

    # Check for pressed 'q'
    check_quit(keyboard)

    # These timing systems should start at the same time, this is almost true
    idle_reaction_time_start = time()
    keyboard.clock.reset()

    # Check if _any_ keys were prematurely pressed
    prematurely_pressed = [(p.name, p.rt) for p in keyboard.getKeys()]
    keyboard.clearEvents()

    # Wait indefinitely until the participant starts giving an answer
    broke_fixation, last_sample, pressed = sample_while_wait(
        idle_reaction_time_start,
        2000,
        eyetracker,
        settings,
        lambda: keyboard.getKeys(keyList=["z", "m", "q"]),
    )

    # Abort trial if fixation has been broken
    if broke_fixation:
        return

    response_time = time() - idle_reaction_time_start

    if pressed:
        if "q" in pressed:
            raise KeyboardInterrupt()

        if "m" in pressed:
            key = "m"
            response = "clockwise"
            missed = False
            if not testing and eyetracker:
                trigger = get_trigger(
                    "response_right", trial_condition, target_bar, change_direction
                )
                eyetracker.tracker.send_message(f"trig{trigger}")

        elif "z" in pressed:
            key = "z"
            response = "anticlockwise"
            missed = False
            if not testing and eyetracker:
                trigger = get_trigger(
                    "response_left", trial_condition, target_bar, change_direction
                )
                eyetracker.tracker.send_message(f"trig{trigger}")

    else:
        key = None
        response = None
        missed = True
        if not testing and eyetracker:
            trigger = get_trigger(
                "response_missed", trial_condition, target_bar, change_direction
            )
            eyetracker.tracker.send_message(f"trig{trigger}")

    # Make sure keystrokes made during this trial don't influence the next
    keyboard.clearEvents()

    return {
        "response_time_in_ms": round(response_time * 1000, 2),
        "key_pressed": key,
        "premature_pressed": True if prematurely_pressed else False,
        "premature_key": prematurely_pressed[0][0] if prematurely_pressed else None,
        "premature_timing": (
            round(prematurely_pressed[0][1] * 1000, 2) if prematurely_pressed else None
        ),
        "missed": missed,
        "broke_fixation": broke_fixation,
        "last_sample": last_sample,
        **evaluate_response(change_direction, response),
    }


def wait_for_key(key_list, keyboard):
    keyboard: Keyboard = keyboard
    keyboard.clearEvents()
    keys = event.waitKeys(keyList=key_list)

    return keys


def check_quit(keyboard):
    if keyboard.getKeys("q"):
        raise KeyboardInterrupt()


def sample_while_wait(start, waiting_time, eyetracker, settings, stuff_to_do=None):
    broke_fixation = False
    sample = None  # this is necessary in case a button is pressed before the first sample is returned

    # loop over sampling + anything else that needs to be done until time is over
    while (time() - start) * 1000 < (waiting_time - SAMPLE_DELAY):
        loop_start = time()
        if stuff_to_do:
            result = stuff_to_do()  # this keeps checking for key presses
            if result:
                return broke_fixation, sample, result

        sample = eyetracker.sample()
        allowed = check_gaze_position(sample, settings)

        if not allowed:
            broke_fixation = True
            return broke_fixation, sample

        wait(SAMPLE_DELAY / 1000 - (time() - loop_start))

    # the following should wait at most SAMPLE_DELAY
    # so possibly not even worth having, but
    # being very precise is very cool kids.
    wait(waiting_time / 1000 - (time() - start))

    return broke_fixation, sample


def check_gaze_position(sample, settings):
    # Check for circular allowed range of 1 dva radius around middle pixel
    if (
        sqrt(
            (sample[0] - settings["middle_pixel"][0]) ** 2
            + (sample[1] - settings["middle_pixel"][1]) ** 2
        )
        <= settings["allowed_radius"]
    ):
        allowed = True
    # Check for blink values
    elif sample[0] == -32768.0 or sample[1] == -32768.0:
        allowed = True
    # Anything else is not allowed
    else:
        allowed = False

    return allowed
