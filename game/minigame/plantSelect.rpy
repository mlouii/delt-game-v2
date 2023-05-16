define THIS_PATH = 'minigame/'
define JSON_DIR = THIS_PATH + 'info/'
define IMG_DIR = THIS_PATH + 'images/'

init python:
  import pygame
  import json
  import os
  import itertools
  import math
  import time

  def load_json_from_file(path):
    file_handle = renpy.file(path)
    file_contents = file_handle.read()
    file_handle.close()
    return json.loads(file_contents)

  class ConfigLoader():
    def __init__(self, level):
      self.level_config = load_json_from_file(path=JSON_DIR + "levels.json")
      self.level = level
      self.plant_show_order = ["peashooter", "repeater", "iceshooter", "wallnut", "sunflower", "cobcannon", "fumeshroom", "pranav", "colin", "logan"]
      self.plant_config = load_json_from_file(path=JSON_DIR + "plants.json")

    def get_plant_config(self, plant_name):
      return self.plant_config[plant_name]

    def get_plant_image_config(self, plant_name):
      return self.plant_config["image_data"][plant_name]

    def get_level_config(self):
      return self.level_config[self.level]

  class ImageLoader():
    def __init__(self, config_loader):
      self.config_data = config_loader
      self.images = {}
      self.load_plant_images()


    def load_plant_images(self):
      self.images = {}
      for plant_name in self.config_data.plant_show_order:
        plant_location = IMG_DIR + "plants/" + plant_name
        resize_factor = self.config_data.get_plant_image_config(plant_name)["resize_factor"]
        image_prefix = config_data.get_plant_image_config(plant_name)["image_prefix"]
        self.images[plant_name] = im.FactorScale(Image(plant_location + "/" + image_prefix + "-0" + ".png"), resize_factor)
        self.images[plant_name]["locked"] = im.MatrixColor(self.images[plant_name], im.matrix.brightness(-1))

  class PlantSeedCard():
    def __init__(self, plant_name, x, y):
      self.plant_name = plant_name
      self.x = x
      self.y = y

  class PlantSelectDisplayable(renpy.Displayable):
    def __init__(self, unlocked_plants):
      super(PlantSelectDisplayable, self).__init__()
      self.unlocked_plants = unlocked_plants
      self.has_ended = False
      self.chosen_plants = []

      self.finish_button_background = Solid((0, 0, 0, 0), xsize=500, ysize=300)
      self.finish_text = Text("Finish", size=50, color=(255, 255, 255, 255))

      self.mouseX = 0
      self.mouseY = 0

    def event(self, ev, x, y, st):
      import pygame
      self.mouseX = x
      self.mouseY = y

      if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
        self.process_click()

      if self.has_ended:
        return True

    def render(self, width, height, st, at):
      if self.has_ended:
        return None
      r = renpy.Render(width, height)

      r.place(self.finish_button_background, x=300, y=300)
      r.place(self.finish_text, x=300, y=300)

      mouse_text = Text("MouseX: " + str(self.mouseX) + " MouseY: " + str(self.mouseY), size=50, color=(255, 255, 255, 255))
      r.place(mouse_text, x=self.mouseX, y=self.mouseY)

      renpy.redraw(self, 0)
      return r

    def process_click(self):
      if self.mouseX > 300 and self.mouseX < 800 and self.mouseY > 300 and self.mouseY < 600:
        self.has_ended = True





screen plant_select_menu():
  modal True
  $ plants = ["peashooter", "repeater", "iceshooter", "wallnut", "sunflower", "cobcannon", "fumeshroom"]
  $ game = PlantSelectDisplayable(plants)
  add game

  if game.has_ended:
    timer 0.1 action Return(True)

label start_plant_select:
  window hide
  $ quick_menu = False
  $ _game_menu_screen = None
  $ renpy.call_screen(_screen_name='plant_select_menu')
  $ quick_menu = True

  return