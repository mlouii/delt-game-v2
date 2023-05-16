init python:
  import pygame
  import json
  import os
  import itertools
  import math
  import time




screen plant_select_menu():
  modal True
  $ plants = ["peashooter", "repeater", "iceshooter", "wallnut", "sunflower", "cobcannon", "fumeshroom"]
  $ game = PlantSelectDisplayable()
  add game

  if game.has_ended:
    timer 0.1 action Return(True)

label start_plant_select:
  window hide
  $ quick_menu = False
  $ _game_menu_screen = None
  $ renpy.call_screen(_screen_name='pvz_game_menu')
  $ quick_menu = True


  return