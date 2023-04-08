define THIS_PATH = 'minigame/'

# XXX: using os.path.join here will actually break because Ren'Py somehow doesn't recognize it
define IMG_DIR = THIS_PATH + 'images/'
define IMG_PS = THIS_PATH + IMG_DIR + 'peashooter/'

init python:
  import pygame
  import json
  import os
  import itertools

  def send_to_file(filename, text):
    with open(config.gamedir + "/" + filename, "a") as f:
        f.write(text)

  def lighten(color):
        return(color[0], color[1] + 8, color[2] + 4)

  class ImageLoader():
    def __init__(self):
      self.images = {}

    def load_plants(self, plant_types):
      self.images["plants"] = {}
      resize_factor = 0.20

      for plant_name in plant_types:
        tile_overlay = im.MatrixColor(im.FactorScale(Image(IMG_DIR + plant_name + "/daell4l-91d102e0-ee83-4683-b394-30d70ce60a92-" + "0" + ".png"), resize_factor), im.matrix.opacity(0.5) * im.matrix.contrast(0.5))
        animation_frames = [im.FactorScale(Image(IMG_DIR + plant_name + "/daell4l-91d102e0-ee83-4683-b394-30d70ce60a92-" + str(i) + ".png"), resize_factor) for i in range(0, 59)]
        self.images["plants"][plant_name] = {
          "overlay": tile_overlay,
          "animation": animation_frames
        }

    def return_overlays(self):
      plants = self.images["plants"].keys()
      overlays = {plant:self.images["plants"][plant]["overlay"] for plant in plants}
      return overlays

  all_images = ImageLoader()

  class Tile():
    def __init__(self, x, y, width, height, color):
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.color = color
      self.is_planted = False
      self.is_hovered = False
      self.plant_selected = None

      self.overlays = all_images.return_overlays()

      self.drawables = {
        "ground": Solid(self.color, xsize=self.width, ysize=self.height),
        "overlay": None
      }

    def render(self, render):
      drawables = self.drawables.copy()
      if self.is_hovered:
        drawables["ground"] = Solid(lighten(lighten(self.color)), xsize=self.width, ysize=self.height)
        if self.plantable():
          drawables["overlay"] = self.overlays[self.plant_selected]

      render.place(drawables["ground"], x = self.x, y = self.y)

      if drawables["overlay"] is not None:
        render.place(drawables["overlay"], x = self.x, y = self.y)

      return render

    def plantable(self):
      return not self.is_planted and self.plant_selected is not None

    def visit(self):
      return [value for value in self.drawables.values() if value is not None]

    def coordinates(self):
      return ((self.x, self.y), (self.x + self.width, self.y + self.height))

  class EnvironmentBuilder():
    def __init__(self, level_config):

      self.env_width = config.screen_width * level_config["width_multiplier"]
      self.env_height = config.screen_height * level_config["height_multiplier"]

      self.start_x = config.screen_width * level_config["start_x"]
      self.start_y = config.screen_height * level_config["start_y"]

      self.tiles = []
      self.tile_width = round(self.env_width / level_config["num_cols"])
      self.tile_height = round(self.env_height / level_config["num_rows"])

      self.lighter_color = level_config["lighter_color"]
      self.dark_color = level_config["dark_color"]
      self.variance = level_config["variance"]

      def rand_color(color):
        return tuple([color[i] + renpy.random.randint(-self.variance[i], self.variance[i]) for i in range(len(color))])

      for i in range(level_config["num_cols"]):
        for j in range(level_config["num_rows"]):

          color = None
          if i % 2 == 0:
            color_seed = self.lighter_color
            color = rand_color(color_seed)
          else:
            color_seed = self.dark_color
            color = rand_color(color_seed)

          if j % 2 == 0:
            color = lighten(color)
          self.tiles.append(Tile(i * self.tile_width + self.start_x, j * self.tile_height + self.start_y, self.tile_width, self.tile_height, color))

    def render(self, render):
      for tile in self.tiles:
        render = tile.render(render)
      return render

    def pos_to_tile(self, x, y):
      for tile in self.tiles:
        ((x1, y1), (x2, y2)) = tile.coordinates()
        if x1 <= x <= x2 and y1 <= y <= y2:
          return tile
      return None

    def update(self, state):
      x, y = state["mouseX"], state["mouseY"]
      tile = self.pos_to_tile(x, y)
      if tile is not None:
        for t in self.tiles:
          t.is_hovered = False
        tile.is_hovered = True
        tile.plant_selected = state["plant_selected"]

    def visit(self):
      return list(itertools.chain(*[tile.visit() for tile in self.tiles]))

  class Plant():
    def __init__(self, tile, plant_type):
      self.tile = tile
      self.plant_type = plant_type
      self.is_dead = False

      self.health = 100
      self.frames = all_images.images["plants"][self.plant_type]["animation"]
      self.frame = 0

    def render(self, render):
      render.place(self.frames[self.frame], x = self.tile.x, y = self.tile.y)
      return render

    def update(self):
      if self.health <= 0:
        self.is_dead = True

      self.frame = (self.frame + 1) % len(self.frames)

  class PlantsController():
    def __init__(self):
      self.plants = []

    def add_plant(self, tile, plant_type):
      self.plants.append(Plant(tile, plant_type))

    def update(self):
      self.plants = [plant for plant in self.plants if not plant.is_dead]

      for plant in self.plants:
        plant.update()

    def render(self, render):
      for plant in self.plants:
        render = plant.render(render)
      return render


  class PvzGameDisplayable(renpy.Displayable):
    def __init__(self, level):

      self.level_config = None
      file_handle = renpy.file("minigame/levels/level" + str(level) + ".json")
      file_contents = file_handle.read()
      file_handle.close()
      self.level_config = json.loads(file_contents)

      self.mouseX = 0
      self.mouseY = 0
      self.plant_selected = "peashooter"

      super(PvzGameDisplayable, self).__init__()
      all_images.load_plants(["peashooter"])

      self.environment = EnvironmentBuilder(self.level_config)
      self.plants = PlantsController()

    def visit(self):
      return self.environment.visit()

    def make_state(self):
      return {
        "mouseX": self.mouseX,
        "mouseY": self.mouseY,
        "plant_selected": self.plant_selected,
      }

    def process_click(self):
      current_state = self.make_state()
      if self.plant_selected is not None:
        tile = self.environment.pos_to_tile(self.mouseX, self.mouseY)
        if tile is not None and tile.plantable():
          tile.is_planted = True
          self.plants.add_plant(tile, self.plant_selected)
        

    def render(self, width, height, st, at):

      current_state = self.make_state()
      self.environment.update(current_state)
      self.plants.update()

      r = renpy.Render(width, height)
      r = self.environment.render(r)
      r = self.plants.render(r)
      renpy.redraw(self, 0)
      return r

    def event(self, ev, x, y, st):
      import pygame
      self.mouseX = x
      self.mouseY = y

      if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
        self.process_click()

      # send_to_file("logz.txt", str(self.mouseX) + " " + str(self.mouseY) + "\n")
    
screen game_menu():
  modal True

  frame:
    xalign 0.5
    yalign 0.5
    xsize 400
    ysize 400

    vbox:
      text "This is a test of the elements of the game menu screen."
      label "Game Menu" xalign 0.5
      label "Lets give it a shot" xalign 0.5
      text "This is a test of the elements of the game menu screen."

  $ game = PvzGameDisplayable(1)
  add game

label test_game_entry_label:
  $ renpy.call_screen(_screen_name='game_menu')




