
define THIS_PATH = 'minigame/'

# XXX: using os.path.join here will actually break because Ren'Py somehow doesn't recognize it
define IMG_DIR = THIS_PATH + 'images/'
define JSON_DIR = THIS_PATH + 'info/'

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

  zombie_config = load_json_from_file(path=JSON_DIR + "zombies.json")
  plant_config = load_json_from_file(path=JSON_DIR + "plants.json")
  projectile_config = load_json_from_file(path=JSON_DIR + "projectiles.json")

  delta_time = 0.0
  delta_multiplier = 70

  def send_to_file(filename, text):
    with open(config.gamedir + "/" + filename, "a") as f:
        f.write(text)

  def lighten(color):
        return(color[0], color[1] + 8, color[2] + 4)

  class ConfigLoader():
    def __init__(self):
      self.plants = plant_config
      self.zombies = zombie_config
      self.projectiles = projectile_config

    def get_zombie_config(self, zombie_type):
      return self.zombies[zombie_type]

    def get_zombie_image_config(self, animation_type):
      return self.zombies["image_data"][animation_type]

    def get_zombie_motion_config(self, motion_type):
      return self.zombies["motion_data"][motion_type]

    def get_plant_config(self, plant_type):
      return self.plants[plant_type]
    
    def get_plant_image_config(self, animation_type):
      return self.plants["image_data"][animation_type]

    def get_projectile_config(self, projectile_type):
      return self.projectiles[projectile_type]
      
    def modify_plant_image_size(self, animation_type, resize_factor):
      image_config = self.get_plant_image_config(animation_type)
      image_config["height"] = image_config["height"] * resize_factor
      image_config["width"] = image_config["width"] * resize_factor
      image_config["joint_x"] = image_config["joint_x"] * resize_factor
      image_config["joint_y"] = image_config["joint_y"] * resize_factor
      image_config["projectile_spawn_x"] = image_config["projectile_spawn_x"] * resize_factor
      image_config["projectile_spawn_y"] = image_config["projectile_spawn_y"] * resize_factor
      self.plants["image_data"][animation_type] = image_config

    def modify_projectile_image_size(self, projectile_name, resize_factor):
      image_config = self.get_projectile_config(projectile_name)
      image_config["height"] = image_config["height"] * resize_factor
      image_config["width"] = image_config["width"] * resize_factor
      image_config["center_x"] = image_config["center_x"] * resize_factor
      image_config["center_y"] = image_config["center_y"] * resize_factor
      self.projectiles[projectile_name] = image_config
      
    def modify_zombie_image_size(self, animation_type, resize_factor):
        image_config = self.get_zombie_image_config(animation_type)
        if image_config["class"] == "zombie":
            for part_type in image_config["parts"]:
              image_config[part_type]["height"] = image_config[part_type]["height"] * resize_factor
              image_config[part_type]["width"] = image_config[part_type]["width"] * resize_factor
              
              if part_type != "torso":
                  image_config[part_type]["joint_x"] = image_config[part_type]["joint_x"] * resize_factor
                  image_config[part_type]["joint_y"] = image_config[part_type]["joint_y"] * resize_factor
              
              if part_type == "torso":
                  for item in image_config[part_type].keys():
                      if item.endswith("_joint"):
                          image_config[part_type][item]["x"] = image_config[part_type][item]["x"] * resize_factor
                          image_config[part_type][item]["y"] = image_config[part_type][item]["y"] * resize_factor

        self.zombies["image_data"][animation_type] = image_config
        
        
  class ImageLoader():
    def __init__(self):
      self.images = {}

    def load_plants(self, plant_types):
      self.images["plants"] = {}
      resize_factor = 0.20

      for plant_name in plant_types:
        plant_location = IMG_DIR + "plants/" + plant_name
        animation_type = config_data.get_plant_config(plant_name)["animation_type"]
        resize_factor = config_data.get_plant_image_config(animation_type)["resize_factor"]
        image_prefix = config_data.get_plant_image_config(plant_name)["image_prefix"]
        num_frames = config_data.get_plant_image_config(plant_name)["num_frames"]

        config_data.modify_plant_image_size(animation_type, resize_factor=resize_factor)

        tile_overlay = im.MatrixColor(im.FactorScale(Image(plant_location + "/" + image_prefix + "-0" + ".png"), resize_factor), im.matrix.opacity(0.5) * im.matrix.contrast(0.5))
        animation_frames = [im.FactorScale(Image(plant_location + "/" + image_prefix + "-" + str(i) + ".png"), resize_factor) for i in range(num_frames)]
        self.images["plants"][plant_name] = {
          "overlay": tile_overlay,
          "animation": animation_frames
        }

    def load_zombies(self, zombie_types):
      self.images["zombies"] = {}
      for zombie_name in zombie_types:
        zombie_location = IMG_DIR + "zombies/" + zombie_name
        animation_type = config_data.get_zombie_config(zombie_name)["animation_type"]
        resize_factor = config_data.get_zombie_image_config(animation_type)["resize_factor"]

        config_data.modify_zombie_image_size(animation_type, resize_factor=resize_factor)
        self.images["zombies"][zombie_name] = {
          "torso": im.FactorScale(Image(zombie_location + "/torso.png"), resize_factor),
          "head": im.FactorScale(Image(zombie_location + "/head.png"), resize_factor),
          "legs": im.FactorScale(Image(zombie_location + "/legs.png"), resize_factor),
          "arms": im.FactorScale(Image(zombie_location + "/arms.png"), resize_factor)
        }

    def load_projectiles(self, projectile_types):
      self.images["projectiles"] = {}
      for projectile_name in projectile_types:
        projectile_location = IMG_DIR + "projectiles/" + projectile_name + ".png"
        resize_factor = config_data.get_projectile_config(projectile_name)["resize_factor"]
        config_data.modify_projectile_image_size(projectile_name, resize_factor=resize_factor)
        self.images["projectiles"][projectile_name] = {
          "image": im.FactorScale(Image(projectile_location), resize_factor)
        }
      
      


    def return_overlays(self):
      plants = self.images["plants"].keys()
      overlays = {plant:self.images["plants"][plant]["overlay"] for plant in plants}
      return overlays

  # These are the global variables
  all_images = ImageLoader()
  config_data = ConfigLoader()

  class Tile():
    def __init__(self, x_location, y_location, row_id, lane_id, width, height, color):
      self.x_location = x_location
      self.y_location = y_location
      self.lane_id = lane_id
      self.row_id = row_id

      self.target_location_x = x_location + int(width/2)
      self.target_location_y = y_location + int(0.8 * height)

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

      render.place(drawables["ground"], x = self.x_location, y = self.y_location)

      if drawables["overlay"] is not None:
        plant_image_config = config_data.get_plant_image_config(self.plant_selected)
        x_location = self.target_location_x - plant_image_config["joint_x"]
        y_location = self.target_location_y - plant_image_config["joint_y"]
        render.place(drawables["overlay"], x = x_location, y = y_location)

      return render

    def plantable(self):
      return not self.is_planted and self.plant_selected is not None

    def visit(self):
      return [value for value in self.drawables.values() if value is not None]

    def coordinates(self):
      return ((self.x_location, self.y_location), (self.x_location + self.width, self.y_location + self.height))

  class EnvironmentBuilder():
    def __init__(self, level_config, game: PvzGameDisplayable):

      self.game = game
      self.num_rows = level_config["num_rows"]

      self.env_width = config.screen_width * level_config["width_multiplier"]
      self.env_height = config.screen_height * level_config["height_multiplier"]

      self.start_x = config.screen_width * level_config["start_x"]
      self.start_y = config.screen_height * level_config["start_y"]

      self.tiles = []
      self.tile_width = round(self.env_width / level_config["num_cols"])
      self.tile_height = round(self.env_height / level_config["num_rows"])

      # This will eventually be updated to be the Lanes class
      self.lanes = [[] for i in range(level_config["num_rows"])]

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

          new_tile =Tile(i * self.tile_width + self.start_x, j * self.tile_height + self.start_y, i, j ,self.tile_width, self.tile_height, color)
          self.tiles.append(new_tile)
          self.lanes[j].append(new_tile)

    def gen_lanes(self):
      lanes = Lanes(len(self.lanes))
      for j in range(self.num_rows):
        lanes.assign_tiles(j, self.lanes[j])
      self.lanes = lanes
      return lanes
    
    def update(self, state):
      x, y = state["mouseX"], state["mouseY"]
      tile = self.lanes.pos_to_tile(x, y)
      if tile is not None:
        for t in self.tiles:
          t.is_hovered = False
        tile.is_hovered = True
        tile.plant_selected = state["plant_selected"]

    def process_click(self):
      # current_state = self.game.make_state()

      for z in self.zombies:
        z.motion_type = "attack"
        z.update_motion()

        choice = (renpy.random.choice(z.body_parts))
        if choice.part_name != "torso":
          choice.status = "detached"

      if self.plant_selected is not None:
        tile = self.environment.pos_to_tile(self.mouseX, self.mouseY)
        if tile is not None and tile.plantable():
          tile.is_planted = True
          self.lanes.add_plant(tile, self.plant_selected)

    def visit(self):
      return list(itertools.chain(*[tile.visit() for tile in self.tiles]))

  class Projectile():
    def __init__(self, plant, projectile_type):
      self.plant = plant
      self.projectile_type = projectile_type
      self.lane = plant.lane

      self.projectile_config = config_data.get_projectile_config(self.projectile_type)
      self.damage = self.projectile_config["damage"]
      self.speed = self.projectile_config["speed"]
      self.pierce = self.projectile_config["pierce"]
      self.center_x = self.projectile_config["center_x"]
      self.center_y = self.projectile_config["center_y"]

      self.image = all_images.images["projectiles"][self.projectile_type]["image"]
      self.projectile_config = config_data.get_projectile_config(self.projectile_type)

      self.plant_spawn_x = self.plant.x_location + self.plant.plant_image_config["projectile_spawn_x"]
      self.plant_spawn_y = self.plant.y_location + self.plant.plant_image_config["projectile_spawn_y"]

      self.x_location = self.plant_spawn_x - self.center_x
      self.y_location = self.plant_spawn_y - self.center_y

      self.active = True
      self.damaged_zombies = []

    def render(self, render):
      render.place(self.image, x = self.x_location, y= self.y_location)
      return render

    def update(self):
      if self.active:
        self.x_location += self.speed * delta_multiplier * delta_time
      
      if self.x_location > config.screen_width:
        self.active = False

    def check_reference_in_list(self, ref_obj, obj_list):
        for obj in obj_list:
            if ref_obj is obj:
                return True
        return False

    def check_collision(self, zombie):
      if self.active:
        if self.lane is zombie.lane:
          if abs(self.x_location - zombie.x_location) < (zombie.hitbox_distance/5) and zombie.is_dead is False:
            if self.check_reference_in_list(zombie, self.damaged_zombies) is False:
              zombie.damage(self.damage)
              self.damaged_zombies.append(zombie)
              if len(self.damaged_zombies) >= self.pierce:
                self.active = False


  class Plant():
    def __init__(self, tile, lane, plant_type):
      self.tile = tile
      self.lane = lane
      self.plant_type = plant_type
      self.is_dead = False

      self.plant_config = config_data.get_plant_config(self.plant_type)
      self.health = self.plant_config["health"]
      self.animation_type = self.plant_config["animation_type"]
      self.hitbox_distance = self.plant_config["hitbox_distance"]

      self.does_spawn_projectile = self.plant_config["spawn_projectile"]
      self.projectile_type = None
      if self.does_spawn_projectile:
        self.projectile_type = self.plant_config["projectile_type"]

      self.frames = all_images.images["plants"][self.plant_type]["animation"]
      self.plant_image_config = config_data.get_plant_image_config(self.plant_type)
      self.frame = 0

      self.x_location = self.tile.target_location_x - self.plant_image_config["joint_x"]
      self.y_location = self.tile.target_location_y - self.plant_image_config["joint_y"]

    def render(self, render):
      render.place(self.frames[self.frame], x = self.x_location, y = self.y_location)
      return render

    def die(self):
      self.tile.is_planted = False
      self.is_dead = True

    def damage(self, damage):
      self.health -= damage
      if self.health <= 0:
        self.die()

    def attack(self):
      if self.does_spawn_projectile:
        self.lane.add_projectile(Projectile(self, self.projectile_type))
      else:
        return None

    def check_collision(self, zombie):
      if zombie.lane is self.lane:
        if abs(zombie.x_location - zombie.hitbox_distance - self.x_location) <= self.hitbox_distance:
          return True
      else: 
        return False

    def update(self):
      if self.health <= 0:
        self.die()

      self.frame = (self.frame + 1) % len(self.frames)

  class Body_Part():
    def __init__(self, zombie, part_name):
      self.zombie = zombie
      self.animation_type = zombie.animation_type
      self.zombie_image_config = config_data.get_zombie_image_config(self.animation_type)
      self.part_name = part_name
      self.part_type = part_name

      self.status = "attached"
      self.velocity_y = -4
      self.velocity_x = 1
      self.zombie_x_timestamp = None
      self.distance_fallen = 0
      self.fade_start_time = None

      if self.part_name in ["left_arm", "right_arm"]:
        self.part_type = "arms"

      if self.part_name in ["left_leg", "right_leg"]:
        self.part_type = "legs"

      self.motion_config = config_data.get_zombie_motion_config(self.zombie.motion_type)[self.part_name]

      self.limit = None
      self.direction = None
      self.motion_type = None
      self.angle = None
      self.update_motion_params()

      self.image = all_images.images["zombies"][self.zombie.zombie_type][self.part_type]
      self.joint_location_x = 0
      self.joint_location_y = 0
      self.target_location_x = 0
      self.target_location_y = 0
      self.image_height = self.zombie_image_config[self.part_type]["height"]
      self.image_width = self.zombie_image_config[self.part_type]["width"]

      if self.part_type != "torso":
        self.joint_location_x = self.zombie_image_config[self.part_type]["joint_x"]
        self.joint_location_y = self.zombie_image_config[self.part_type]["joint_y"]
        self.target_location_x = self.zombie_image_config["torso"][self.part_name + "_joint"]["x"]
        self.target_location_y = self.zombie_image_config["torso"][self.part_name + "_joint"]["y"]

    def process_rotation(self):
      transformed_image = Transform(self.image, rotate=self.angle, anchor = (0, 0), transform_anchor = True)
      # Calculate the offset of the joint after rotation
      dx = self.joint_location_x
      dy = self.joint_location_y
      current_angle = math.atan2(dy, dx)
      new_angle = current_angle + math.radians(self.angle)

      new_dx = dx * math.cos(math.radians(self.angle)) - dy * math.sin(math.radians(self.angle))
      new_dy = dx * math.sin(math.radians(self.angle)) + dy * math.cos(math.radians(self.angle))

      # Calculate the position of the transformed image
      x_location = self.zombie.x_location + self.target_location_x - new_dx
      y_location = self.zombie.y_location + self.target_location_y - new_dy
      return transformed_image, x_location, y_location

    def render(self, render):
      if self.status == "attached":
        if self.motion_type == None:
          transformed_image = Transform(self.image, rotate=self.angle, anchor = (0, 0), transform_anchor = True)
          # Calculate the position of the transformed image
          x_location = self.zombie.x_location + self.target_location_x - self.joint_location_x
          y_location = self.zombie.y_location + self.target_location_y - self.joint_location_y
          render.place(transformed_image, x=x_location, y=y_location)
        elif(self.motion_type == "rotate"):
          transformed_image, x_location, y_location = self.process_rotation()
          render.place(transformed_image, x=x_location, y=y_location)

      elif self.status == "detached":
        if self.zombie_x_timestamp == None:
          self.zombie_x_timestamp = self.zombie.x_location
          
        x_location = self.zombie_x_timestamp + self.target_location_x - self.joint_location_x
        y_location = self.zombie.y_location + self.target_location_y - self.joint_location_y + self.distance_fallen
        render.place(self.image, x=x_location, y=y_location)
        
      elif self.status == "fading":
        if self.fade_start_time == None:
          self.fade_start_time = time.time()
        elapsed = min((time.time() - self.fade_start_time), 1)
        x_location = self.zombie_x_timestamp + self.target_location_x - self.joint_location_x
        y_location = self.zombie.y_location + self.target_location_y - self.joint_location_y + self.distance_fallen
        render.place(self.image, x=x_location, y=y_location)
      return render

    def update(self):
      if self.status == "attached":
        if self.motion_type == "rotate":
          self.angle += (self.direction * self.motion_config["speed"][str(self.direction)] * delta_time * delta_multiplier)
          if (self.angle < self.limit[0]):
            self.direction = 1
          if (self.angle > self.limit[1]):
            self.direction = -1

      elif self.status == "detached":
        if self.zombie_x_timestamp == None:
          self.zombie_x_timestamp = self.zombie.x_location

        self.target_location_x += self.velocity_x * delta_time * delta_multiplier
        self.distance_fallen += self.velocity_y * delta_time * delta_multiplier
        self.velocity_y += 0.3

        if self.distance_fallen > (self.zombie_image_config["fall_height"] - self.target_location_y):
          self.velocity_y = 0
          self.velocity_x = 0
          self.status = "fading"
      elif self.status == "fading":
        if self.fade_start_time == None:
          self.fade_start_time = time.time()
        if time.time() - self.fade_start_time > 0.2:
          self.status = "gone"

    def update_motion_params(self):
      self.motion_config = config_data.get_zombie_motion_config(self.zombie.motion_type)[self.part_name]
      if self.motion_config["type"] == "rotate":
        self.limit = self.motion_config["limit"]
        self.direction = self.motion_config["start_direction"]
        self.motion_type = self.motion_config["type"]
        self.angle = self.motion_config["start_angle"]
      else:
        self.motion_type = None

      

  class Zombie():
    def __init__(self, x_location, y_location, zombie_type, lane):
      self.x_location = x_location
      self.y_location = y_location
      self.lane = lane
      self.zombie_type = zombie_type
      self.animation_type = config_data.get_zombie_config(zombie_type)["animation_type"]
      self.image_config = config_data.get_zombie_image_config(self.animation_type)

      self.motion_type = renpy.random.choice(config_data.get_zombie_config(zombie_type)["motions"])
      self.motion_config = config_data.get_zombie_motion_config(self.motion_type)
      self.status = "moving"

      self.is_dead = False
      self.should_delete = False

      self.health = zombie_config[self.zombie_type]["health"]
      self.speed = zombie_config[self.zombie_type]["speed"]
      self.attack = zombie_config[self.zombie_type]["attack"]
      self.hitbox_distance = zombie_config[self.zombie_type]["hitbox_distance"]

      self.body_parts = [Body_Part(self, part_name) for part_name in self.image_config["part_name_order"]]

      self.target_plant = None

    def render(self, render):
      for body_part in self.body_parts:
        render = body_part.render(render)
      return render

    def update_motion(self):
      self.motion_config = config_data.get_zombie_motion_config(self.motion_type)
      for body_part in self.body_parts:
        body_part.update_motion_params()

    def check_damage_limb_detach(self):
      info = self.image_config["damage_fall_order"]
      for part_name in info.keys():
        if self.health <= (info[part_name] * zombie_config[self.zombie_type]["health"]):
          part = [part for part in self.body_parts if part.part_name == part_name]
          if len(part) > 0:
            part[0].status = "detached"

    def damage(self, damage):
      self.health -= damage
      self.check_damage_limb_detach()

    def start_eating(self, plant):
      self.target_plant = plant
      self.motion_type = "attack"
      self.update_motion()

    def update(self):
      if self.motion_config["moving"]:
        self.x_location -= (self.speed * delta_time * delta_multiplier)

      if hasattr(self, "target_plant") and self.target_plant is not None: # check if target_plant still exists
        self.target_plant.damage(self.attack/10)

        if self.target_plant.is_dead:
          self.target_plant = None
          self.motion_type = renpy.random.choice(config_data.get_zombie_config(self.zombie_type)["motions"])
          self.update_motion()

      if self.health <= 0:
        self.speed = 0
        self.is_dead = True

      if self.x_location < -10:
        self.should_delete = True
        self.is_dead = True

      head = [part for part in self.body_parts if part.part_name == "head"]
      if not head or head[0].status == "gone":
        self.should_delete = True

      self.body_parts = [part for part in self.body_parts if part.status != "gone"]
      for body_part in self.body_parts:
        body_part.update()

  class Lane():
    def __init__(self, id):
      self.id = id
      self.y_location = None
      self.target_location_y = None
      self.tiles = []
      self.plants = []
      self.zombies = []
      self.projectiles = []

    def populate_tiles(self, tiles):
      self.tiles = tiles
      self.y_location = tiles[0].y_location
      self.target_location_y = tiles[0].target_location_y

    def add_plant(self, plant):
      self.plants.append(plant)

    def add_zombie(self, zombie):
      self.zombies.append(zombie)

    def add_projectile(self, projectile):
      self.projectiles.append(projectile)

    def get_zombies(self):
      return self.zombies

    def check_collisions(self):
      for zombie in self.zombies:
        for plant in self.plants:
          if plant.check_collision(zombie) and not zombie.target_plant:
            zombie.start_eating(plant)
        for projectile in self.projectiles:
          projectile.check_collision(zombie)

    def update(self):
      self.plants = [plant for plant in self.plants if not plant.is_dead]
      self.zombies = [zombie for zombie in self.zombies if not zombie.should_delete]
      self.projectiles = [projectile for projectile in self.projectiles if projectile.active]
      self.check_collisions()

      for plant in self.plants:
        plant.update()
      for zombie in self.zombies:
        zombie.update()
      for projectile in self.projectiles:
        projectile.update()

    def render(self, render):
      for tile in self.tiles:
        render = tile.render(render)
      for zombie in self.zombies:
        render = zombie.render(render)
      for plant in self.plants:
        render = plant.render(render)
      for projectile in self.projectiles:
        render = projectile.render(render)
      return render

  class Lanes:
    def __init__(self, num_lanes):
        self.lanes = [Lane(i) for i in range(num_lanes)]

    def add_plant_xy(self, x, y, plant):
        tile = self.pos_to_tile(x, y)
        lane_index = tile.lane_id
        plant = Plant(tile, self.lane_id_to_lane(tile.lane_id), plant)
        self.lanes[lane_index].add_plant(plant)

    def add_plant_tile(self, tile, plant):
        plant = Plant(tile, self.lane_id_to_lane(tile.lane_id), plant)
        self.lanes[tile.lane_id].add_plant(plant)

    def remove_plant(self, lane_index, plant):
        self.lanes[lane_index].remove_plant(plant)

    def add_zombie(self, lane_index, zombie):
        self.lanes[lane_index].add_zombie(zombie)

    def remove_zombie(self, lane_index, zombie):
        self.lanes[lane_index].remove_zombie(zombie)

    def get_all_zombies(self):
      zombies = []
      for lane in self.lanes:
          zombies += lane.get_zombies()
      return zombies

    def get_all_plants(self):
      plants = []
      for lane in self.lanes:
          plants += lane.plants
      return plants

    def assign_tiles(self, lane_index, tiles):
        self.lanes[lane_index].populate_tiles(tiles)

    def randomly_add_zombie(self, zombie_type):
        lane_index = renpy.random.randint(0, len(self.lanes) - 1)
        lane = self.lanes[lane_index]
        zombie = Zombie(lane.tiles[-1].x_location + renpy.random.randint(-1* lane.tiles[-1].width, lane.tiles[-1].width), lane.y_location, zombie_type, lane)
        lane.add_zombie(zombie)


    def update(self):
      for lane in self.lanes:
        lane.update()

    def render(self, render):
      for lane in self.lanes:
        render = lane.render(render)
      return render

    def pos_to_tile(self, x, y):
      for lane in self.lanes:
        for tile in lane.tiles:
          if tile.x_location <= x <= tile.x_location + tile.width and tile.y_location <= y <= tile.y_location + tile.height:
              return tile
      return None

    def lane_id_to_lane(self, lane_id):
      return self.lanes[lane_id]


  class PvzGameDisplayable(renpy.Displayable):
    def __init__(self, level):
      self.level_config = None
      file_handle = renpy.file(JSON_DIR + "level" + str(level) + ".json")
      file_contents = file_handle.read()
      file_handle.close()
      self.level_config = json.loads(file_contents)

      self.mouseX = 0
      self.mouseY = 0
      self.plant_selected = "peashooter"

      self.last_time = time.time()

      super(PvzGameDisplayable, self).__init__()
      all_images.load_plants(["peashooter"])
      all_images.load_zombies(["basic", "dog"])
      all_images.load_projectiles(["baseball"])

      self.environment = EnvironmentBuilder(self.level_config, self)
      self.lanes = self.environment.gen_lanes()
      for _ in range(50):
        self.lanes.randomly_add_zombie("basic")

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
      for plant in self.lanes.get_all_plants():
        plant.attack()

      if self.plant_selected is not None:
        tile = self.lanes.pos_to_tile(self.mouseX, self.mouseY)
        if tile is not None and tile.plantable():
          tile.is_planted = True
          self.lanes.add_plant_tile(tile, self.plant_selected)
        

    def render(self, width, height, st, at):
      global delta_time
      current_time = time.time()
      delta_time = (current_time - self.last_time)
      self.last_time = current_time

      current_state = self.make_state()
      self.environment.update(current_state)
      self.lanes.update()

      r = renpy.Render(width, height)
      # r = self.environment.render(r)
      r = self.lanes.render(r)
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