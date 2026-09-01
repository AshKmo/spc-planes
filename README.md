# 2D Plane AI Competition
The Swinburne Programming Club has discovered an entry point to the 2D realm and can foresee a variety of ways in which it can be exploited for significant profit.

However, a lot of other organisations have also discovered this realm, and thus a war for control over the realm has emerged.

The SPC has designed an unmanned 2D combat aircraft to assert its dominance over the realm. Your job is to compete with your fellow members to develop the best code for the combat plane, which will fight in a simulation with an identical plane with its own AI.
## OK, now what?
To get started, first make sure you have Python installed, then clone this repository and run `pip install -r requirements.txt` within the repository folder to install the required dependencies.

Start by running `python main.py`. Two planes will fly across the screen firing small bullets.

`plane1_ai.py` contains the code for the blue plane. This is where your code goes. Your task is to edit this file to make the plane smarter.

`plane2_ai.py` contains the code for the enemy plane. The simulation is designed so that the AI for Plane 2 will think that it is Plane 1, which means that you can copy someone else's `plane1_ai.py` into `plane2_ai.py` and it will work as the author intended. Once you've completed your `plane1_ai.py`, share it on the [SPC Discord](https://discord.com/invite/As9fscu6gV) to see if it can beat anyone else's.

`zain_ai.py`, `samson_ai.py` and `zain_ai.py` are example AIs that you can copy into `plane2_ai.py` to fight against your plane.
## Rules
- Your code must not perform input and output (except for debugging)
- Your code also must not depend on any external libraries, excluding NumPy
- Try not to vibecode

More information about how to write the code can be found in `plane1_ai.py`.

Good luck!