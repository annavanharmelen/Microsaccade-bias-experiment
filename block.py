"""
This file contains the functions necessary for
creating and running a full block of trials start-to-finish.
To run the 'microsaccade bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""
import random
from stimuli import show_text
from response import wait_for_key


def create_blocks(
    valid_trials, invalid_trials, n_blocks, n_block_trials, predictability
):
    if len(valid_trials) % 40 != 0 or len(invalid_trials) % 40 != 0:
        raise Exception("Expected both numbers of trials to be divisible by 40.")

    # Determine number of (in)valid trials per block
    n_invalid_trials = n_block_trials * (100 - predictability) // 100
    n_valid_trials = n_block_trials * predictability // 100

    # Create list of blocks
    blocks = [[] for _ in range(n_blocks)]

    # Trials are already in random order, they just need to be cut into smaller blocks
    for n_block in range(n_blocks):
        blocks[n_block].extend(
            valid_trials[n_block * n_valid_trials : (n_block + 1) * n_valid_trials]
        )
        blocks[n_block].extend(
            invalid_trials[
                n_block * n_invalid_trials : (n_block + 1) * n_invalid_trials
            ]
        )
        random.shuffle(blocks[n_block])

    return blocks


def create_trial_list(n_trials, validity: str):
    if n_trials % 40 != 0:
        raise Exception(
            "Expected number of trials to be divisible by 40, otherwise perfect factorial combinations are not possible."
        )

    if validity != "valid" and validity != "invalid":
        raise Exception("Expected validity of trial to be either 'valid' or 'invalid'.")

    # Generate equal distribution of target locations
    locations = n_trials // 2 * ["left"] + n_trials // 2 * ["right"]

    # Generate equal distribution of rotation directions,
    # that co-occur equally with the target locations
    directions = 2 * (n_trials // 4 * ["clockwise"] + n_trials // 4 * ["anticlockwise"])

    # Generate equal distribution of trial lengths,
    # that co-occur equally with both target locations and directions
    durations = n_trials // 10 * list(range(500, 3201, 300))

    # Add validity to all trials
    validities = [validity] * n_trials

    # Create trial parameters for all trials
    trials = list(zip(locations, directions, durations, validities))
    random.shuffle(trials)

    return trials


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
        
    # Make sure the keystroke from starting the experiment isn't saved
    settings["keyboard"].clearEvents()

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

    # Make sure the keystroke from starting the experiment isn't saved
    settings["keyboard"].clearEvents()

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
