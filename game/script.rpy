# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Shield Girl")
define playerName = "You"
define mark = Character("Mark", color="#000000")
define shahaan = Character("Shahaan", color="#000000")
define berto = Character("Berto", color="#000000")
define colin = Character("Colin", color="#000000")
define pranav = Character("Pranav", color="#000000")
define mario = Character("Mario", color="#000000")
define jacob = Character("Jacob", color="#000000")
define talha = Character("Talha", color="#000000")
define brayden = Character("Brayden", color="#000000")
define michael = Character("Michael", color="#000000")
define neil = Character("Neil", color="#000000")
define kanishk = Character("Kanishk", color="#000000")
define luis = Character("Luis", color="#000000")
define isiah = Character("Isaiah", color="#000000")
define ps = Character("Public Safety", color="#000000")
define talha = Character("Talha Bot 9000", color="#000000")
define van = Character("Van", color="#000000")
define mo = Character("Mo", color="#000000")
define erik = Character("Erik", color="#000000")
define logan = Character("Logan", color="#000000")
define y = Character([playerName], color="#FFFFFF")
define shahaan = Character("Shahaan", color="#000000")
define oppasig = Character("Oppa Sig", color="#a82222")
define a_oppasig = Character("Asian Oppa Sig", color="#a82222")
define leather = Character("Asian Leather Jacket Guy", color="#a82222")
define kinetic = Character("Kinetic Footwear Guy", color="#a82222")
define arg = Character("A Random Girl", color="#a82222")
define arg_r = Character("Potentially Racist Girl?", color="#a82222")
define shield_girl = Character("Shield Girl", color="#a82222")
define shield_girl_glitch = Character("{glitch=30}Shield Girl{/glitch}", color="#a82222")
define refactored = Character("Refactored", color="#a82222")
define officer = Character("Public Safety Officer", color="#a82222")
define neil = Character("Neil", color="#a82222")
define kanishk = Character("Kanishk", color="#a82222")

define zion = Character("Zion", color="#000000")
define sweetheart = Character("Leah", color="#000000")
define andrew = Character("Andrew", color="#000000")

define reagan = Character("Ronald Reagan", color="#3c00ff")
define kappa = Character("Underage Kappa affiliate", color="#3c00ff")
define jenna = Character("Jenna Ortega", color="#3c00ff")



define y_nvl = Character([playerName], kind=nvl, image="nighten", callback=Phone_SendSound)
define mark_nvl = Character("Mark", kind=nvl, callback=Phone_ReceiveSound)
define shahaan_nvl = Character("Shahaan", kind=nvl, callback=Phone_ReceiveSound)
define sienna_nvl = Character("Sienna", kind=nvl, callback=Phone_ReceiveSound)

define config.adv_nvl_transition = None
define config.nvl_adv_transition = Dissolve(0.3)

init python:
    global chosen_plants
    global level_outcome
    global current_level
    global current_area
    global is_testing
    global playerName
    global skip_games
    global difficulty_multiplier
    global current_difficulty
    global MC_Name
    playerName = "You"





# for dealing with the minigame part
label game_and_select:
    if skip_games:
        return

    scene blank
    with dissolve

    $ config.rollback_enabled = False
    $ quick_menu = False
    $ _game_menu_screen = None
    $ current_area = level_to_area(current_level)

    call start_plant_select from _call_start_plant_select
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
    call test_game_entry_label from _call_test_game_entry_label
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
        mark "Is this game too hard for you? Should I make it easier?"

        menu: 
            "{b}Yes:{/b} I'm really bad":
                $ current_difficulty = 0.75 * current_difficulty 

            "{b}No:{/b} I've got this dw":
                $ current_difficulty = 1 * current_difficulty 

            "{b}NOOO:{/b} Make it even harder >:)":
                $ current_difficulty = 1.3 * current_difficulty 
        jump game_and_select

    stop music fadeout 2.0
    $ current_difficulty = difficulty_multiplier
    window show

    return


label start:

    image area5:
        "area2"
        pause 10
        glitch("area2")
        pause 0.3
        glitch("area2")
        pause 0.3
        glitch("area2")
        pause 0.3
        glitch("area2")
        pause 0.3
        glitch("clouds")
        pause 0.2
        glitch("clouds")
        pause 0.2
        glitch("clouds")
        pause 0.2
        "clouds"
        pause 20
        glitch("clouds")
        pause 0.2
        glitch("slide1")
        pause 0.2
        glitch("clouds")
        pause 0.2
        glitch("slide1")
        pause 0.2
        glitch("clouds")
        pause 0.2
        glitch("slide1")
        pause 0.2
        "slide1"
        pause 20
        glitch("clouds")
        pause 0.2
        "clouds"
        pause 5
        glitch("slide2")
        pause 0.4
        glitch("slide2")
        pause 0.4
        "slide2"
        pause 20
        glitch("slide2")
        pause 0.4
        glitch("clouds")
        pause 0.2
        glitch("slide2")
        pause 0.4
        glitch("clouds")
        pause 3
        "clouds"
        pause 5
        glitch("slide3")
        pause 0.4
        glitch("slide3")
        pause 0.4
        "slide3"
        pause 20
        glitch("slide3")
        pause 0.4
        glitch("clouds")
        pause 0.2
        glitch("slide3")
        pause 0.4
        glitch("clouds")
        pause 3
        "clouds"
        pause 5
        glitch("slide4")
        pause 0.4
        glitch("slide4")
        pause 0.4
        "slide4"
        pause 20
        glitch("slide4")
        pause 0.4
        glitch("clouds")
        pause 0.2
        glitch("slide4")
        pause 0.4
        glitch("clouds")
        pause 3
        "clouds"
        pause 5
        glitch("slide5")
        pause 0.4
        glitch("slide5")
        pause 0.4
        "slide5"
        pause 20
        glitch("slide5")
        pause 0.4
        glitch("clouds")
        pause 0.2
        glitch("slide5")
        pause 0.4
        glitch("clouds")
        pause 3
        "clouds"
        pause 5
        glitch("slide6")
        pause 0.4
        glitch("slide6")
        pause 0.4
        "slide6"
        pause 20
        glitch("slide6")
        pause 0.4
        glitch("clouds")
        pause 0.2
        glitch("slide6")
        pause 0.4
        glitch("clouds")
        pause 3
        "clouds"
        pause 5
        glitch("slide7")
        pause 0.4
        glitch("slide7")
        pause 0.4
        "slide7"

    $ difficulty_multiplier = 0.2
    $ current_difficulty = difficulty_multiplier

    $ is_testing = False
    $ skip_games = False
    # if is_testing:
    #     scene clouds
    #     show area5
    #     $ current_level = "level90"
    #     $ chosen_plants = ["peashooter", "sunflower", "wallnut", "repeater", "cobcannon"]
    #     call test_game_entry_label from _call_test_game_entry_label_1

    # call ask_difficulty

    $ plants = ["peashooter", "sunflower", "wallnut", "repeater", "iceshooter", "fumeshroom", "jacob", "pranav", "colin", "logan", "cobcannon", "andrew"]
    $ seen_zombies = ["basic", "dog", "conehead", "buckethead", "shield_bearer", "kinetic","officer","van", "mask_shield_bearer", "neil", "kanishk"]
    $ current_level = "level0"
    call game_and_select

    $ playerName = "You"
    $ y = Character(playerName, color="#376e3a")
    $ MCName = playerName
    $ y_nvl = Character(playerName, kind=nvl, image="nighten", callback=Phone_SendSound)
    play music pushing_onwards
    # call intro from _call_intro

    # call ufarm from _call_ufarm

    # call party from _call_party
    
    call alumni

    # This ends the game.

    return
