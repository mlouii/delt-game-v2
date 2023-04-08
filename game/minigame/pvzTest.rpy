define THIS_PATH = 'minigame/'

# XXX: using os.path.join here will actually break because Ren'Py somehow doesn't recognize it
define IMG_DIR = 'images/'
define PEASHOOTER = THIS_PATH + IMG_DIR + 'ps-transparent.png'
define IMG_PS = THIS_PATH + IMG_DIR + 'images/'

init python:
  import pygame
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

    def load_plants(self):
      resize_factor = 0.20
      tile_overlay = im.MatrixColor(im.FactorScale(Image(IMG_PS + "daell4l-91d102e0-ee83-4683-b394-30d70ce60a92-" + "0" + ".png"), resize_factor), im.matrix.opacity(0.5) * im.matrix.contrast(0.5))
      animation_frames = [im.FactorScale(Image(IMG_PS + "daell4l-91d102e0-ee83-4683-b394-30d70ce60a92-" + str(i) + ".png"), resize_factor) for i in range(0, 59)]
      self.images["plants"] = {}
      self.images["plants"]["peashooter"] = {
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
    def __init__(self, num_tiles_width, num_tiles_height):

      self.env_width = config.screen_width * 0.7
      self.env_height = config.screen_height * 0.7

      self.start_x = config.screen_width * 0.15
      self.start_y = config.screen_height * 0.15

      self.tiles = []
      self.tile_width = round(self.env_width / num_tiles_width)
      self.tile_height = round(self.env_height / num_tiles_height)

      self.lighter_color = (48, 176, 77)
      self.dark_color = (48, 143, 69)
      self.variance = (0, 7, 4)
      def rand_color(color):
        return tuple([color[i] + renpy.random.randint(-self.variance[i], self.variance[i]) for i in range(len(color))])

      for i in range(num_tiles_width):
        for j in range(num_tiles_height):

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

      self.health = 100
      self.frames = all_images.images["plants"][self.plant_type]["animation"]
      self.frame = 0

    def render(self, render):
      render.place(self.frames[self.frame], x = self.tile.x, y = self.tile.y)
      return render

    def update(self):
      self.frame = (self.frame + 1) % len(self.frames)

  class PlantsController():
    def __init__(self):
      self.plants = []

    def add_plant(self, tile, plant_type):
      self.plants.append(Plant(tile, plant_type))

    def update(self):
      for plant in self.plants:
        plant.update()

    def render(self, render):
      for plant in self.plants:
        render = plant.render(render)
      return render


  class PvzGameDisplayable(renpy.Displayable):
    def __init__(self):

      self.mouseX = 0
      self.mouseY = 0
      self.plant_selected = "peashooter"

      super(PvzGameDisplayable, self).__init__()
      all_images.load_plants()

      self.environment = EnvironmentBuilder(9, 5)
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

  $ game = PvzGameDisplayable()
  add game

label test_game_entry_label:
  $ renpy.call_screen(_screen_name='game_menu')




