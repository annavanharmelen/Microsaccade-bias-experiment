"""
This file contains the functions necessary for
creating the interactive response dial at the end of a trial.
To run the 'microsaccade bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from psychopy import event
from psychopy.hardware.keyboard import Keyboard
from time import time
from eyetracker import get_trigger

RESPONSE_DIAL_SIZE = 2


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
    pressed = event.waitKeys(keyList=["z", "m", "q"], maxWait=2)

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
        "premature_keys": prematurely_pressed[0] if prematurely_pressed else None,
        "missed": missed,
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
