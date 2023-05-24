# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Shield Girl")
define mark = Character("Mark", color="#000000")
define you = Character("You", color="#a83232")

init python:
    global chosen_plants
    global level_outcome
    global current_level
    global current_area
    global is_testing




# The game starts here.

label game_and_select:
    scene blank
    with dissolve

    $ config.rollback_enabled = False
    $ quick_menu = False
    $ _game_menu_screen = None
    $ current_area = level_to_area(current_level)

    call start_plant_select
    stop music fadeout 2.0

    if (len(chosen_plants) == 0):
        $ quick_menu = False
        show mark 
        with vpunch
        mark "You dumb as hell"
        mark "You aint need nobody to help you???"
        mark "Fuck do you think you are"
        mark "Stupid"

        hide mark 
        with fade

        jump game_and_select
        
        

    scene expression current_area with dissolve
    call test_game_entry_label
    $ preferences.set_volume(0.1, "main")

    $ config.rollback_enabled = True

    if (level_outcome == "lost"):
        $ quick_menu = False
        stop music fadeout 0.5
        scene blank
        with dissolve

        show mark
        with vpunch

        mark "Wow you're actually so bad at this game"
        mark "How about we try this again?"

        jump game_and_select
    stop music fadeout 2.0
    window show

    return

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    $ is_testing = True
    if is_testing:
        $ chosen_plants = ["iceshooter", "wallnut", "fumeshroom", "pranav", "colin", "cobcannon"]
        call test_game_entry_label

    scene ufarm-sunny
    with fade

    show shield-girl2 at right
    with moveinright

    e "Ima hit you with this table fucker"

    you "No dont do it im pussy"

    e "Nobody loves you"

    hide shield-girl2

    $ current_level = "level1"
    call game_and_select
    show ufarm-sunny

    show shield-girl2
    

    e "Lol I heard that you [level_outcome]"

    # This ends the game.

    return
