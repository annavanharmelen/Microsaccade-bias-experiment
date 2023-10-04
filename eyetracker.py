"""
This file contains the functions necessary for
connecting and using the eyetracker.
To run the 'microsaccade bias' experiment, see main.py.

made by Anna van Harmelen, 2023, using code by Rose Nasrawi & Baiwei Liu
"""

from lib import eyelinker
from psychopy import event
import os


class Eyelinker:
    """
    usage:

       from eyetracker import Eyelinker

    To initialise:

       eyelinker = Eyelinker(participant, session, window, directory)
       eyelinker.calibrate()
    """

    def __init__(self, participant, session, window, directory) -> None:
        """
        This also connects to the tracker
        """
        self.directory = directory
        self.window = window
        self.tracker = eyelinker.EyeLinker(
            window=window, eye="RIGHT", filename=f"{session}_{participant}.edf"
        )
        self.tracker.init_tracker()

    def start(self):
        self.tracker.start_recording()

    def calibrate(self):
        self.tracker.calibrate()

    def stop(self):
        os.chdir(self.directory)

        self.tracker.stop_recording()
        self.tracker.transfer_edf()
        self.tracker.close_edf()


def get_trigger(frame, condition, target_position, change_direction):
    condition_marker = {"invalid": 1, "valid": 2}[condition]

    if change_direction == "anticlockwise":
        condition_marker += 2

    if target_position == "right":
        condition_marker += 4

    return {
        "stimuli_onset": "1",
        "cue_onset": "2",
        "orientation_change": "3",
        "response_left": "4",
        "response_right": "5",
        "response_missed": "6",
    }[frame] + str(condition_marker)
