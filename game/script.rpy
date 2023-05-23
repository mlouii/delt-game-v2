﻿# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")

init python:
    global selected_plants
    global level_outcome



# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room
    show eileen happy

    $ config.rollback_enabled = False

    hide eileen

    call start_plant_select
    stop music fadeout 2.0

    # e "waaa"

    # $ chosen_plants = ["jacob", "wallnut", "cobcannon", "iceshooter"]

    # $ text = "You chose " + ", ".join(chosen_plants) + "."
    # # $ type_text = "the type of chosen_plants is " + str(type(chosen_plants)) + "."
    # e "hey [text]"

    # e "goddamn i love dudes"

    # $ level_outcome = "undefined"

    scene area1

    call test_game_entry_label

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    

    # These display lines of dialogue.

    e "Lol I heard that you [level_outcome]"

    e "Once you add a story, pictures, and music, you can release it to the world!"

    # This ends the game.

    return
