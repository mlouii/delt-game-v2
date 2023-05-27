# image splash glitched:
#     glitch("splashscreen") # reliable slicing
#     pause 0.3
#     glitch("splashscreen", offset=60, randomkey=None) # bigger and always-random slicing
#     pause 0.1
#     repeat

# label splashscreen:
#     scene black
#     with Pause(1)

#     play music intro

#     show splashscreen
#     with dissolve
#     with Pause(1)

#     hide splashscreen

#     show splash glitched
#     with Pause(0.5)

#     hide splash glitched

#     show splashscreen-p at glitch
#     with Pause(0.3)

#     hide splashscreen-p

#     show splashscreen
#     with Pause(0.5)

#     scene black with dissolve
#     with Pause(1)

#     return