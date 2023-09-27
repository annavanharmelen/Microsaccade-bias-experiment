"""
This file contains the functions necessary for
creating and running a full block of trials start-to-finish.
To run the 'microsaccade bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""
import random
from trial import show_text
from response import wait_for_key


def create_block(n_trials):
    if n_trials % 10 != 0:
        raise Exception("Expected number of trials to be divisible by 10.")

    # Create random, but equal distribution of target locations
    locations = n_trials // 10 * 5 * ["left", "right"]
    random.shuffle(locations)
    
    # Create 10% incongruent trials
    congruencies = n_trials // 10 * (9 * ["congruent"] + ["incongruent"])
    random.shuffle(congruencies)

    # Generate random trial lengths
    durations = list(range(500, 3000, 250))
    random.shuffle(durations)

    # Create trial parameters for all trials in one block
    trials = zip(congruencies, locations, durations)

    return list(trials)


def block_break(current_block, n_blocks, avg_score, settings, eyetracker):
    blocks_left = n_blocks - current_block

    show_text(
        f"You scored {avg_score}% correct on the previous block. "
        f"\n\nYou just finished block {current_block}, you {'only ' if blocks_left == 1 else ''}"
        f"have {blocks_left} block{'s' if blocks_left != 1 else ''} left. "
        "Take a break if you want to, but try not to move your head during this break."
        "\n\nPress SPACE when you're ready to continue.",
        settings["window"],
    )
    settings["window"].flip()

    if eyetracker:
        keys = wait_for_key(["space", "c"], settings["keyboard"])
        if "c" in keys:
            eyetracker.calibrate()
            eyetracker.start()
            return True
    else:
        wait_for_key(["space"], settings["keyboard"])

    return False


def long_break(n_blocks, avg_score, settings, eyetracker):
    show_text(
        f"You scored {avg_score}% correct on the previous block. "
        f"\n\nYou're halfway through! You have {n_blocks // 2} blocks left. "
        "Now is the time to take a longer break. Maybe get up, stretch, walk around."
        "\n\nPress SPACE whenever you're ready to continue again.",
        settings["window"],
    )
    settings["window"].flip()

    if eyetracker:
        keys = wait_for_key(["space", "c"], settings["keyboard"])
        if "c" in keys:
            eyetracker.calibrate()
            return True
    else:
        wait_for_key(["space"], settings["keyboard"])

    return False


def finish(n_blocks, settings):
    show_text(
        f"Congratulations! You successfully finished all {n_blocks} blocks!"
        "You're completely done now. Press SPACE to exit the experiment.",
        settings["window"],
    )
    settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])


def quick_finish(settings):
    settings["window"].flip()
    show_text(
        f"You've exited the experiment. Press SPACE to close this window.",
        settings["window"],
    )
    settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])
