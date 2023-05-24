define THIS_PATH = 'minigame/'
define JSON_DIR = THIS_PATH + 'info/'
define IMG_DIR = THIS_PATH + 'images/'
define AUDIO_DIR = THIS_PATH + 'audio/'

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

  def convert_to_2d_list(lst, n=4):
    result = []
    sublist = []
    for i, item in enumerate(lst, 1):
        sublist.append(item)
        if i % 4 == 0:
            result.append(sublist)
            sublist = []
    if sublist:
        result.append(sublist)
    return result

  def recharge_time_to_text(recharge_time):
    if recharge_time == 5:
      return "fast"
    elif recharge_time == 20:
      return "slow"
    elif recharge_time == 40:
      return "very slow"
    else:
      return "Dawg you got a glitch"

  class ConfigLoader_Select():
    def __init__(self, level):
      self.level_config = load_json_from_file(path=JSON_DIR + "levels.json")
      self.level = level
      self.plant_show_order = ["peashooter", "sunflower", "wallnut", "repeater", "iceshooter", "fumeshroom", "pranav", "colin", "cobcannon", "logan", "andrew", "jacob"]
      self.zombie_show_order = ["basic", "dog", "conehead", "buckethead", "shield_bearer", "kinetic","officer","van", "mask_shield_bearer", "neil", "kanishk"]
      self.plant_config = load_json_from_file(path=JSON_DIR + "plants.json")
      self.zombie_config = load_json_from_file(path=JSON_DIR + "zombies.json")

    def get_plant_config(self, plant_name):
      return self.plant_config[plant_name]

    def get_plant_image_config(self, plant_name):
      return self.plant_config["image_data"][plant_name]

    def get_zombie_config(self, zombie_name):
      return self.zombie_config[zombie_name]

    def get_level_config(self):
      return self.level_config[self.level]

  class ImageLoader_Select():
    def __init__(self, config_loader):
      self.config_data = config_loader
      self.images = {}
      self.load_plant_images()
      self.load_zombie_images()
      self.images["sun"] = im.FactorScale(Image(IMG_DIR + "gui/" + "sun" + ".png"), 0.75)
      self.images["select-background"] = im.FactorScale(Image(IMG_DIR + "gui/" + "select-background" + ".png"), 1)
      self.images["opp-background"] = im.FactorScale(Image(IMG_DIR + "gui/" + "opp-background" + ".png"), 1)
      self.images["locked-zombie"] = im.FactorScale(Image(IMG_DIR + "gui/" + "locked-zombie" + ".png"), 0.5)
      self.images["not-today"] = im.FactorScale(Image(IMG_DIR + "gui/" + "not-today" + ".png"), 0.5)


    def load_plant_images(self):
      self.images = {}
      for plant_name in self.config_data.plant_show_order:
        plant_location = IMG_DIR + "plants/" + plant_name
        resize_factor = self.config_data.get_plant_image_config(plant_name)["resize_factor"]
        image_prefix = config_data.get_plant_image_config(plant_name)["image_prefix"]
        self.images[plant_name] = im.FactorScale(Image(plant_location + "/" + image_prefix + "-0" + ".png"), resize_factor)
        self.images[plant_name + "locked"] = im.MatrixColor(self.images[plant_name], im.matrix.brightness(-1))

    def load_zombie_images(self):
      for zombie_name in self.config_data.zombie_show_order:
        zombie_location = IMG_DIR + "zombies/" + zombie_name
        self.images[zombie_name] = im.FactorScale(Image(zombie_location + "/" + zombie_name + ".png"), 0.5)   

  class ZombieCard_Select():
    def __init__(self, zombie_name, x, y, is_locked, is_today, config_data, image_data, zombie_almanac):
      self.zombie_name = zombie_name
      self.x_location = x
      self.y_location = y
      self.is_locked = is_locked
      self.is_today = is_today
      self.config_data = config_data
      self.image_data = image_data
      self.zombie_almanac = zombie_almanac

      self.width = 130
      self.height = 170

      self.image = self.image_data.images["locked-zombie"]
      if not self.is_locked:
        self.image = self.image_data.images[self.zombie_name]

    def process_click(self, x, y):
      if x > self.x_location and x < self.x_location + self.width and y > self.y_location and y < self.y_location + self.height:
        self.zombie_almanac.load_zombie(self.zombie_name)
        return True
      return False

    def render(self, render):
      render.place(self.image, x = self.x_location, y = self.y_location)
      if not self.is_today and not self.is_locked:
        render.place(self.image_data.images["not-today"], x = self.x_location, y = self.y_location)
      return render

  class PlantSeedCard_Select():
    def __init__(self, plant_name, x, y, is_locked, config_data, image_data, almanac):
      self.plant_name = plant_name
      self.x_location = x
      self.y_location = y

      self.original_x = x
      self.original_y = y

      self.target_x = None
      self.target_y = None

      self.is_moving = False
      self.speed = 1

      self.x_distance = None
      self.y_distance = None

      self.y_velocity = None
      self.x_velocity = None

      self.is_locked = is_locked
      self.already_selected = False
      self.width = 130
      self.height = 170
      self.config_data = config_data
      self.image_data = image_data
      self.almanac = almanac
      self.plant_config = self.config_data.get_plant_config(plant_name)
      self.background_solid = Solid((50, 252, 104), xsize=self.width, ysize=self.height)
      self.cost_text = None
      if self.is_locked:
        self.cost_text = Text("???", size = 20)
      else:
        self.cost_text = Text(str(self.plant_config["cost"]), size = 20)

      self.image = None
      if self.is_locked:
        self.image = self.image_data.images[plant_name + "locked"]
      else:
        self.image = self.image_data.images[plant_name]

    def render(self, render):
      render.place(self.background_solid, x = self.x_location, y = self.y_location)
      if self.plant_name == "cobcannon":
        render.place(self.image, x = self.x_location, y = self.y_location+10)
      else:
        render.place(self.image, x = self.x_location+15, y = self.y_location+10)
      render.place(self.cost_text, x = self.x_location+40, y = (self.y_location+self.height)-31)
      render.place(self.image_data.images["sun"], x = (self.x_location+self.width)-40, y = (self.y_location+self.height)-35)
      if self.is_locked:
        self.gray_overlay = Solid((0, 0, 0, 100), xsize=self.width, ysize=self.height)
        render.place(self.gray_overlay, x = self.x_location, y = self.y_location)
      return render

    def process_click(self, x, y, new_slot_x, new_slot_y, can_select):
      if self.is_moving:
        return False
      if x > self.x_location and x < self.x_location + self.width and y > self.y_location and y < self.y_location + self.height:
        if not self.is_locked:
          self.almanac.plant_name = self.plant_name
          if not self.already_selected:
            if can_select:
              self.already_selected = True
              self.target_x = new_slot_x
              self.target_y = new_slot_y
              renpy.play(AUDIO_DIR + "seed-select.mp3", channel = "audio")
            else:
              return False
          else:
            self.already_selected = False
            self.target_x = self.original_x
            self.target_y = self.original_y
          self.is_moving = True
          self.x_distance = self.target_x - self.x_location
          self.y_distance = self.target_y - self.y_location
          return True
      return False

    def snap_to_target(self):
      self.x_location = self.target_x
      self.y_location = self.target_y
      self.is_moving = False
      self.speed = 1

    def update(self):
      if self.is_moving:
        distance = ((self.x_distance ** 2) + (self.y_distance ** 2)) ** 0.5
        if distance > 0:
          angle = math.atan2(self.y_distance, self.x_distance)
          move_speed_x = math.cos(angle) * self.speed
          move_speed_y = math.sin(angle) * self.speed
          self.x_location += move_speed_x
          self.y_location += move_speed_y
          self.speed = 1.1 * self.speed
        if self.y_distance > 0:
          if self.y_location > self.target_y:
            self.snap_to_target()
        else:
          if self.y_location < self.target_y:
            self.snap_to_target()

        if self.x_distance > 0:
          if self.x_location > self.target_x:
            self.snap_to_target()
        else:
          if self.x_location < self.target_x:
            self.snap_to_target()

    def update_selected(self, new_slot_x, new_slot_y):
      self.target_x = new_slot_x
      self.target_y = new_slot_y
      self.is_moving = True
      self.x_distance = self.target_x - self.x_location
      self.y_distance = self.target_y - self.y_location

  class ZombieAlamanac():
    def __init__(self, x_location, y_location, config_data, image_data):
      self.x_location = x_location
      self.y_location = y_location
      self.width = 1000
      self.height = 550
      self.background_solid = Solid((50, 252, 104), xsize=self.width, ysize=self.height)
      self.config_data = config_data
      self.image_data = image_data

      self.zombie_name = None
      self.image = None

      self.text_offset = 300

    def load_zombie(self, zombie_name):
      self.zombie_name = zombie_name

    def add_newlines(self, text, line_length):
      words = text.split()
      lines = []
      current_line = ""

      for word in words:
          if len(current_line) + len(word) <= line_length:
              current_line += word + " "
          else:
              lines.append(current_line.rstrip())
              current_line = word + " "

      lines.append(current_line.rstrip())

      return "\n".join(lines)

    def render(self, render):
      almanac = self.config_data.get_zombie_config(self.zombie_name)["almanac"]
      render.place(self.background_solid, x = self.x_location, y = self.y_location)

      image = im.FactorScale(self.image_data.images[self.zombie_name], 2)
      render.place(image, x = self.x_location+50, y = self.y_location+50)

      name_text = Text(almanac["almanac_name"], size = 50, underline=True)
      render.place(name_text, x = self.x_location+self.text_offset, y = self.y_location+50)
      description_text = Text(self.add_newlines(almanac["description"], 60), size = 20)
      render.place(description_text, x = self.x_location+self.text_offset, y = self.y_location+120)

      param_counter = 1
      #iterate through keys and values in alamanc
      for key, value in almanac.items():
        if key not in ["almanac_name", "description", "story"]:
          key_text = Text(key.capitalize(), size = 20, bold = True)
          value_text = Text(self.add_newlines(value, 30), size = 20)
          render.place(key_text, x = self.x_location+self.text_offset, y = self.y_location+150+(param_counter*30))
          render.place(value_text, x = self.x_location+self.text_offset+200, y = self.y_location+150+(param_counter*30))
          param_counter += 1

      story_text = Text(self.add_newlines(almanac["story"], 80), size = 20)
      render.place(story_text, x = self.x_location+50, y = self.y_location+400)
      return render



  class AlmanacEntry():
    def __init__(self, x_location, y_location, config_data, image_data):
      self.x_location = x_location
      self.y_location = y_location
      self.width = 1000
      self.height = 550
      self.background_solid = Solid((50, 252, 104), xsize=self.width, ysize=self.height)
      self.config_data = config_data
      self.image_data = image_data

      self.plant_name = None
      self.image = None

      self.text_offset = 300

    def load_plant(self, plant_name):
      self.plant_name = plant_name

    def add_newlines(self, text, line_length):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) <= line_length:
                current_line += word + " "
            else:
                lines.append(current_line.rstrip())
                current_line = word + " "

        lines.append(current_line.rstrip())

        return "\n".join(lines)

    def render(self, render):
      extra_x = 0
      if self.plant_name == "cobcannon":
        extra_x = 50
      almanac = self.config_data.get_plant_config(self.plant_name)["almanac"]
      render.place(self.background_solid, x = self.x_location, y = self.y_location)

      image = im.FactorScale(self.image_data.images[self.plant_name], 2)
      render.place(image, x = self.x_location+50, y = self.y_location+50)

      name_text = Text(almanac["almanac_name"], size = 50, underline=True)
      render.place(name_text, x = self.x_location+self.text_offset+extra_x, y = self.y_location+50)
      description_text = Text(self.add_newlines(almanac["description"], 60), size = 20)
      render.place(description_text, x = self.x_location+self.text_offset+extra_x, y = self.y_location+120)

      param_counter = 1
      #iterate through keys and values in alamanc
      for key, value in almanac.items():
        if key not in ["almanac_name", "description", "story"]:
          key_text = Text(key.capitalize(), size = 20, bold = True)
          value_text = Text(self.add_newlines(value, 30), size = 20)
          render.place(key_text, x = self.x_location+self.text_offset+extra_x, y = self.y_location+150+(param_counter*30))
          render.place(value_text, x = self.x_location+self.text_offset+200+extra_x, y = self.y_location+150+(param_counter*30))
          param_counter += 1

      story_text = Text(self.add_newlines(almanac["story"], 80), size = 20)
      render.place(story_text, x = self.x_location+50, y = self.y_location+350)

      sun_cost_text = Text("Xs Off Required", size = 20, bold = True)
      render.place(sun_cost_text, x = self.x_location+50, y = self.y_location+self.height-70)
      sun_cost_text = Text(str(self.config_data.get_plant_config(self.plant_name)["cost"]), size = 20)
      render.place(sun_cost_text, x = self.x_location+250, y = self.y_location+self.height-70)

      recharge_text = Text("Recharge", size = 20, bold = True)
      render.place(recharge_text, x = self.x_location+450, y = self.y_location+self.height-70)
      recharge_text = Text(recharge_time_to_text(self.config_data.get_plant_config(self.plant_name)["recharge_time"]), size = 20)
      render.place(recharge_text, x = self.x_location+650, y = self.y_location+self.height-70)
      return render

  class WarningDisplay():
    def __init__(self, parent):
      self.is_active = False
      self.parent = parent
      self.background_solid = Solid((0, 0, 0, 200), xsize=1900, ysize=1080)
      self.x_location = 0
      self.y_location = 0

    def render(self, render):
      if self.is_active:
        render.place(self.background_solid, x = self.x_location, y = self.y_location)

        warn_text = Text(f"Are you sure? You only have {len(self.parent.chosen_plants)} selected", size = 70, color=(255, 255, 255, 255))
        render.place(warn_text, x = self.x_location+300, y = self.y_location+450)

        yes_button = Solid((255, 50, 50, 255), xsize=500, ysize=100)
        render.place(yes_button, x = self.x_location+300, y = self.y_location+600)

        yes_text = Text("YES FUCK YOU", size = 45, color=(255, 255, 255, 255))
        render.place(yes_text, x = self.x_location+400, y = self.y_location+630)

        no_button = Solid((35, 235, 85, 255), xsize=500, ysize=100)
        render.place(no_button, x = self.x_location+900, y = self.y_location+600)

        no_text = Text("NO", size = 45, color=(255, 255, 255, 255))
        render.place(no_text, x = self.x_location+1000, y = self.y_location+630)
      return render

    def process_click(self, x, y):
      if self.is_active:
        if x > self.x_location+300 and x < self.x_location+800 and y > self.y_location+600 and y < self.y_location+700:
          self.is_active = False
          self.parent.has_ended = True
          return True
        elif x > self.x_location+900 and x < self.x_location+1400 and y > self.y_location+600 and y < self.y_location+700:
          self.is_active = False
          return True
      return False


  class PlantSelectDisplayable(renpy.Displayable):
    def __init__(self, unlocked_plants, num_seed_slots, seen_zombies, level):
      renpy.play(AUDIO_DIR + "choose-your-seeds.mp3", channel = "music")
      renpy.music.set_volume(0.5, channel = "music")
      super(PlantSelectDisplayable, self).__init__()
      self.unlocked_plants = unlocked_plants
      self.seen_zombies = seen_zombies
      self.level = level
      self.max_slots = min(num_seed_slots, len(self.unlocked_plants))
      self.has_ended = False
      self.chosen_plants = []

      self.finish_button_background = Solid((255, 50, 50, 255), xsize=500, ysize=100)
      self.finish_text = Text("OKAY IM DONE", size=45, color=(255, 255, 255, 255))

      self.switch_to_zombie_background = Solid((35, 235, 85, 255), xsize=500, ysize=100)
      self.switch_to_zombie_text = Text("WHO MY OPPS?", size=45, color=(255, 255, 255, 255))

      self.config_data = ConfigLoader_Select(1)
      self.image_data = ImageLoader_Select(self.config_data)

      self.render_order_plants = convert_to_2d_list(self.config_data.plant_show_order)
      self.render_order_zombies = convert_to_2d_list(self.config_data.zombie_show_order)

      self.seed_select_start_x = 100
      self.seed_select_start_y = 350

      self.selected_start_x = 100
      self.selected_start_y = 50
      self.alamac = AlmanacEntry(800, 330, self.config_data, self.image_data)
      self.seed_choices = []
      for i, row in enumerate(self.render_order_plants):
        for j, plant_name in enumerate(row):
          is_locked = True
          if plant_name in self.unlocked_plants:
            is_locked = False
          self.seed_choices.append(PlantSeedCard_Select(plant_name, self.seed_select_start_x+(j*150), self.seed_select_start_y+(i*200), is_locked, self.config_data, self.image_data, self.alamac))
      self.alamac.load_plant("peashooter")
      self.mouseX = 0
      self.mouseY = 0
      self.warning = WarningDisplay(self)

      self.level_config = load_json_from_file(path=JSON_DIR + "levels.json")["level1"]
      self.level_zombies = self.level_config["zombies"]
      self.is_on_zombie_page = False

      self.zombie_almanac = ZombieAlamanac(800, 330, self.config_data, self.image_data)
      self.zombie_almanac.load_zombie("basic")
      self.zombie_cards = []
      for i, row in enumerate(self.render_order_zombies):
        for j, zombie_name in enumerate(row):
          is_locked = True
          if zombie_name in self.seen_zombies:
            is_locked = False
          is_today = False
          if zombie_name in self.level_zombies:
            is_today = True
          self.zombie_cards.append(ZombieCard_Select(zombie_name, self.seed_select_start_x+(j*150), self.seed_select_start_y+(i*200), is_locked,is_today, self.config_data, self.image_data, self.zombie_almanac))
      

    def event(self, ev, x, y, st):
      import pygame
      self.mouseX = x
      self.mouseY = y

      if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
        self.process_click()

      if self.has_ended:
        return self.chosen_plants

    def update(self):
      for plant in self.seed_choices:
        plant.update()

    def render(self, width, height, st, at):
      if self.has_ended:
        return None
      r = renpy.Render(width, height)
      self.update()

      if not self.is_on_zombie_page:
        r.place(self.image_data.images["select-background"], x=0, y=0)
        width = 150 * 4 + 40
        height = 200 * 3 + 40
        brown_background = Solid((139, 69, 19, 250), xsize=width, ysize=height)
        r.place(brown_background, x=self.seed_select_start_x-20, y=self.seed_select_start_y-20)

        for i in range(self.max_slots):
          light_brown_background = Solid((205, 133, 63, 250), xsize=130, ysize=170)
          r.place(light_brown_background, x=self.selected_start_x+(i*150), y=self.selected_start_y)

        for plant in self.seed_choices:
          r.place(light_brown_background, x=plant.original_x, y=plant.original_y)

        for plant in self.seed_choices:
          r = plant.render(r)

        r.place(self.finish_button_background, x=self.seed_select_start_x, y=self.seed_select_start_y+(len(self.render_order_plants)*200))
        r.place(self.finish_text, x=self.seed_select_start_x + 50, y=self.seed_select_start_y+(len(self.render_order_plants)*200) + 30)
        r = self.alamac.render(r)
      else:
        r.place(self.image_data.images["opp-background"], x=0, y=0)
        width = 150 * 4 + 40
        height = 200 * 3 + 40
        brown_background = Solid((139, 69, 19, 250), xsize=width, ysize=height)
        light_brown_background = Solid((205, 133, 63, 250), xsize=130, ysize=170)
        r.place(brown_background, x=self.seed_select_start_x-20, y=self.seed_select_start_y-20)

        for zombie in self.zombie_cards:
          r.place(light_brown_background, x=zombie.x_location, y=zombie.y_location)

        for zombie in self.zombie_cards:
          r = zombie.render(r)

        r = self.zombie_almanac.render(r)


      r.place(self.switch_to_zombie_background, x=1400, y=950)
      r.place(self.switch_to_zombie_text, x=1500, y=980)

      # mouse_text = Text("MouseX: " + str(self.mouseX) + " MouseY: " + str(self.mouseY), size=50, color=(255, 255, 255, 255))
      # r.place(mouse_text, x=self.mouseX-300, y=self.mouseY-300)

      if self.warning.is_active:
        r = self.warning.render(r)

      renpy.redraw(self, 0)
      return r

    def get_chosen_plants(self):
      return self.chosen_plants

    def card_to_chosen_idx(self, card):
      return self.chosen_plants.index(card.plant_name)

    def process_click(self):
      if self.warning.is_active:
        self.warning.process_click(self.mouseX, self.mouseY)
        return True
      if not self.is_on_zombie_page: 
        if self.mouseX > self.seed_select_start_x and self.mouseX < self.seed_select_start_x + 500 and self.mouseY > self.seed_select_start_y+(len(self.render_order_plants)*200) and self.mouseY < self.seed_select_start_y+(len(self.render_order_plants)*200) + 100:
          if len(self.chosen_plants) < self.max_slots:
            self.warning.is_active = True
          else:
            self.has_ended = True
            return True

        if self.mouseX > 1400 and self.mouseX < 1900 and self.mouseY > 950 and self.mouseY < 1050:
          self.is_on_zombie_page = True
          self.switch_to_zombie_text = Text("BACK TO BROTHERS", size=45, color=(255, 255, 255, 255))
          renpy.play(AUDIO_DIR + "splat.mp3", channel = "audio")
          return True

        for plant in self.seed_choices:
          can_select = False
          if len(self.chosen_plants) < self.max_slots:
            can_select = True
          if plant.process_click(self.mouseX, self.mouseY, self.selected_start_x + (len(self.chosen_plants) * 150), self.selected_start_y, can_select):
            if plant.already_selected:
              self.chosen_plants.append(plant.plant_name)
            else:
              idx = self.chosen_plants.index(plant.plant_name)
              plant_names_to_move = self.chosen_plants[idx+1:]
              self.chosen_plants.remove(plant.plant_name)
              seed_cards_to_move = [card for card in self.seed_choices if card.plant_name in plant_names_to_move]
              for card in seed_cards_to_move:
                card.update_selected(self.selected_start_x + (self.card_to_chosen_idx(card) * 150), self.selected_start_y)
            return True
      else:
        if self.mouseX > 1400 and self.mouseX < 1900 and self.mouseY > 950 and self.mouseY < 1050:
          self.is_on_zombie_page = False
          self.switch_to_zombie_text = Text("WHO MY OPPS?", size=45, color=(255, 255, 255, 255))
          renpy.play(AUDIO_DIR + "splat.mp3", channel = "audio")
          return True

        for zombie in self.zombie_cards:
          if not zombie.is_locked:
            if zombie.process_click(self.mouseX, self.mouseY):
              return True

      return False





screen plant_select_menu():
  modal True
  $ plants = ["peashooter", "sunflower", "wallnut", "repeater", "iceshooter", "fumeshroom", "pranav", "colin", "cobcannon", "logan", "andrew", "jacob"]
  $ seen_zombies = ["basic", "conehead", "buckethead", "dog", "van", "shield_bearer", "kinetic", "neil", "kanishk", "mask_shield_bearer", "officer"]
  $ game = PlantSelectDisplayable(plants, 7, seen_zombies, "level1")
  add game


label start_plant_select:
  window hide
  $ quick_menu = False
  $ _game_menu_screen = None
  $ chosen_plants = renpy.call_screen(_screen_name='plant_select_menu')
  $ quick_menu = True

  return