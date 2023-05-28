
define THIS_PATH = 'minigame/'

# XXX: using os.path.join here will actually break because Ren'Py somehow doesn't recognize it
define IMG_DIR = THIS_PATH + 'images/'
define AUDIO_DIR = THIS_PATH + 'audio/'
define JSON_DIR = THIS_PATH + 'info/'
define GRAVITY_CONSTANT = 0.3

init python:
  import pygame
  import json
  import os
  import itertools
  import math
  import time
  import random
  import copy

  def difficulty_multiplier_to_str(difficulty_multiplier):
    if difficulty_multiplier < 0.55:
      return "Pussy"
    elif difficulty_multiplier < 0.76:
      return "Easy"
    elif difficulty_multiplier < 1.1:
      return "Normal"
    elif difficulty_multiplier < 1.4:
      return "Hard"
    else:
      return "Extreme"


  def plant_name_to_plant(tile, lane, plant_type, gui_controller):
    if plant_type == "peashooter":
      return PeaShooter("peashooter", tile, lane)
    elif plant_type == "repeater":
      return PeaShooter("repeater", tile, lane)
    elif plant_type == "fumeshroom":
      return PeaShooter("fumeshroom", tile, lane)
    elif plant_type == "pranav":
      return Pranav(tile, lane)
    elif plant_type == "colin":
      return PeaShooter("colin", tile, lane)
    elif plant_type == "logan":
      return Logan(tile, lane)
    elif plant_type == "iceshooter":
      return IceShooter(tile, lane)
    elif plant_type == "wallnut":
      return Wallnut(tile, lane)
    elif plant_type == "sunflower":
      return Sunflower(tile, lane, gui_controller)
    elif plant_type == "cobcannon":
      return CobCannon(tile, lane, gui_controller)
    elif plant_type == "andrew":
      return Andrew(tile, lane)
    elif plant_type == "jacob":
      return Jacob(tile, lane)


  def load_json_from_file(path):
    file_handle = renpy.file(path)
    file_contents = file_handle.read()
    file_handle.close()
    return json.loads(file_contents)

  level_config = load_json_from_file(path=JSON_DIR + "levels.json")
  zombie_config = load_json_from_file(path=JSON_DIR + "zombies.json")
  plant_config = load_json_from_file(path=JSON_DIR + "plants.json")
  projectile_config = load_json_from_file(path=JSON_DIR + "projectiles.json")
  explosion_config = load_json_from_file(path=JSON_DIR + "explosions.json")

  delta_time = 0.0
  delta_multiplier = 70

  has_been_resized = False

  def send_to_file(filename, text):
    with open(config.gamedir + "/" + filename, "a") as f:
        f.write(text)

  def lighten(color):
        return(color[0], color[1] + 8, color[2] + 4)

  def level_to_area(level_name):
    return level_config[level_name]["area"]

  class ConfigLoader():
    def __init__(self, level_config, zombie_config, plant_config, projectile_config, explosion_config):
      self.levels = level_config
      self.plants = plant_config
      self.zombies = zombie_config
      self.projectiles = projectile_config
      self.explosions = explosion_config

    def get_tile_width(self, level_name):
      level_config = self.get_level_config(level_name)
      env_width = config.screen_width * level_config["width_multiplier"]
      return round(env_width / level_config["num_cols"])

    def get_explosion_config(self, explosion_type):
      return self.explosions[explosion_type]

    def get_level_config(self, level_name):
      area_dict = self.levels["areas"][self.levels[level_name]["area"]]
      toRet = self.levels[level_name].copy()
      toRet.update(area_dict)
      return toRet

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

    def modify_explosion_image_size(self, explosion_type, resize_factor):
      if has_been_resized:
        return
      image_config = self.get_explosion_config(explosion_type)
      image_config["height"] = image_config["height"] * resize_factor
      image_config["width"] = image_config["width"] * resize_factor
      image_config["joint_x"] = image_config["joint_x"] * resize_factor
      image_config["joint_y"] = image_config["joint_y"] * resize_factor
      self.explosions[explosion_type] = image_config
      
    def modify_plant_image_size(self, animation_type, resize_factor):
      if has_been_resized:
        return
      image_config = self.get_plant_image_config(animation_type)
      plant_config = self.get_plant_config(animation_type)
      image_config["height"] = image_config["height"] * resize_factor
      image_config["width"] = image_config["width"] * resize_factor
      image_config["joint_x"] = image_config["joint_x"] * resize_factor
      image_config["joint_y"] = image_config["joint_y"] * resize_factor
      if plant_config["spawn_projectile"]:
        image_config["projectile_spawn_x"] = image_config["projectile_spawn_x"] * resize_factor
        image_config["projectile_spawn_y"] = image_config["projectile_spawn_y"] * resize_factor
      if plant_config["animation_type"] == "sunflower":
        image_config["sun_spawn_x"] = image_config["sun_spawn_x"] * resize_factor
        image_config["sun_spawn_y"] = image_config["sun_spawn_y"] * resize_factor
      self.plants["image_data"][animation_type] = image_config

    def modify_projectile_image_size(self, projectile_name, resize_factor):
      if has_been_resized:
        return
      image_config = self.get_projectile_config(projectile_name)
      image_config["height"] = image_config["height"] * resize_factor
      image_config["width"] = image_config["width"] * resize_factor
      image_config["center_x"] = image_config["center_x"] * resize_factor
      image_config["center_y"] = image_config["center_y"] * resize_factor
      self.projectiles[projectile_name] = image_config
      
    def modify_zombie_image_size(self, animation_type, resize_factor):
        if has_been_resized:
          return
        image_config = self.get_zombie_image_config(animation_type)
        if image_config["class"] in ["zombie", "vehicle", "shield"]:
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

  class Particle():
    def __init__(self, x, y, color, x_size, y_size, speed, direction, life, gravity_affected):
      self.x = x
      self.y = y
      self.color = color
      self.x_size = x_size
      self.y_size = y_size
      self.speed = speed
      self.direction = direction
      self.life = life
      self.age = 0
      self.gravity_affected = gravity_affected

      self.image = Solid(self.color, xsize=self.x_size, ysize=self.y_size)

      self.x_velocity = self.speed * math.cos(self.direction)
      self.y_velocity = self.speed * math.sin(self.direction)

    def update(self):
      self.x += self.x_velocity * delta_multiplier * delta_time
      self.y += self.y_velocity * delta_multiplier * delta_time
      if self.gravity_affected:
        self.y_velocity += GRAVITY_CONSTANT
      self.age += delta_time
      if self.age >= self.life:
        return True
      return False

    def render(self, render):
      image = self.image
      render.place(image, x=self.x, y=self.y)
      return render

  class Pranav_Smoke_Particle():
    def __init__(self, x, y):
      self.x = x - config_data.get_projectile_config("pranav-smoke")["center_x"]
      self.y = y - config_data.get_projectile_config("pranav-smoke")["center_y"]
      self.speed = renpy.random.randint(2, 3)
      self.image = Image(IMG_DIR + "projectiles/" + "pranav-smoke" + ".png")
      self.life = 1
      self.age = 0

    def update(self):
      self.y -= self.speed * delta_multiplier * delta_time
      self.age += delta_time
      if self.age >= self.life:
        return True
      return False

    def render(self, render):
      image = self.image
      # send_to_file("logz.txt", str(self.x), ", ", str(self.y) + "\n")
      render.place(image, x=self.x, y=self.y)
      return render

  class Electric_Particle(Particle):
    def __init__(self, x, y, x_variance):
      color = (255, 102, 255, 150)
      y_size = renpy.random.randint(8, 15)
      speed = renpy.random.randint(3, 5)
      direction = 1.5 * math.pi
      x = x + renpy.random.randint(-x_variance, x_variance)
      super().__init__(x, y, color, 2, y_size, speed, direction, 0.5, False)
      

    def update(self):
      should_remove = super().update()
      self.x += renpy.random.randint(-2, 2)
      return should_remove

    def render(self, render):
      return super().render(render)

  class EyeEffect():
    def __init__(self, x, y, is_tranformation=False):
      self.x = x
      self.y = y
      self.color_1 = (255, 102, 255, 150)
      self.color_2 = (255, 102, 255, 100)
      self.size_limit = 5

      if is_tranformation:
        self.color_1 = (255,255,59, 150)
        self.color_2 = (250,225,97, 100)

      self.size_1 = 1
      self.size_2 = 2
      self.spawn_time = time.time()
      if not is_tranformation:
        renpy.play(AUDIO_DIR + "charge.mp3", channel = "audio")
      else:
        renpy.play(AUDIO_DIR + "neil-roar.mp3", channel = "audio")
      self.stop_growth = False

    def calculate_placement_location(self, target_x, target_y, size):
      x = target_x - (size / 2)
      y = target_y - (size / 2)
      return x, y

    def update(self):
      if not self.stop_growth:
        self.size_1 = int(10*(time.time() - self.spawn_time))
        self.size_2 = int(15*(time.time() - self.spawn_time))

    def render(self, render):
      x, y = self.calculate_placement_location(self.x, self.y, self.size_1)
      image = Solid(self.color_1, xsize=self.size_1, ysize=self.size_1)
      render.place(image, x=x, y=y)

      x, y = self.calculate_placement_location(self.x, self.y, self.size_2)
      image = Solid(self.color_2, xsize=self.size_2, ysize=self.size_2)
      render.place(image, x=x, y=y)
      # send_to_file("logz.txt", str(self.size_1) + "\n")
      
      return render

  class LaserEffect():
    def __init__(self, x, y, target_x, target_y, is_tranformation=False, life=False):
      self.x = x
      self.y = y
      self.is_tranformation = is_tranformation
      self.target_x = target_x
      self.target_y = target_y
      self.size_1 = 7
      self.size_2 = 10

      self.spawn_time = time.time()
      self.life = life

      if self.is_tranformation:
        self.size_1 = 30
        self.size_2 = 40

      self.color = (255, 102, 255, 150)
      self.color_2 = (255, 102, 255, 100)
      self.size = 1

      if not self.is_tranformation:
        renpy.play(AUDIO_DIR + "zap.mp3", channel = "audio")

      self.distance_to_target = int(math.sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2)) + 10
      self.angle_to_rotate = math.degrees(math.atan2(self.target_y - self.y, self.target_x - self.x))
    
    def update(self, x, y):
      self.x = x
      self.y = y
      self.distance_to_target = int(math.sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2)) + 10
      self.angle_to_rotate = math.degrees(math.atan2(self.target_y - self.y, self.target_x - self.x))
      if self.is_tranformation:
        self.size_1 = renpy.random.randint(5, 50)
        self.size_2 = renpy.random.randint(70, 90)
        opacity = renpy.random.randint(100, 140)
        self.color = (255,255,59, opacity+50)
        self.color_2 = (250,225,97, opacity)
      else:
        self.size_1 = renpy.random.randint(5, 7)
        self.size_2 = renpy.random.randint(10, 15)

      if self.life:
        if time.time() - self.spawn_time > self.life:
          return True
      return False

    def render(self, render):
      if self.is_tranformation:
        image_1 = Solid(self.color, xsize=self.size_1, ysize=self.distance_to_target)
        image_2 = Solid(self.color_2, xsize=self.size_2, ysize=self.distance_to_target)
        offset = renpy.random.randint(-10, 10)
        render.place(image_2, x=self.x - int(self.size_2/2) + offset, y=self.y)
        render.place(image_1, x=self.x - int(self.size_1/2) - offset, y=self.y)
      else:
        image_1 = Transform(Solid(self.color, xsize=self.distance_to_target, ysize=self.size_1), rotate=self.angle_to_rotate, anchor = (0, 0), transform_anchor = True)
        image_2 = Transform(Solid(self.color_2, xsize=self.distance_to_target, ysize=self.size_2), rotate=self.angle_to_rotate, anchor = (0, 0), transform_anchor = True)
        render.place(image_1, x=self.x, y=self.y + int(self.size_1))
        render.place(image_2, x=self.x, y=self.y + int(self.size_2))
      return render


  class ParticleSystem():
    def __init__(self):
      self.particles = []

    def summon(self, x, y):
      for i in range(7):
        color = (255, 232, 3, 170)
        x_variance = 30
        y_size = renpy.random.randint(30, 40)
        speed = renpy.random.randint(2, 4)
        direction = 1.5 * math.pi
        x = x + renpy.random.randint(-x_variance, x_variance)
        self.particles.append(Particle(x, y, color, 6, y_size, speed, direction, 1, False))

    def clear(self):
      self.particles = []

    def explosion(self, x, y):
      for i in range(20):
        v = renpy.random.randint(20, 255)
        color = (255, v, v, 255)
        x_variance = 15
        size = renpy.random.randint(4, 6)
        speed = renpy.random.randint(25, 30)
        direction = (1.5 + (renpy.random.randint(-25, 25)/100))* math.pi
        x = x + renpy.random.randint(-x_variance, x_variance)
        self.particles.append(Particle(x, y, color, size, size, speed, direction, 0.3, True))

    def electricity(self, x, y, x_variance):
      for i in range(3):
        # color = (255, 102, 255, 150)
        # y_size = renpy.random.randint(8, 15)
        # speed = renpy.random.randint(1, 3)
        # direction = 1.5 * math.pi
        # x = x + renpy.random.randint(-x_variance, x_variance)
        self.particles.append(Electric_Particle(x, y, x_variance))

    def transformation(self, target_x, target_y):
      for i in range(1):
        self.particles.append(LaserEffect(target_x, 100, target_x, target_y, is_tranformation=True, life=2))

    def trail(self, x, y, color, size, life):
      for i in range(1):
        size += renpy.random.randint(0, 2)
        speed = 1
        direction = renpy.random.uniform(0.7 * math.pi, 1.3 * math.pi)
        self.particles.append(Particle(x + 10, y, color, size, size, speed, direction, life, False))

    def splash(self, x, y, color, life):
      for i in range(5):
        size = renpy.random.randint(3, 5)
        speed = renpy.random.randint(1, 4)
        direction = renpy.random.uniform(0, 2 * math.pi)
        self.particles.append(Particle(x, y, color, size, size, speed, direction, life, True))

    def pranav_smoke_blow(self, x, y):
      for i in range(5):
        x_variance = config_data.get_tile_width("level1")//4
        self.particles.append(Pranav_Smoke_Particle(x + renpy.random.randint(-x_variance, x_variance), y))

    def update(self):
      for particle in self.particles:
        result = None
        if isinstance(particle, LaserEffect):
          result = particle.update(particle.x, particle.y)
        else:
          result = particle.update()
        if result:
          self.particles.remove(particle)

    def render(self, render):
      for particle in self.particles:
        render = particle.render(render)
      return render

        
  class ImageLoader():
    def __init__(self):
      self.images = {}
      self.brightness_factor = 0.3

    def load_gui(self):
      self.images["gui"] = {}
      to_load = ["sun", "target", "hellfire", "shovel", "evil", "bed"]
      for image_name in to_load:
        location = IMG_DIR + "gui/" + image_name + ".png"
        image = Image(location)
        self.images["gui"][image_name] = image

      self.images["gui"]["bed"] = im.FactorScale(self.images["gui"]["bed"], 0.5)

    def load_explosions(self):
      self.images["explosions"] = {}
      explosion_names = ["hellfire"]

      for explosion_name in explosion_names:
        explosion_config = config_data.get_explosion_config(explosion_name)
        explosion_location = IMG_DIR + "explosions/" + explosion_name
        num_frames = explosion_config["num_frames"]
        image_prefix = explosion_config["image_prefix"]
        resize_factor = explosion_config["resize_factor"]
        animation_frames = [im.FactorScale(Image(explosion_location + "/" + image_prefix + str(i) + ".png"), resize_factor) for i in range(num_frames)]
        config_data.modify_explosion_image_size(explosion_name, resize_factor=resize_factor)
        self.images["explosions"][explosion_name] = animation_frames

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
          "animation": {
            "default": animation_frames,
            "damaged_default": [im.MatrixColor(frame, im.matrix.brightness(self.brightness_factor)) for frame in animation_frames]
          }
        }

        if config_data.get_plant_image_config(animation_type)["has_attack_frame"]:
          attack_frame = im.FactorScale(Image(plant_location + "/" + image_prefix + "-attack" + ".png"), resize_factor)
          self.images["plants"][plant_name]["animation"]["attack"] = attack_frame
          self.images["plants"][plant_name]["animation"]["damaged_attack"] = im.MatrixColor(attack_frame, im.matrix.brightness(self.brightness_factor))

        if config_data.get_plant_image_config(plant_name)["has_damage_frames"]:
          keys = config_data.get_plant_image_config(plant_name)["damage_frame_order"].keys()
          for key in keys:
            frame = im.FactorScale(Image(plant_location + "/" + image_prefix + "-" + key + ".png"), resize_factor)
            self.images["plants"][plant_name]["animation"][key] = frame
            self.images["plants"][plant_name]["animation"]["damaged_" + key] = im.MatrixColor(frame, im.matrix.brightness(self.brightness_factor))

        if "other_frames" in config_data.get_plant_image_config(animation_type):
          other_frames = config_data.get_plant_image_config(animation_type)["other_frames"]
          for frame_name in other_frames:
            frame = im.FactorScale(Image(plant_location + "/" + image_prefix + "-" + frame_name + ".png"), resize_factor)
            self.images["plants"][plant_name]["animation"][frame_name] = frame
            self.images["plants"][plant_name]["animation"]["damaged_" + frame_name] = im.MatrixColor(frame, im.matrix.brightness(self.brightness_factor))

      projectiles_to_load = self.determine_projectiles_to_load(plant_names=plant_types)
      self.load_projectiles(projectiles_to_load)


    def load_zombies(self, zombie_types):
      self.images["zombies"] = {}
      for zombie_name in zombie_types:
        self.images["zombies"][zombie_name] = {}
        self.images["zombies"][zombie_name]["icon"] = im.FactorScale(Image(IMG_DIR + "zombies/" + zombie_name + f"/{zombie_name}.png"), 0.35)
        zombie_location = IMG_DIR + "zombies/" + zombie_name
        animation_type = config_data.get_zombie_config(zombie_name)["animation_type"]
        resize_factor = config_data.get_zombie_image_config(animation_type)["resize_factor"]

        config_data.modify_zombie_image_size(animation_type, resize_factor=resize_factor)

        part_types = config_data.get_zombie_image_config(animation_type)["parts"]
        part_types_with_damage_frames = None
        has_damage_frames = config_data.get_zombie_config(zombie_name)["has_damage_frames"]
        blacken_on_explosion = config_data.get_zombie_config(zombie_name)["blacken_on_explosion"]
        if blacken_on_explosion:
          self.images["zombies"][zombie_name]["blackened"] = {
             part_type:im.MatrixColor(im.FactorScale(Image(zombie_location + f"/{part_type}.png"), resize_factor), im.matrix.brightness(-1)) for part_type in part_types
          }
        if has_damage_frames:
          part_types_with_damage_frames = config_data.get_zombie_config(zombie_name)["damage_frame_order"].keys()

        types_to_loop = ["default", "iced"]
        if zombie_name == "shield" or zombie_name == "armored_shield":
          types_to_loop = ["default"]
        for type_to_loop in types_to_loop:
          suffix = ""
          if type_to_loop == "iced":
            suffix = "-" + type_to_loop
          self.images["zombies"][zombie_name][type_to_loop] = {part_type:im.FactorScale(Image(zombie_location + f"/{part_type}{suffix}.png"), resize_factor) for part_type in part_types}
          self.images["zombies"][zombie_name]["damaged_"+type_to_loop] = {
            part_type:im.MatrixColor(im.FactorScale(Image(zombie_location + f"/{part_type}{suffix}.png"), resize_factor), im.matrix.brightness(self.brightness_factor)) for part_type in part_types
          }
          if has_damage_frames:
            for part in part_types_with_damage_frames:
              for damage_frame in config_data.get_zombie_config(zombie_name)["damage_frame_order"][part].keys():
                self.images["zombies"][zombie_name][damage_frame + suffix] = {
                  part_type:im.FactorScale(Image(zombie_location + f"/{part_type}-{damage_frame}{suffix}.png"), resize_factor) for part_type in part_types
                }
                self.images["zombies"][zombie_name]["damaged_"+ damage_frame + suffix] = {
                  part_type:im.MatrixColor(im.FactorScale(Image(zombie_location + f"/{part_type}-{damage_frame}{suffix}.png"), resize_factor), im.matrix.brightness(self.brightness_factor)) for part_type in part_types
                }


    def load_projectiles(self, projectile_types):
      self.images["projectiles"] = {}
      for projectile_name in projectile_types:
        projectile_location = IMG_DIR + "projectiles/" + projectile_name + ".png"
        resize_factor = config_data.get_projectile_config(projectile_name)["resize_factor"]
        config_data.modify_projectile_image_size(projectile_name, resize_factor=resize_factor)

        if projectile_name != "andrew":
          self.images["projectiles"][projectile_name] = {
            "image": im.FactorScale(Image(projectile_location), resize_factor)
          }
        else:
          self.images["projectiles"][projectile_name] = {}
          for i in range(6):
            self.images["projectiles"][projectile_name][i] = im.FactorScale(Image(IMG_DIR + "projectiles/" + projectile_name + "-" + str(i) + ".png"), resize_factor)

    def determine_projectiles_to_load(self, plant_names):
      projectiles = []
      for plant_name in plant_names:
        if config_data.get_plant_config(plant_name)["spawn_projectile"]:
          projectile_name = config_data.get_plant_config(plant_name)["projectile_type"]
          if projectile_name not in projectiles:
            projectiles.append(projectile_name)
      return projectiles
      

    def return_overlays(self):
      plants = self.images["plants"].keys()
      overlays = {plant:self.images["plants"][plant]["overlay"] for plant in plants}
      return overlays

  # These are the global variables
  all_images = ImageLoader()
  config_data = ConfigLoader(level_config, zombie_config, plant_config, projectile_config, explosion_config)
  particleSystem = ParticleSystem()

  class Tile():
    def __init__(self, x_location, y_location, row_id, lane_id, width, height, color):
      self.x_location = x_location
      self.y_location = y_location
      self.lane_id = lane_id
      self.lane = None
      self.row_id = row_id
      self.is_protected = False

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

      if self.is_protected:
        render.place(all_images.images["gui"]["bed"] , x = self.x_location, y = self.y_location)

      if drawables["overlay"] is not None:
        plant_image_config = config_data.get_plant_image_config(self.plant_selected)
        x_location = self.target_location_x - plant_image_config["joint_x"]
        y_location = self.target_location_y - plant_image_config["joint_y"]
        render.place(drawables["overlay"], x = x_location, y = y_location)

      return render

    def get_plant_on_tile(self):
      for plant in self.lane.plants:
        if plant.tile == self:
          return plant

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

      self.image = None
      if not self.projectile_type == "andrew":
        self.image = all_images.images["projectiles"][self.projectile_type]["image"]
      self.effects = self.projectile_config["effects"]
      self.does_spawn_particle = self.projectile_config["spawn_particles"]

      self.trail_time = time.time()
      self.leave_trail = False
      self.particle_color = None
      self.particle_size = None
      if self.does_spawn_particle:
        self.particle_color = (self.projectile_config["particle_color"][0], self.projectile_config["particle_color"][1], self.projectile_config["particle_color"][2])
        self.particle_size = self.projectile_config["particle_size"]
        self.leave_trail = self.projectile_config["leave_trail"]

      self.plant_spawn_x = self.plant.x_location + self.plant.plant_image_config["projectile_spawn_x"]
      self.plant_spawn_y = self.plant.y_location + self.plant.plant_image_config["projectile_spawn_y"]

      self.x_location = self.plant_spawn_x - self.center_x
      self.y_location = self.plant_spawn_y - self.center_y

      self.range = (config_data.get_tile_width("level1") * self.projectile_config["range"])

      self.angle = 0
      self.angle_rotation_direction = 1
      if renpy.random.randint(1, 2) == 1:
        self.angle_rotation_direction = -1
      self.angle_rotation_speed = renpy.random.randint(5, 9)

      self.active = True
      self.damaged_zombies = []

    def process_rotation(self):
      transformed_image = Transform(self.image, rotate=self.angle, anchor = (0, 0), transform_anchor = True)
      # Calculate the offset of the joint after rotation
      dx = self.center_x
      dy = self.center_y
      current_angle = math.atan2(dy, dx)
      new_angle = current_angle + math.radians(self.angle)

      new_dx = dx * math.cos(math.radians(self.angle)) - dy * math.sin(math.radians(self.angle))
      new_dy = dx * math.sin(math.radians(self.angle)) + dy * math.cos(math.radians(self.angle))

      # Calculate the position of the transformed image
      x_location = self.x_location - new_dx + self.center_x
      y_location = self.y_location - new_dy + self.center_y
      return transformed_image, x_location, y_location

    def render(self, render):

      x = self.x_location 
      y = self.y_location
      image = self.image
      if self.projectile_type == "beer" or self.projectile_type == "ice":
        image, x, y = self.process_rotation()

      render.place(image, x=x, y=y)
      return render

    def update(self):

      if self.projectile_type == "beer" or self.projectile_type == "ice":
        self.angle += self.angle_rotation_speed * self.angle_rotation_direction * delta_multiplier * delta_time

      if self.active:
        self.x_location += self.speed * delta_multiplier * delta_time
        self.range -= self.speed * delta_multiplier * delta_time
      
      if self.x_location > config.screen_width or self.range <= 0:
        self.active = False

      if self.leave_trail and time.time() - self.trail_time > 0.2:
        self.trail_time = time.time()
        self.trail_effect()

    def check_reference_in_list(self, ref_obj, obj_list):
        for obj in obj_list:
            if ref_obj is obj:
                return True
        return False

    def trail_effect(self):
      if self.does_spawn_particle:
        spawn_x = self.x_location + self.center_x
        spawn_y = self.y_location + self.center_y
        particleSystem.trail(spawn_x, spawn_y, self.particle_color, self.particle_size, 0.2)

    def splash_effect(self):
      if self.does_spawn_particle:
        spawn_x = self.x_location + self.center_x
        spawn_y = self.y_location + self.center_y
        particleSystem.splash(spawn_x, spawn_y, self.particle_color, 0.2)

    def check_collision(self, zombie):
      if self.active:
        if self.lane is zombie.lane:
          if abs(self.x_location - zombie.x_location) < (zombie.hitbox_distance/5) and zombie.is_dead is False:
            if self.check_reference_in_list(zombie, self.damaged_zombies) is False:
              if self.effects == "ice":
                zombie.get_iced()
              if self.projectile_type in ["smoke", "pranav-smoke"] and zombie.zombie_type == "mask_shield_bearer":
                return
              zombie.damage(self.damage)
              self.damaged_zombies.append(zombie)
              if zombie.zombie_type == "armored_shield" and self.projectile_type == "icicle":
                self.pierce = 0
              if len(self.damaged_zombies) >= self.pierce:
                self.active = False
                self.splash_effect()
                # if renpy.music.get_playing(channel = "sound") is None:
                #   renpy.play(AUDIO_DIR + "splat.mp3", channel = "sound")

  class Andrew_Projectile(Projectile):
    def __init__(self, plant):
      super().__init__(plant, "andrew")
      self.frame = 0
      self.frame_timer = time.time()
      self.frame_delay = 0.2

    def render(self, render):
      image = all_images.images["projectiles"][self.projectile_type][self.frame]
      render.place(image, x=self.x_location, y=self.y_location)
      return render

    def update(self):
      super().update()
      if time.time() - self.frame_timer > self.frame_delay:
        self.frame_timer = time.time()
        self.frame = (self.frame + 1) % 6


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
      self.cost = self.plant_config["cost"]

      self.does_spawn_projectile = self.plant_config["spawn_projectile"]
      self.projectile_type = None
      if self.does_spawn_projectile:
        self.projectile_type = self.plant_config["projectile_type"]

      self.costume = "default"
      self.attack_costume_timer = time.time()

      self.frames = all_images.images["plants"][self.plant_type]["animation"][self.costume]
      self.damaged_timer = None

      self.plant_image_config = config_data.get_plant_image_config(self.plant_type)
      self.frame = 0

      self.x_location = self.tile.target_location_x - self.plant_image_config["joint_x"]
      self.y_location = self.tile.target_location_y - self.plant_image_config["joint_y"]

      self.is_being_stolen = False
      self.is_protected = False
      self.game = None

      renpy.play(AUDIO_DIR + "plant-planted.mp3", channel = "audio")

    def set_new_tile(self, tile):
      self.tile = tile
      self.x_location = self.tile.target_location_x - self.plant_image_config["joint_x"]
      self.y_location = self.tile.target_location_y - self.plant_image_config["joint_y"]

    def render(self, render):
      if self.costume in ["default", "damaged_default"]:
        self.frames = all_images.images["plants"][self.plant_type]["animation"][self.costume]
        render.place(self.frames[self.frame], x = self.x_location, y = self.y_location)
      else:
        # send_to_file("logz.txt", ",".join(list(all_images.images["plants"][self.plant_type]["animation"].keys())) + "\n")
        image = all_images.images["plants"][self.plant_type]["animation"][self.costume]
        render.place(image, x = self.x_location, y = self.y_location)
      return render

    def die(self):
      self.tile.is_planted = False
      self.is_dead = True
      if not self.plant_type == "jacob":
        renpy.play(AUDIO_DIR + "oof.mp3", channel = "audio")
      if self.is_protected:
        self.game.has_protected_plant_died = True

    def damage(self, damage):
      self.health -= damage
      if self.health <= 0:
        self.die()
      
      if not self.costume.startswith("damaged_"):
        self.costume = "damaged_" + self.costume
        self.damaged_timer = time.time()


    def attack(self):
      self.costume = "attack"
      self.attack_costume_timer = time.time()
      if self.does_spawn_projectile:
        self.lane.add_projectile(Projectile(self, self.projectile_type))
      else:
        return None

    def check_collision(self, zombie):
      if zombie.lane is self.lane:
        if abs(zombie.x_location - zombie.hitbox_distance - (self.x_location- self.hitbox_distance*0.5)) - self.hitbox_distance*0.5 <= (self.hitbox_distance + renpy.random.randint(0,4)) and zombie.is_dead is False:
          return True
      else: 
        return False

    def set_damage_frame_costume(self):
      damage_frame_order = self.plant_image_config["damage_frame_order"]
      for key,value in damage_frame_order.items():
        if self.health <= self.plant_config["health"] * (1-value):
          self.costume = key

    def update(self):

      if self.plant_image_config["has_damage_frames"]:
        self.set_damage_frame_costume()

      if self.costume == "attack":
        if time.time() - self.attack_costume_timer > 0.3:
          self.costume = "default"

      if self.health <= 0:
        self.die()

      if self.damaged_timer is not None:
        if time.time() - self.damaged_timer > 0.05:
          self.costume = self.costume.replace("damaged_", "")
          self.damaged_timer = None

      self.frame = (self.frame + 1) % len(self.frames)

  class Jacob(Plant):
    def __init__(self, tile, lane):
      super().__init__(tile, lane, "jacob")
      self.target_tile = None
      self.attacking = False

      self.is_jumping = False
      self.jump_velocity = -15

      self.is_falling = False
      self.x_distance = None
      self.y_distance = None

      self.y_velocity = None
      self.speed = 2


    def get_zombie_costs_on_tile(self, tile):
      zombie_costs = []
      for zombie in self.lane.return_all_zombies_on_tile(tile):
        zombie_costs.append(zombie.zombie_config["cost"])
      return sum(zombie_costs)

    def damage_zombies(self):
      for zombie in self.lane.return_all_zombies_on_tile(self.target_tile):
        zombie.damage(self.plant_config["damage"])

    def damage(self, damage):
      pass

    def update(self):
      if not self.attacking:
        self.check_zombies_within_range()

      if self.attacking:
        self.y_location += self.y_velocity * delta_multiplier * delta_time
        if self.is_jumping:
          self.y_velocity += 0.5 * delta_multiplier * delta_time
          if self.y_velocity >= 0:
            self.is_jumping = False
            self.y_velocity = 0
            self.is_falling = True
            self.x_distance = self.target_tile.target_location_x - self.x_location - self.plant_image_config["joint_x"]
            self.y_distance = self.target_tile.target_location_y - self.y_location - self.plant_image_config["joint_y"]
        
        if self.is_falling:
          distance = ((self.x_distance ** 2) + (self.y_distance ** 2)) ** 0.5
          if distance > 0:
            angle = math.atan2(self.y_distance, self.x_distance)
            move_speed_x = math.cos(angle) * self.speed
            move_speed_y = math.sin(angle) * self.speed
            self.x_location += move_speed_x
            self.y_location += move_speed_y
            self.speed = 1.1 * self.speed

            if self.y_location + self.plant_image_config["joint_y"]> self.target_tile.target_location_y:
              self.damage_zombies()
              self.is_dead = True
              if self.is_protected:
                self.game.has_protected_plant_died = True
              self.attacking = False
              self.tile.is_planted = False
              self.x_location = self.target_tile.target_location_x - self.plant_image_config["joint_x"]
              self.y_location = self.target_tile.target_location_y - self.plant_image_config["joint_y"]
              renpy.play(AUDIO_DIR + "thud.mp3", channel = "audio")

        
    def check_zombies_within_range(self):
      current_tile_id = self.tile.row_id
      tile_in_front = self.lane.get_tile_by_row_id(current_tile_id + 1)
      tile_behind = self.lane.get_tile_by_row_id(current_tile_id - 1)
      all_tiles = [self.tile, tile_in_front, tile_behind]
      valid_tiles = [tile for tile in all_tiles if tile is not None]

      best_tile = None
      best_tile_cost = 0
      for tile in valid_tiles:
        zombie_costs = self.get_zombie_costs_on_tile(tile)
        if zombie_costs > best_tile_cost:
          best_tile_cost = zombie_costs
          best_tile = tile

      if best_tile is not None:
        self.target_tile = best_tile
        self.attacking = True
        self.is_jumping = True
        self.y_velocity = self.jump_velocity
        self.costume = "attack"
        renpy.play(AUDIO_DIR + "roar.mp3", channel = "audio")



    

  class Andrew(Plant):
    def __init__(self, tile, lane):
      super().__init__(tile, lane, "andrew")
      tile.is_planted = False
      self.launch_attack()

    def launch_attack(self):
      self.lane.add_projectile(Andrew_Projectile(plant=self))
      self.is_dead = True
      self.tile.is_planted = False
      renpy.play(AUDIO_DIR + "griddy.mp3", channel = "audio")


  class CobCannon(Plant):
    def __init__(self, tile, lane, gui_controller):
      super().__init__(tile, lane, "cobcannon")
      self.gui_controller = gui_controller
      self.explosion_controller = self.gui_controller.explosion_controller
      self.attack_timer = None
      self.attack_delay = self.plant_config["attack_delay"]
      self.is_ready_to_fire = True
      self.in_firing_sequence = False

      self.targeting_delay = self.plant_config["targeting_delay"]
      self.targeting_timer = None

      self.target_coord_x = None
      self.target_coord_y = None

      self.target_marker = None

    def attack(self):
      pass

    def missile_exploded(self):
      pass

    def die(self):
      super().die()
      if self.in_firing_sequence:
        self.gui_controller.is_targeting = False
        self.gui_controller.targeted_location_x = None
        self.gui_controller.targeted_location_y = None
        if self.target_marker is not None:
          self.target_marker.impacted()
        

    def render(self, render):
      if not self.is_ready_to_fire:
        cooldown_height = int(self.plant_image_config["height"] * (time.time() - self.attack_timer) / self.attack_delay)
        background_solid = Solid((0, 0, 0, 100), xsize=int(self.plant_image_config["width"]), ysize=cooldown_height)
        render.place(background_solid, x = self.x_location, y = self.y_location + self.plant_image_config["height"] - cooldown_height)
      return super().render(render)

    def update(self):
      super().update()
      if not self.is_ready_to_fire:
        self.costume = "cooldown"
        if time.time() - self.attack_timer > self.attack_delay:
          self.costume = "default"
          self.is_ready_to_fire = True
          renpy.play(AUDIO_DIR + "ready-to-fire.mp3", channel = "audio")

      if self.in_firing_sequence:
        if self.is_ready_to_fire:
          self.costume = "ready"
        if self.gui_controller.targeted_location_x:
          if not self.targeting_timer:
            if not self.gui_controller.lanes.pos_to_tile(self.gui_controller.targeted_location_x, self.gui_controller.targeted_location_y):
              self.in_firing_sequence = False
              self.is_ready_to_fire = True
              self.gui_controller.targeted_location_x = None
              self.gui_controller.targeted_location_y = None
              self.costume = "default"
              self.gui_controller.display_notification("Must target a tile!")
              return

            self.targeting_timer = time.time()
            self.gui_controller.is_targeting = False
            renpy.play(AUDIO_DIR + "call-airstrike.mp3", channel = "audio")
            self.is_ready_to_fire = False
            self.attack_timer = time.time()
            self.target_marker = self.gui_controller.add_target_marker(self.gui_controller.targeted_location_x, self.gui_controller.targeted_location_y, self)
            self.target_coord_x = self.gui_controller.targeted_location_x
            self.target_coord_y = self.gui_controller.targeted_location_y
            self.gui_controller.targeted_location_x = None
            self.gui_controller.targeted_location_y = None
            
        if self.targeting_timer and time.time() - self.targeting_timer > self.targeting_delay:
          self.targeting_timer = None
          self.in_firing_sequence = False
          self.drop_hellfire()
          self.target_marker = None
            
    def drop_hellfire(self):
      self.explosion_controller.add_missile(self.target_coord_x, self.target_coord_y, self, self.target_marker)

    def prepare_missile(self):
      if not self.in_firing_sequence and not self.gui_controller.is_targeting:
        self.in_firing_sequence = True
        renpy.play(AUDIO_DIR + "load-missile.mp3", channel = "audio")
        self.gui_controller.is_targeting = True
      else:
        self.in_firing_sequence = False


  class IceShooter(Plant):
    def __init__(self, tile, lane):
      super().__init__(tile, lane, "iceshooter")
      self.attack_timer = time.time()
      self.attack_delay = self.plant_config["attack_delay"]

    def does_lane_have_hittable_zombies(self):
      for zombie in self.lane.zombies:
        if zombie.x_location > (self.x_location + self.hitbox_distance):
          return True
      return False

    def update(self):
      super().update()
      if self.does_lane_have_hittable_zombies():
        if time.time() - self.attack_timer > self.attack_delay:
          self.attack()
          self.attack_timer = time.time()
    
  # covers peashooter and repeater, as well as fumeshroom
  class PeaShooter(Plant):
    def __init__(self, plant_name, tile, lane):
      super().__init__(tile, lane, plant_name)
      self.attack_timer = time.time()
      self.shot_timer = time.time()
      self.attack_delay = self.plant_config["attack_delay"]
      self.shot_delay = self.plant_config["shot_delay"]
      self.num_shot_already = 0
      self.shot_range = (config_data.get_tile_width("level1") * config_data.get_projectile_config(self.projectile_type)["range"])

      if plant_name == "fumeshroom" or plant_name == "pranav":
        renpy.play(AUDIO_DIR + "smoker-planted.mp3", channel = "audio")

    def does_lane_have_hittable_zombies(self):
      
      for zombie in self.lane.zombies:
        if zombie.x_location > (self.x_location + self.hitbox_distance) and zombie.x_location < self.x_location + self.plant_image_config["projectile_spawn_x"] + self.shot_range:
          return True
      return False

    def update(self):
      super().update()

      if self.plant_type == "logan":
        if not self.does_lane_have_hittable_zombies():
          self.costume = "default"
        if (time.time() - self.attack_timer <= self.attack_delay) and (time.time() - self.shot_timer > self.shot_delay):
          self.costume = "chugging"

      if self.does_lane_have_hittable_zombies():
        if (time.time() - self.attack_timer > self.attack_delay):
          if (time.time() - self.shot_timer > self.shot_delay and self.num_shot_already < self.plant_config["num_shots"]):
            self.costume = "attack"
            self.attack_costume_timer = time.time()

            if self.plant_type == "pranav":
              particleSystem.pranav_smoke_blow(self.tile.target_location_x, self.tile.target_location_y) 

            self.lane.add_projectile(Projectile(self, self.projectile_type))
            self.shot_timer = time.time()
            self.num_shot_already += 1
            if self.num_shot_already >= self.plant_config["num_shots"]:
              self.num_shot_already = 0
              self.attack_timer = time.time()

  class Pranav(PeaShooter):
    def __init__(self, tile, lane):
      super().__init__("pranav", tile, lane)

    def render(self, render):
      render = super().render(render)
      health_bar_height = int(self.plant_image_config["height"] * (self.health / self.plant_config["health"]))
      background_solid = Solid((0, 0, 0, 255), xsize=int(self.plant_image_config["width"]), ysize=int(self.plant_image_config["height"] - health_bar_height))
      render.place(background_solid, x = self.x_location, y = self.y_location)
      return render

  class Logan(PeaShooter):
    def __init__(self, tile, lane):
      super().__init__("logan", tile, lane)

    def render(self, render):
      render = super().render(render)
      if (time.time() - self.attack_timer <= self.attack_delay):
        timer_text = Text(str(round((time.time() - self.attack_timer), 1)), size=20, color=(255, 255, 255, 255))
        render.place(timer_text, x = self.x_location, y = self.y_location)
      return render

  class Wallnut(Plant):
    def __init__(self, tile, lane):
      super().__init__(tile, lane, "wallnut")

  class Sunflower(Plant):
    def __init__(self, tile, lane, gui_controller):
      super().__init__(tile, lane, "sunflower")
      self.sun_timer = time.time()
      self.sun_delay = self.plant_config["sun_delay"]
      self.glow_seconds_before_sun = self.plant_config["glow_seconds_before_sun"]
      self.gui_controller = gui_controller

    def update(self):
      super().update()
      if (time.time() - self.sun_timer) + self.glow_seconds_before_sun > self.sun_delay:
        self.costume = "glowing"
      else:
        self.costume = "default"

      if time.time() - self.sun_timer > self.sun_delay:
        sun_spawn_x = self.plant_image_config["sun_spawn_x"] + self.x_location
        sun_spawn_y = self.plant_image_config["sun_spawn_y"] + self.y_location
        self.gui_controller.add_sun(sun_spawn_x, sun_spawn_y, self.tile.target_location_y - 20, False)
        self.sun_timer = time.time()
    

      

  class Body_Part():
    def __init__(self, zombie, part_name):
      self.zombie = zombie
      self.animation_type = zombie.animation_type
      self.zombie_image_config = config_data.get_zombie_image_config(self.animation_type)
      self.zombie_config = config_data.get_zombie_config(self.zombie.zombie_type)

      self.has_damage_frames = False
      if self.zombie_config["has_damage_frames"] and part_name in self.zombie_config["damage_frame_order"].keys():
        self.has_damage_frames = True

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

      if self.part_name in ["left_tire", "right_tire"]:
        self.part_type = "tire"

      self.motion_config = config_data.get_zombie_motion_config(self.zombie.motion_type)[self.part_name]

      self.limit = None
      self.direction = None
      self.motion_type = None
      self.angle = 0
      self.update_motion_params(reset_angles=True)

      self.image = all_images.images["zombies"][self.zombie.zombie_type][self.zombie.costume][self.part_type]
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

    def determine_damage_frame(self):
      health = self.zombie.health
      damage_frames = self.zombie_config["damage_frame_order"][self.part_name]
      damage_frame = None
      for frame in damage_frames.keys():
        if health <= (self.zombie_config["health"] * (1-damage_frames[frame])):
          damage_frame = frame
      return damage_frame

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
      if not self.zombie.blackened:
        if self.has_damage_frames and self.determine_damage_frame() is not None:
          damage_frame = self.determine_damage_frame()
          costume = damage_frame
          if self.zombie.costume.startswith("damaged_"):
            costume = "damaged_"+costume
          if self.zombie.costume.endswith("iced"):
            costume = costume + "-iced"
          self.image = all_images.images["zombies"][self.zombie.zombie_type][costume][self.part_type]
        else:
          self.image = all_images.images["zombies"][self.zombie.zombie_type][self.zombie.costume][self.part_type]
      else:
        self.image = all_images.images["zombies"][self.zombie.zombie_type]["blackened"][self.part_type]

      if self.status == "attached":
        transformed_image, x_location, y_location = self.process_rotation()
        render.place(transformed_image, x=x_location, y=y_location)
      elif self.status == "detached":

        costume_name = self.zombie.costume
        if costume_name.startswith("damaged_") and not self.zombie.blackened:
          costume_name = costume_name.replace("damaged_", "")

        if self.zombie.blackened:
          costume_name = "blackened"

        self.image = all_images.images["zombies"][self.zombie.zombie_type][costume_name][self.part_type]
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
          rotate_speed = self.motion_config["speed"][str(self.direction)]
          if self.zombie.is_iced:
            rotate_speed = rotate_speed * 0.5

          self.angle += (self.direction * rotate_speed * delta_time * delta_multiplier)
          if (self.angle < self.limit[0]):
            self.direction = 1
          if (self.angle > self.limit[1]):
            self.direction = -1

        if self.motion_type == "fall":
          if self.part_name == "torso":
            self.zombie.y_location += self.motion_config["speed"] * delta_time * delta_multiplier
      elif self.status == "detached":
        if self.zombie_x_timestamp == None:
          self.zombie_x_timestamp = self.zombie.x_location

        self.target_location_x += self.velocity_x * delta_time * delta_multiplier
        self.distance_fallen += self.velocity_y * delta_time * delta_multiplier
        self.velocity_y += GRAVITY_CONSTANT

        if self.distance_fallen > (self.zombie_image_config["fall_height"] - self.target_location_y):
          self.velocity_y = 0
          self.velocity_x = 0
          self.status = "fading"
      elif self.status == "fading":
        if self.fade_start_time == None:
          self.fade_start_time = time.time()
        if time.time() - self.fade_start_time > 0.2:
          self.status = "gone"

    def update_motion_params(self, reset_angles = False):
      self.motion_config = config_data.get_zombie_motion_config(self.zombie.motion_type)[self.part_name]
      if self.motion_config["type"] == "rotate":
        self.limit = self.motion_config["limit"]
        self.motion_type = self.motion_config["type"]

        if reset_angles:
          if self.motion_config["start_angle"] != "none":
            self.angle = self.motion_config["start_angle"] + renpy.random.randint(-self.motion_config["start_angle_variance"], self.motion_config["start_angle_variance"])
          if self.motion_config["start_direction"] != "none":
            self.direction = self.motion_config["start_direction"]
      elif self.motion_config["type"] == "fall":
        self.motion_type = self.motion_config["type"]
      else:
        self.motion_type = None

      

  class Zombie():
    def __init__(self, x_location, y_location, zombie_type, lane):
      self.lane = lane
      self.zombie_type = zombie_type
      self.animation_type = config_data.get_zombie_config(zombie_type)["animation_type"]
      self.image_config = config_data.get_zombie_image_config(self.animation_type)
      self.zombie_config = config_data.get_zombie_config(zombie_type)

      self.x_location = x_location
      self.y_location = self.lane.tiles[0].target_location_y - self.image_config["fall_height"]

      self.costume = "default"
      self.damaged_timer = None

      self.is_iced = False
      self.ice_timer = None

      self.motion_type = renpy.random.choice(config_data.get_zombie_config(zombie_type)["motions"])
      self.motion_config = config_data.get_zombie_motion_config(self.motion_type)
      self.status = "moving"

      self.is_dead = False
      self.should_delete = False

      self.health = config_data.get_zombie_config(zombie_type)["health"]
      self.speed = config_data.get_zombie_config(zombie_type)["speed"]
      self.attack = config_data.get_zombie_config(zombie_type)["attack"]
      self.hitbox_distance = config_data.get_zombie_config(zombie_type)["hitbox_distance"]
      self.hitbox_width = config_data.get_zombie_config(zombie_type)["hitbox_width"]

      self.attack_motions = config_data.get_zombie_config(zombie_type)["attack_motions"]
      self.death_motions = config_data.get_zombie_config(zombie_type)["death_motions"]
      self.zombie_class = self.image_config["class"]

      self.body_parts = [Body_Part(self, part_name) for part_name in self.image_config["part_name_order"]]
      self.blackened = False

      self.target_plant = None

    def render(self, render):
      for body_part in self.body_parts:
        render = body_part.render(render)
      return render

    def update_motion(self):
      self.motion_config = config_data.get_zombie_motion_config(self.motion_type)
      for body_part in self.body_parts:
        body_part.update_motion_params()

    def get_iced(self):
      if self.image_config["class"] != "shield":
        self.is_iced = True
        self.ice_timer = time.time()
        self.costume = "iced"

    def check_damage_limb_detach(self):
      info = self.image_config["damage_fall_order"]
      for part_name in info.keys():
        if self.health <= ((1-info[part_name]) * zombie_config[self.zombie_type]["health"]):
          part = [part for part in self.body_parts if part.part_name == part_name]
          if len(part) > 0:
            part[0].status = "detached"

    def damage(self, damage):
      self.health -= damage
      self.check_damage_limb_detach()
      if not self.costume.startswith("damaged_"):
        self.costume = "damaged_" + self.costume
        self.damaged_timer = time.time()
      if self.health <= 0:
        self.die()

    def start_eating(self, plant):
      self.target_plant = plant
      self.motion_type = renpy.random.choice(self.attack_motions)
      self.update_motion()

    def check_attack_plant(self):
      if hasattr(self, "target_plant") and self.target_plant is not None: # check if target_plant still exists
        self.target_plant.damage(self.attack)

        if self.target_plant.is_dead:
          self.target_plant = None
          self.motion_type = renpy.random.choice(config_data.get_zombie_config(self.zombie_type)["motions"])
          self.update_motion()

    def die(self):
      self.speed = 0
      self.is_dead = True
      self.motion_type = renpy.random.choice(self.death_motions)
      self.update_motion()

    def update(self):
      walk_speed = self.speed
      if self.is_iced:
        walk_speed = walk_speed * 0.5

      if self.motion_config["moving"]:
        self.x_location -= (walk_speed * delta_time * delta_multiplier)

      if self.is_iced and time.time() - self.ice_timer > 5:
        self.is_iced = False
        self.costume = "default"

      if self.costume.startswith("damaged_") and time.time() - self.damaged_timer > 0.05:
        self.costume = self.costume.replace("damaged_", "")

      self.check_attack_plant()
      
      if self.health <= 0:
        self.die()

      if self.x_location < -10:
        self.should_delete = True
        self.is_dead = True

      if self.zombie_class not in ["vehicle", "shield"]:
        head = [part for part in self.body_parts if part.part_name == "head"]
        if not head or head[0].status == "gone":
          self.should_delete = True

      self.body_parts = [part for part in self.body_parts if part.status != "gone"]
      for body_part in self.body_parts:
        body_part.update()

      if self.blackened:
        self.costume = "blackened"

  class Shield(Zombie):
    def __init__(self, x_location, y_location, lane, bearer):
      super().__init__(x_location, y_location, "shield", lane)
      self.bearer = bearer

    def start_eating(self, plant):
      pass

    def update(self):
      if self.costume.startswith("damaged_") and time.time() - self.damaged_timer > 0.05:
        self.costume = self.costume.replace("damaged_", "")

      if not self.bearer.is_dead:
        true_angle = math.radians(-90 - self.bearer.body_parts[1].angle)
        hand_location_x = math.cos(true_angle) * self.bearer.body_parts[1].image_height *0.7
        hand_location_y = math.sin(true_angle) * self.bearer.body_parts[1].image_height * 0.7

        torso_joint_x = self.body_parts[0].image_width
        torso_joint_y = self.body_parts[0].image_height

        self.x_location = int(self.bearer.x_location + hand_location_x - torso_joint_x)
        self.y_location = int(self.bearer.y_location - hand_location_y - torso_joint_y)

      #send_to_file("logz.txt", "angle: " + str(true_angle) + ", "+str(self.bearer.x_location) + " , " + str(hand_location_x) + " , " + str(torso_joint_x) + " , final = " + str(self.x_location) + "\n")

      if not self.bearer or self.bearer.is_dead or self.health <= 0:
        self.die()
        self.should_delete = True

  class ArmoredShield(Shield):
    def __init__(self, x_location, y_location, lane, bearer):
      super().__init__(x_location, y_location, lane, bearer)
      self.zombie_type = "armored_shield"

  # basic zombie covers all zombies that don't have a special class, such as dog
  class BasicZombie(Zombie):
    def __init__(self, x_location, y_location, zombie_type, lane):
      super().__init__(x_location, y_location, zombie_type, lane)
      self.attack_timer = time.time()

    def check_attack_plant(self):
      attack_delay = 1
      if self.is_iced:
        attack_delay = 2

      if hasattr(self, "target_plant") and self.target_plant is not None: # check if target_plant still exists
        if (time.time() - self.attack_timer > attack_delay):
          self.target_plant.damage(self.attack)
          self.attack_timer = time.time()

        if self.target_plant.is_dead:
          self.target_plant = None
          self.motion_type = renpy.random.choice(config_data.get_zombie_config(self.zombie_type)["motions"])
          self.update_motion()

  class NeilZombie(BasicZombie):
    def __init__(self, x_location, y_location, lane):
      super().__init__(x_location, y_location, "neil", lane)
      self.transform_timer = time.time()
      self.transform_interval = 20
      self.eye_effect = None

      self.lanes = self.lane.lanes
      self.transform_delay_timer = None
      self.transform_delay = 2.5


    def find_eye_location(self):
      eye_x = None
      eye_y = None
      if len(self.body_parts) > 5:
        eye_x = self.x_location + self.body_parts[-2].target_location_x - self.body_parts[-2].joint_location_x + (self.body_parts[-2].image_width / 5)
        eye_y = self.y_location + self.body_parts[-2].target_location_y - self.body_parts[-2].joint_location_y + (self.body_parts[-2].image_height / 2)
      else:
        eye_x = self.x_location + self.body_parts[-1].target_location_x - self.body_parts[-1].joint_location_x + (self.body_parts[-1].image_width / 5)
        eye_y = self.y_location + self.body_parts[-1].target_location_y - self.body_parts[-1].joint_location_y + (self.body_parts[-1].image_height / 2)
      return eye_x, eye_y

    def start_transform(self):
      if self.is_dead:
        return
      self.motion_type = "stay_still"
      self.update_motion()
      eye_x, eye_y = self.find_eye_location()
      self.eye_effect = EyeEffect(eye_x, eye_y-5, is_tranformation=True)
      self.transform_delay_timer = time.time()
    
    def transform(self):
      self.lanes.transform_basic_and_conehead_to_kinetic()
      
    def update(self):
      super().update()
      if time.time() - self.transform_timer > self.transform_interval:
        if self.lanes.has_basic_or_conehead():
          self.transform_timer = time.time()
          self.start_transform()

      if self.eye_effect:
        self.eye_effect.update()

      if self.transform_delay_timer and time.time() - self.transform_delay_timer > self.transform_delay and not self.is_dead:
        self.transform_delay_timer = None
        self.transform()
        self.eye_effect.stop_growth = True
        self.eye_effect = None
        self.motion_type = renpy.random.choice(config_data.get_zombie_config(self.zombie_type)["motions"])
        self.update_motion()
        self.target_plant = None

    def render(self, render):
      render = super().render(render)
      if self.eye_effect and not self.is_dead:
        render = self.eye_effect.render(render)
      return render

  class KanishkZombie(Zombie):
    def __init__(self, x_location, y_location, lane):
      super().__init__(x_location, y_location, "kanishk", lane)
      self.target_steal_plant = self.lane.get_most_expensive_plant()
      self.has_stolen_plant = False

    def walk_backwards(self):
      if self.speed < 0:
        return
      self.speed = self.zombie_config["speed"] * -0.5
      self.motion_type = "walk_shield"
      self.update_motion()

    def start_eating(self, plant):
      if not self.target_steal_plant or self.has_stolen_plant:
        return
      if plant.x_location == self.target_steal_plant.x_location and not self.has_stolen_plant and not self.target_steal_plant.plant_type == "jacob":
        self.has_stolen_plant = True
        self.target_steal_plant = copy.copy(plant)
        self.target_steal_plant.is_being_stolen = True
        plant.is_dead = True
        if plant.is_protected:
          self.game.has_protected_plant_died = True
        plant.tile.is_planted = False
        if plant.plant_type == "cobcannon":
          if plant.target_marker is not None:
            plant.target_marker.impacted()
        self.walk_backwards()
        renpy.play(AUDIO_DIR + "heheha.mp3", channel = "audio")

    def check_attack_plant(self):
      pass

    def render(self, render):
      render = super().render(render)
      if self.has_stolen_plant and self.target_steal_plant:
        plant_image = all_images.images["plants"][self.target_steal_plant.plant_type]["animation"]["default"][0]
        render.place(plant_image, x = self.x_location-self.target_steal_plant.plant_image_config["width"]-40, y = self.y_location)
      else:
        if self.target_steal_plant and not self.is_dead:
          target_image = all_images.images["gui"]["evil"]
          render.place(target_image, x = self.target_steal_plant.tile.target_location_x - 70, y = self.target_steal_plant.tile.target_location_y - 180)
      return render

    def die(self):
      if self.target_steal_plant and self.has_stolen_plant:
        new_plant_tile = self.lane.x_location_to_tile(self.x_location)
        plant_currently_on_tile = new_plant_tile.get_plant_on_tile()
        if plant_currently_on_tile:
          plant_currently_on_tile.die()

        new_plant = self.lane.lanes.add_plant_tile(new_plant_tile, self.target_steal_plant.plant_type)
        new_plant.health = self.target_steal_plant.health
        if self.target_steal_plant.plant_type == "cobcannon":
          new_plant.is_ready_to_fire = False
          new_plant.attack_timer = time.time()
        self.target_steal_plant = None
      super().die()

    def does_target_plant_exist(self):
      if self.target_steal_plant in self.lane.plants:
        return True
      return False

    def update(self):
      super().update()
      if not self.has_stolen_plant and self.speed < 0:
        walk_speed = self.speed
        if self.is_iced:
          walk_speed = walk_speed * 0.5
        if self.motion_config["moving"]:
          self.x_location -= (walk_speed * delta_time * delta_multiplier)

      if self.target_steal_plant and not self.has_stolen_plant:
        if self.target_steal_plant.is_being_stolen or not self.does_target_plant_exist():
          self.target_steal_plant = self.lane.get_most_expensive_plant()
          if self.target_steal_plant and self.target_steal_plant.x_location > self.x_location:
            self.walk_backwards()

      if not self.target_steal_plant and self.x_location < 1200 and self.speed > 0:
        self.target_steal_plant = self.lane.get_most_expensive_plant()
        if not self.target_steal_plant:
          self.walk_backwards()

      if self.target_steal_plant and self.target_steal_plant.x_location > self.x_location:
        self.walk_backwards()

      if self.x_location > 1550 and self.speed < 0:
        self.should_delete = True
        self.is_dead = True
        


  class KineticZombie(Zombie):
    def __init__(self, x_location, y_location, lane):
      super().__init__(x_location, y_location, "kinetic", lane)
      self.attack_timer = time.time()
      self.post_kill_timer = None
      self.eye_effect = None
      self.laser_effect = None

      self.electricity_sound_timer = time.time()

      self.pause_timer = None

    def find_eye_location(self):
      eye_x = None
      eye_y = None
      if len(self.body_parts) > 5:
        eye_x = self.x_location + self.body_parts[-2].target_location_x - self.body_parts[-2].joint_location_x + (self.body_parts[-2].image_width / 5)
        eye_y = self.y_location + self.body_parts[-2].target_location_y - self.body_parts[-2].joint_location_y + (self.body_parts[-2].image_height / 2)
      else:
        eye_x = self.x_location + self.body_parts[-1].target_location_x - self.body_parts[-1].joint_location_x + (self.body_parts[-1].image_width / 5)
        eye_y = self.y_location + self.body_parts[-1].target_location_y - self.body_parts[-1].joint_location_y + (self.body_parts[-1].image_height / 2)
      return eye_x, eye_y

    def start_eating(self, plant):
      if plant.plant_type == "jacob" or self.pause_timer:
        return 
      self.target_plant = plant
      self.motion_type = renpy.random.choice(self.attack_motions)
      self.attack_delay_timer = time.time()

      eye_x, eye_y = self.find_eye_location()
      self.eye_effect = EyeEffect(eye_x, eye_y)
      self.update_motion()
      
    def check_attack_plant(self):
      attack_delay = 2

      if hasattr(self, "target_plant") and self.target_plant is not None: # check if target_plant still exists
        if (time.time() - self.attack_delay_timer > attack_delay and self.is_dead == False):
          eye_x, eye_y = self.find_eye_location()
          if self.eye_effect:
            self.eye_effect.stop_growth = True
          self.laser_effect = LaserEffect(eye_x, eye_y, self.target_plant.tile.target_location_x, self.target_plant.tile.target_location_y)
          self.target_plant.damage(self.attack)
          self.attack_timer = time.time()

        if self.target_plant.is_dead:
          self.target_plant = None
          self.post_kill_timer = time.time()

    def pause_two_seconds(self):
      self.motion_type = renpy.random.choice(self.attack_motions)
      self.update_motion()
      self.pause_timer = time.time()
    
    def render(self, render):
      render = super().render(render)
      if self.eye_effect and not self.is_dead:
        render = self.eye_effect.render(render)
      if self.laser_effect:
        render = self.laser_effect.render(render)
      return render

    def update(self):
      super().update()
      if self.zombie_type == "kinetic":
        legs = [part for part in self.body_parts if part.part_type == "legs"]
        for leg in legs:
          min_angle = 3
          if self.is_iced:
            min_angle = 1
          if leg.angle and abs(leg.angle) < min_angle and self.motion_type == "walk":
            if time.time() - self.electricity_sound_timer > 1:
              self.electricity_sound_timer = time.time()
              renpy.play(AUDIO_DIR + "voltage.mp3", channel = "audio")
              particleSystem.electricity(self.x_location, self.y_location + self.image_config["fall_height"], 30) 
      
      eye_x, eye_y = self.find_eye_location()
      if self.eye_effect:
        self.eye_effect.update()
      if self.laser_effect:
        self.laser_effect.update(eye_x, eye_y)

      if self.pause_timer and time.time() - self.pause_timer > 2:
        self.pause_timer = None
        self.motion_type = renpy.random.choice(config_data.get_zombie_config(self.zombie_type)["motions"])
        self.update_motion()

      if self.post_kill_timer and time.time() - self.post_kill_timer > 1.5:
        self.motion_type = renpy.random.choice(config_data.get_zombie_config(self.zombie_type)["motions"])
        self.update_motion()
        self.post_kill_timer = None
        self.eye_effect = None
        self.laser_effect = None

  class VanZombie(Zombie):
    def __init__(self, x_location, y_location, lane):
      super().__init__(x_location, y_location, "van", lane)
      self.death_time_duration = 1
      self.death_time = None
      self.last_shudder_movement = 0
      renpy.play(AUDIO_DIR + "van-starting.mp3", channel = "audio")

    def die(self):
      self.speed = 0
      self.is_dead = True
      if self.death_time == None:
        self.death_time = time.time()
    
    def update(self):
      super().update()
      if self.death_time != None:
        shudder = renpy.random.randint(-15, 15)
        self.x_location += (shudder - self.last_shudder_movement)
        self.last_shudder_movement = shudder
        if (time.time() - self.death_time) > self.death_time_duration:
          for i in range(1, 4):
            self.lane.add_zombie(BasicZombie(self.x_location + 50*i, self.y_location, "basic", self.lane))
            particleSystem.summon(self.x_location + 60*i, self.y_location + 150)
          renpy.play(AUDIO_DIR + "van-destroyed.mp3", channel = "audio")
          self.should_delete = True

    def check_attack_plant(self):
      if hasattr(self, "target_plant") and self.target_plant is not None: # check if target_plant still exists
        if self.target_plant.plant_type == "jacob":
          return
        self.target_plant.damage(self.attack)
        renpy.play(AUDIO_DIR + "plant-crushed.mp3", channel = "audio")

        if self.target_plant.is_dead:
          self.target_plant = None
          self.motion_type = renpy.random.choice(config_data.get_zombie_config(self.zombie_type)["motions"])
          self.update_motion()






  class Lane():
    def __init__(self, id, lanes):
      self.id = id
      self.y_location = None
      self.target_location_y = None
      self.tiles = []
      self.plants = []
      self.zombies = []
      self.projectiles = []
      self.lanes = lanes

    def populate_tiles(self, tiles):
      self.tiles = tiles
      self.y_location = tiles[0].y_location
      self.target_location_y = tiles[0].target_location_y

    def get_tile_by_row_id(self, row_id):
      temp = [tile for tile in self.tiles if tile.row_id == row_id]
      if len(temp) > 0:
        return temp[0]
      else:
        return None

    def get_most_expensive_plant(self):
      plants = self.plants
      if len(plants) > 0:
        return max(plants, key=lambda plant: plant.cost)
      else:
        return None

    def x_location_to_tile(self, x_location):
      return [tile for tile in self.tiles if tile.x_location < x_location and tile.x_location + tile.width > x_location][0]

    def add_plant(self, plant):
      self.plants.append(plant)

    def add_zombie(self, zombie):
      self.zombies.append(zombie)

    def add_projectile(self, projectile):
      self.projectiles.append(projectile)

    def return_all_zombies_on_tile(self, tile):
      return [zombie for zombie in self.zombies if (zombie.x_location + zombie.hitbox_width) > tile.x_location and zombie.x_location < tile.x_location + tile.width]

    def get_zombies(self):
      return self.zombies

    def transform_basic_and_conehead_to_kinetic(self):
      did_transform_anything = False
      for zombie in self.zombies:
        if zombie.zombie_type in ["basic", "conehead"]:
          zombie.should_delete = True
          zombie.is_dead = True
          did_transform_anything = True
          kinetic = KineticZombie(zombie.x_location, zombie.y_location, self)
          particleSystem.transformation(zombie.x_location+20, zombie.y_location + zombie.image_config["fall_height"])
          self.add_zombie(kinetic)
          kinetic.pause_two_seconds()
      return did_transform_anything


    def has_zombies(self):
      return len(self.zombies) > 0

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

      order = [self.plants, self.zombies, self.projectiles]
      for update_target in order:
        for target in update_target:
          target.update()


    def render(self, render):
      order = [self.tiles, self.plants, self.zombies, self.projectiles]
      for render_target in order:
        for target in render_target:
          render = target.render(render)
      return render

  class Lanes:
    def __init__(self, num_lanes):
        self.lanes = [Lane(i, self) for i in range(num_lanes)]
        self.gui_controller = None

    def set_gui_controller(self, gui_controller):
        self.gui_controller = gui_controller

    def add_plant_xy(self, x, y, plant):
        tile = self.pos_to_tile(x, y)
        lane_index = tile.lane_id
        plant = Plant(tile, self.lane_id_to_lane(tile.lane_id), plant)
        self.lanes[lane_index].add_plant(plant)

    def add_plant_tile(self, tile, plant, is_protected=False):
        plant_name = plant
        plant = plant_name_to_plant(tile, self.lane_id_to_lane(tile.lane_id), plant, self.gui_controller)
        if is_protected:
          plant.is_protected = True
          tile.is_protected = True
        self.lanes[tile.lane_id].add_plant(plant)
        if plant_name != "andrew":
          tile.is_planted = True
        return plant

    def get_all_plants(self):
      plants = []
      for lane in self.lanes:
          plants += lane.plants
      return plants

    def get_most_expensive_plant(self):
      plants = self.get_all_plants()
      if len(plants) > 0:
        return max(plants, key=lambda plant: plant.cost)
      else:
        return None

    def has_expensive_plant(self):
      plants = self.get_all_plants()
      for plant in plants:
        if plant.cost >= 175:
          return True
      return False

    def lane_indexes_with_expensive_plants(self):
      indexes = []
      plants = self.get_all_plants()
      for plant in plants:
        if plant.cost >= 175:
          indexes.append(plant.tile.lane_id)
      return indexes

    def remove_plant(self, lane_index, plant):
        self.lanes[lane_index].remove_plant(plant)

    def add_zombie(self, lane_index, zombie):
        self.lanes[lane_index].add_zombie(zombie)

    def remove_zombie(self, lane_index, zombie):
        self.lanes[lane_index].remove_zombie(zombie)

    def has_basic_or_conehead(self):
      for lane in self.lanes:
        for zombie in lane.zombies:
          if zombie.zombie_type in ["basic", "conehead"]:
            return True
      return False

    def transform_basic_and_conehead_to_kinetic(self):
      did_transform_anything = False
      for lane in self.lanes:
        did_transform_anything = lane.transform_basic_and_conehead_to_kinetic() or did_transform_anything
      
      if did_transform_anything:
        renpy.play(AUDIO_DIR + "transformation.mp3", channel = "audio")

    def has_zombies(self):
      for lane in self.lanes:
        if lane.has_zombies():
          return True
      return False

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
        for tile in tiles:
          tile.lane = self.lanes[lane_index]
        self.lanes[lane_index].populate_tiles(tiles)

    def update(self):
      for lane in self.lanes:
        lane.update()
      particleSystem.update()

    def render(self, render):
      for lane in self.lanes:
        render = lane.render(render)
      render = particleSystem.render(render)
      return render

    def pos_to_tile(self, x, y):
      for lane in self.lanes:
        for tile in lane.tiles:
          if tile.x_location <= x <= tile.x_location + tile.width and tile.y_location <= y <= tile.y_location + tile.height:
              return tile
      return None

    def lane_id_and_tile_id_to_tile(self, lane_id, tile_id):
      return self.lanes[lane_id].tiles[tile_id]

    def lane_id_to_lane(self, lane_id):
      return self.lanes[lane_id]

  class Explosion():
    def __init__(self, x, y, explosion_type):
      self.x = x
      self.y = y
      self.explosion_type = explosion_type
      self.animation_frames = all_images.images["explosions"][explosion_type]
      self.animation_index = 0
      self.animation_timer = time.time()
      self.animation_delay = 0.02
      self.is_dead = False
      
      renpy.play(AUDIO_DIR + "hellfire-explosion.mp3", channel = "audio")

    def update(self):
      if time.time() - self.animation_timer > self.animation_delay:
        self.animation_timer = time.time()
        self.animation_index += 1
        if self.animation_index >= len(self.animation_frames):
          self.is_dead = True

    def render(self, render):
      render.place(self.animation_frames[self.animation_index], x = self.x, y = self.y)
      return render

  class Missile():
    def __init__(self, target_location_x, target_location_y, explosion_controller, cobcannon, target_marker):
      self.target_location_x = target_location_x
      self.target_location_y = target_location_y
      self.explosion_controller = explosion_controller
      self.cobcannon = cobcannon
      self.target_marker = target_marker
      
      self.should_delete = False
      self.current_y = 100

      self.speed = int((target_location_y - 100)/10)

      renpy.play(AUDIO_DIR + "hellfire-flare.mp3", channel = "audio")

    def update(self):
      self.current_y += self.speed
      if self.current_y >= self.target_location_y:
        self.explosion_controller.add_explosion(self.target_location_x, self.target_location_y, "hellfire")
        self.cobcannon.missile_exploded()
        self.target_marker.impacted()
        self.should_delete = True

    def render(self, render):
      missile_image = all_images.images["gui"]["hellfire"]
      render.place(missile_image, x = self.target_location_x - 25, y = self.current_y - 100)
      return render


  class ExplosionController():
    def __init__(self, lanes):
      self.missiles = []
      self.explosions = []
      self.lanes = lanes

    def check_blacken(self, zombie):
      if zombie.is_dead:
        if config_data.get_zombie_config(zombie.zombie_type)["blacken_on_explosion"]:
          zombie.blackened = True

    def damage_zombies(self, x, y, explosion_type):
      tile = self.lanes.pos_to_tile(x, y)
      lane_id = tile.lane_id
      tile_id = tile.row_id
      explosion_config = config_data.get_explosion_config(explosion_type)
      horizontal_spread = explosion_config["horizontal_spread"]
      vertical_spread = explosion_config["vertical_spread"]
      direct_damage = explosion_config["damage"]
      splash_damage = explosion_config["splash"]

      lane = self.lanes.lanes[lane_id]
      tile = lane.tiles[tile_id]
      direct_hit_zombies = lane.return_all_zombies_on_tile(tile)
      for zombie in direct_hit_zombies:
        zombie.damage(direct_damage)
        self.check_blacken(zombie)

      splash_zombies = []

      for i in range(lane_id-vertical_spread, lane_id+vertical_spread+1):
        for j in range(tile_id-horizontal_spread, tile_id+horizontal_spread+1):
          if i < 0 or i >= len(self.lanes.lanes) or j < 0 or j >= len(self.lanes.lanes[i].tiles):
            continue
          else:
            lane = self.lanes.lanes[i]
            tile = lane.tiles[j]
            if (i != lane_id or j != tile_id):
              splash_zombies.extend(lane.return_all_zombies_on_tile(tile))
              splash_zombies = list(set(splash_zombies))

      for zombie in splash_zombies:
        zombie.damage(splash_damage)
        self.check_blacken(zombie)
        
    def add_missile(self, x, y, cobcannon, target_marker):
      missile = Missile(x, y, self, cobcannon, target_marker)
      self.missiles.append(missile)

    def add_explosion(self, x, y, explosion_type):
      explosion_config = config_data.get_explosion_config(explosion_type)
      
      image_x = x - explosion_config["joint_x"]
      image_y = y - explosion_config["joint_y"]
      explosion = Explosion(image_x, image_y, explosion_type)
      self.damage_zombies(x, y, explosion_type)
      self.explosions.append(explosion)
      particleSystem.explosion(x, y)

    def update(self):
      for explosion in self.explosions:
        explosion.update()
        if explosion.is_dead:
          self.explosions.remove(explosion)

      for missile in self.missiles:
        missile.update()
        if missile.should_delete:
          self.missiles.remove(missile)

    def render(self, render):
      for explosion in self.explosions:
        render = explosion.render(render)
      
      for missile in self.missiles:
        render = missile.render(render)
      return render

  class PlantSeedCard():
    def __init__(self, plant_name, slot_id):
      self.plant_name = plant_name
      self.plant_config = config_data.get_plant_config(plant_name)

      self.slot_id = slot_id
      self.width = 130
      self.height = 170
      self.x_location = 200 + slot_id * (self.width+20)
      self.y_location = 30

      self.recharge_timer = time.time()
      self.is_recharge_ready = True
      self.can_afford = False

      #graphics
      self.background_solid = Solid((50, 252, 104), xsize=self.width, ysize=self.height)
      self.image = im.FactorScale(all_images.images["plants"][self.plant_name]["animation"]["default"][0], 0.85)
      self.sun = im.FactorScale(all_images.images["gui"]["sun"], 0.7)
      self.cost_text = Text(str(self.plant_config["cost"]), size = 20)

    def render(self, render):
      render.place(self.background_solid, x = self.x_location, y = self.y_location)
      render.place(self.image, x = self.x_location+15, y = self.y_location+10)
      render.place(self.cost_text, x = self.x_location+40, y = (self.y_location+self.height)-35)
      render.place(self.sun, x = (self.x_location+self.width)-40, y = (self.y_location+self.height)-35)
      if not self.is_recharge_ready:
        self.gray_overlay = Solid((0, 0, 0, 100), xsize=self.width, ysize=self.height)
        render.place(self.gray_overlay, x = self.x_location, y = self.y_location)
        progress_overlay = Solid((0, 0, 0, 150), xsize=self.width, ysize=(self.height - int((self.height*(time.time() - self.recharge_timer))/self.plant_config["recharge_time"])))
        render.place(progress_overlay, x = self.x_location, y = self.y_location)
      else:
        if not self.can_afford:
          self.gray_overlay = Solid((0, 0, 0, 100), xsize=self.width, ysize=self.height)
          render.place(self.gray_overlay, x = self.x_location, y = self.y_location)
      return render

    def reset_recharge_timer(self):
      self.recharge_timer = time.time()
      self.is_recharge_ready = False

    def update(self, state):
      if time.time() - self.recharge_timer > self.plant_config["recharge_time"]:
        self.is_recharge_ready = True

      if state["sun_amount"] >= self.plant_config["cost"]:
        self.can_afford = True
      else:
        self.can_afford = False

  class Sun():
    def __init__(self, x, y, target_y, from_sky = True):
      self.x = x
      self.y = y
      self.target_y = target_y
      self.speed = 1
      self.from_sky = from_sky

      self.reached_target = False
      self.begin_collecting = False
      self.is_collected = False
      self.is_dead = False
      self.life_timer = time.time()
      self.image = im.FactorScale(all_images.images["gui"]["sun"], 1.3)

      self.collect_speed = 5
      self.collect_location_x = 50
      self.collect_location_y = 50

      self.x_distance = None
      self.y_distance = None

      self.y_velocity = None
      self.x_velocity = None

      self.background_size = 70
      self.size_limits = [60, 80]

      self.opacity = 150
      self.opacity_change = -3
      self.opacity_limits = [100, 180]
      self.size_change = 1
      self.background_color_yellow = (255, 255, 0, 150)
      self.background_angle = 0

      if not self.from_sky:
        self.y_velocity = -8
        self.x_velocity = renpy.random.randint(-1, 1)

    def update(self, state):
      mouse_x = state["mouseX"]
      mouse_y = state["mouseY"]

      if not self.begin_collecting:
        if time.time() - self.life_timer > 10:
          self.is_dead = True

        if self.from_sky:
          if self.y < self.target_y:
            self.y += self.speed * delta_multiplier * delta_time
        else:
          if not self.reached_target:
            self.y += self.y_velocity * delta_multiplier * delta_time
            self.x += self.x_velocity * delta_multiplier * delta_time
            self.y_velocity += GRAVITY_CONSTANT * delta_multiplier * delta_time

        if self.y > self.target_y:
          self.reached_target = True

      if mouse_x > self.x and mouse_x < self.x + 50 and mouse_y > self.y and mouse_y < self.y + 50:
        if not self.begin_collecting:
          self.x_distance = self.x - self.collect_location_x
          self.y_distance = self.y - self.collect_location_y
          self.begin_collecting = True
          renpy.play(AUDIO_DIR + "sun-collected.mp3", channel = "audio")

      if self.begin_collecting:
        distance = ((self.x_distance ** 2) + (self.y_distance ** 2)) ** 0.5
        if distance > 0:
          angle = math.atan2(self.y_distance, self.x_distance)
          collect_speed_x = math.cos(angle) * self.collect_speed
          collect_speed_y = math.sin(angle) * self.collect_speed
          self.x -= collect_speed_x * delta_multiplier * delta_time
          self.y -= collect_speed_y * delta_multiplier * delta_time

        self.collect_speed = 1.1 * self.collect_speed
        if self.x < self.collect_location_x or self.y < self.collect_location_y:
          self.is_collected = True
          self.is_dead = True

      if self.size_change == 1:
        self.background_size += 1
        if self.background_size > self.size_limits[1]:
          self.size_change = -1
      else:
        self.background_size -= 1
        if self.background_size < self.size_limits[0]:
          self.size_change = 1

      self.opacity += self.opacity_change
      if self.opacity > self.opacity_limits[1] or self.opacity < self.opacity_limits[0]:
        self.opacity_change *= -1


      self.background_angle += 1 * delta_multiplier * delta_time

    def process_rotation(self):
      self.background_color_yellow = (255, 255, 0, self.opacity)
      transformed_image = Transform(Solid(self.background_color_yellow, xsize=self.background_size, ysize=self.background_size), rotate=self.background_angle, anchor = (0, 0), transform_anchor = True)
      # Calculate the offset of the joint after rotation
      dx = int(self.background_size /2) 
      dy = int(self.background_size /2) 
      current_angle = math.atan2(dy, dx)
      new_angle = current_angle + math.radians(self.background_angle)

      new_dx = dx * math.cos(math.radians(self.background_angle)) - dy * math.sin(math.radians(self.background_angle))
      new_dy = dx * math.sin(math.radians(self.background_angle)) + dy * math.cos(math.radians(self.background_angle))

      # Calculate the position of the transformed image
      x_location = self.x - new_dx + 37
      y_location = self.y - new_dy + 33
      return transformed_image, x_location, y_location


    def render(self, render):
      # rotate background and center it
      background_image,background_x, background_y = self.process_rotation()
      render.place(background_image, x = background_x, y = background_y)

      render.place(self.image, x = self.x, y = self.y)
      return render

  class TargetMarker():
    def __init__(self, x, y, cobcannon):
      self.x = x
      self.y = y
      self.image = all_images.images["gui"]["target"]
      self.should_delete = False
      self.cobcannon = cobcannon
    
    def render(self, render):
      render.place(self.image, x = self.x - 65, y = self.y - 40)
      if hasattr(self, "cobcannon") and self.cobcannon is None:
        self.should_delete = True
      return render

    def impacted(self):
      self.should_delete = True

  class GUIController():
    def __init__(self, plant_names, level_config):
      self.plant_seed_cards = []
      self.last_sun_timer = time.time()
      self.suns = []
      self.target_markers = []
      self.sun_image = im.FactorScale(all_images.images["gui"]["sun"], 1.6)
      self.background_solid = Solid((160, 82, 45), xsize=150, ysize=200)
      self.explosion_controller = None
      self.lanes = None
      self.level_config = level_config

      self.targeting_image = im.FactorScale(all_images.images["gui"]["target"], 1)
      self.shovel_image = shovel_image = im.FactorScale(all_images.images["gui"]["shovel"], 1)
      self.is_targeting = False
      self.targeted_location_x = None
      self.targeted_location_y = None

      self.notification_message = None
      self.notification_message_timer = time.time()

      self.wave_message = None
      self.wave_message_timer = time.time()

      self.story_header = None
      self.story_message = None
      self.story_message_timer = time.time()
      self.story_zombie_image = None

      for i in range(len(plant_names)):
        self.plant_seed_cards.append(PlantSeedCard(plant_names[i], i))

    def display_notification(self, message):
      self.notification_message = message
      self.notification_message_timer = time.time()

    def dispay_wave_message(self, message):
      self.wave_message = message
      self.wave_message_timer = time.time()

    def display_story_message(self, header, message, zombie_name):
      self.story_header = header
      self.story_message = message
      self.story_zombie_image = all_images.images["zombies"][zombie_name]["icon"]
      self.story_message_timer = time.time()

    def add_target_marker(self, x, y, cobcannon):
      target = TargetMarker(x, y, cobcannon)
      self.target_markers.append(target)
      return target

    def render(self, render, state):
      for plant_seed_card in self.plant_seed_cards:
        render = plant_seed_card.render(render)

      shovel_location = 150 * len(self.plant_seed_cards) + 200 + 20
      render.place(self.shovel_image, x = shovel_location, y = 30)

      for sun in self.suns:
        render = sun.render(render)

      cost_text = Text(str(state["sun_amount"]), size = 40)
      render.place(self.background_solid, x = 15, y = 15)
      render.place(self.sun_image, x = 50, y = 30)
      render.place(cost_text, x = 50, y = 100)

      if self.notification_message:
        notification_background = Solid((255, 255, 255, 180), xsize=(len(self.notification_message) * 25), ysize=110)
        # center the notification background in the x axis
        render.place(notification_background, x = int((1900/2) - (len(self.notification_message) * 25)/2), y = 870)
        notification_text = Text(self.notification_message, size = 40)
        render.place(notification_text, x = int((1900/2) - (len(self.notification_message) * 25)/2) + 20, y = 900)

      if self.wave_message:
        notification_background = Solid((255, 255, 255, 180), xsize=(len(self.wave_message) * 30), ysize=110)
        render.place(notification_background, x = int((1900/2) - (len(self.wave_message) * 25)/2), y = 470)
        notification_text = Text(self.wave_message, size = 40, bold = True, color = (255, 0, 0))
        render.place(notification_text, x = int((1900/2) - (len(self.wave_message) * 25)/2) + 20, y = 500)

      # place the story message and header at the bottom of the screen, image on the left, text on the right

      if self.story_message:
        notification_background = Solid((255, 255, 255, 180), xsize=1000, ysize=200)
        render.place(notification_background, x = 430, y = 900)
        render.place(self.story_zombie_image, x = 440, y = 910)
        notification_text = Text(self.story_header, size = 30, bold = True, color = (255, 0, 0))
        render.place(notification_text, x = 540, y = 930)
        notification_text = Text(self.story_message, size = 30)
        render.place(notification_text, x = 540, y = 980)

      if self.is_targeting and not self.targeted_location_x:
        render.place(self.targeting_image, x = state["mouseX"] - 65, y = state["mouseY"] - 40)

      if state["is_shovelling"]:
        render.place(self.shovel_image, x = state["mouseX"] - 40, y = state["mouseY"] - 40)

      if state["plant_selected"] and not self.is_targeting:
        render.place(all_images.images["plants"][state["plant_selected"]]["animation"]["default"][0], x = state["mouseX"] - 65, y = state["mouseY"] - 40)
      
      for target_marker in self.target_markers:
        render = target_marker.render(render)
        
      return render

    def process_click(self, state):
      x = state["mouseX"]
      y = state["mouseY"]

      if self.is_targeting:
        self.is_targeting = False
        self.targeted_location_x = x
        self.targeted_location_y = y

      if x > 150 * len(self.plant_seed_cards) + 200 + 20 and x < 150 * len(self.plant_seed_cards) + 200 + 20 + 100 and y > 30 and y < 30 + 100:
        state["is_shovelling"] = True
        state["plant_selected"] = None
        state["plant_seed_slot_selected"] = None
        renpy.play(AUDIO_DIR + "shovel-pickup.mp3", channel = "audio")
        return state

      plant_selected = state["plant_selected"]
      for plant_seed_card in self.plant_seed_cards:
        if x > plant_seed_card.x_location and x < plant_seed_card.x_location + plant_seed_card.width and y > plant_seed_card.y_location and y < plant_seed_card.y_location + plant_seed_card.height:
          if plant_seed_card.is_recharge_ready:
            if plant_seed_card.can_afford:
              plant_selected = plant_seed_card.plant_name
              state["plant_seed_slot_selected"] = plant_seed_card
            else:
              self.display_notification("Not enough Xs off!")
          else:
            self.display_notification("Not ready yet!")
      state["plant_selected"] = plant_selected
      return state

    def add_sun(self, x, y, target_y, from_sky):
      self.suns.append(Sun(x, y, target_y, from_sky))

    def update(self, state):
      if time.time() - self.last_sun_timer > self.level_config["sun_fall_delay"]:
        self.last_sun_timer = time.time()
        self.add_sun(renpy.random.randint(300, 1300), 150, renpy.random.randint(600, 900), True)

      if self.notification_message != None:
        if time.time() - self.notification_message_timer > 3:
          self.notification_message = None

      if self.wave_message != None:
        if time.time() - self.wave_message_timer > 3:
          self.wave_message = None

      if self.story_message != None:
        if time.time() - self.story_message_timer > 4:
          self.story_message = None

      for sun in self.suns:
        sun.update(state)
        if sun.is_dead:
          if sun.is_collected:
            state["sun_amount"] += 50
          self.suns.remove(sun)

      for plant_seed_card in self.plant_seed_cards:
        plant_seed_card.update(state)

      for target_marker in self.target_markers:
        if target_marker.should_delete:
          self.target_markers.remove(target_marker)

      return state

  class BufferedZombie():
    def __init__(self, zombie_spawner, zombie_type, lane, spawn_time):
      self.zombie_spawner = zombie_spawner
      self.zombie_type = zombie_type
      self.lane = lane
      self.spawn_time = spawn_time
      self.should_delete = False

    def update(self):
      if time.time() - self.spawn_time >= 0:
        self.spawn()
        self.should_delete = True

    def spawn(self):
      zombie = Zombie(self.zombie_spawner.spawn_x_location, self.lane.y_location, self.zombie_type, self.lane)
      if self.zombie_type in  ["basic", "dog", "conehead", "buckethead", "shield_bearer", "mask_shield_bearer", "officer"]:
        zombie = BasicZombie(self.zombie_spawner.spawn_x_location, self.lane.y_location, self.zombie_type, self.lane)
        if self.zombie_type in ["shield_bearer"]:
          shield = Shield(self.zombie_spawner.spawn_x_location, self.lane.y_location, self.lane, zombie)
          self.lane.add_zombie(shield)
          self.lane.add_zombie(zombie)
          return

        if self.zombie_type in ["mask_shield_bearer"]:
          shield = ArmoredShield(self.zombie_spawner.spawn_x_location, self.lane.y_location, self.lane, zombie)
          self.lane.add_zombie(shield)
          self.lane.add_zombie(zombie)
          return
        self.lane.add_zombie(zombie)
        return
      if self.zombie_type == "van":
        zombie = VanZombie(self.zombie_spawner.spawn_x_location, self.lane.y_location, self.lane)
      if self.zombie_type == "kinetic":
        zombie = KineticZombie(self.zombie_spawner.spawn_x_location, self.lane.y_location, self.lane)
      if self.zombie_type == "neil":
        zombie = NeilZombie(self.zombie_spawner.spawn_x_location, self.lane.y_location, self.lane)
      if self.zombie_type == "kanishk":
        zombie = KanishkZombie(self.zombie_spawner.spawn_x_location, self.lane.y_location, self.lane)
      self.lane.add_zombie(zombie)

  class ZombieSpawner():
    def __init__(self, level_config, lanes, gui_controller, difficulty_multiplier):
      self.start_time = time.time()
      self.level_config = level_config
      self.lanes = lanes
      self.spent_per_lane = [0,0,0,0,0]
      self.displayed_probs = [0,0,0,0,0]
      self.interval = 0
      self.fast_forward_seconds = 0
      self.max_interval = self.level_config["spawn"]["intervals"]
      self.has_finished = False
      self.announced_first_wave = False
      self.difficulty_multiplier = difficulty_multiplier
      self.gui_controller = gui_controller

      self.allow_fast_forward_timer = None

      self.wave_intervals = []
      for i in range(1, self.max_interval+1):
        if self.level_config["spawn"][str(i)]["type"] == "wave":
          self.wave_intervals.append(i)

      self.buffered_zombies = []
      self.spawn_x_location = 1600

      self.progress_bar_background = Solid((0, 0, 0, 255), xsize=404, ysize=44)

    def reset(self):
      self.start_time = time.time()
      self.interval = 0
      self.buffered_zombies = []
      
    def calculate_interval(self):
      initial_delay = self.level_config["spawn"]["initial_delay"]
      seconds_elapsed = time.time() - self.start_time + self.fast_forward_seconds
      if seconds_elapsed < initial_delay:
        return 0
      if not self.announced_first_wave:
        renpy.play(AUDIO_DIR + "opps-coming.mp3", channel = "audio")
        self.announced_first_wave = True
      interval = int((seconds_elapsed - initial_delay)/20) + 1
      if interval > self.max_interval:
        self.has_finished = True
        return self.max_interval
      return int((seconds_elapsed - initial_delay)/20) + 1

    def prepare_zombie_interval(self):
      current_time = time.time()
      interval_config = self.level_config["spawn"][str(self.interval)]

      if "message" in interval_config:
        self.gui_controller.display_story_message(interval_config["message"]["header"], interval_config["message"]["message"], interval_config["message"]["zombie_image_name"])

      zombie_types = self.level_config["spawn"]["probabilities"]
      budget = max((interval_config["budget"] * self.difficulty_multiplier), 1)
      zombies_to_spawn = []
      remaining_budget = budget
      if "must_spawn" in interval_config:
        for key, val in interval_config["must_spawn"].items():
          if key == "kanishk" and not self.lanes.has_expensive_plant():
            continue
          for i in range(val):
            zombies_to_spawn.append(key)
            remaining_budget -= config_data.get_zombie_config(key)["cost"]
      while remaining_budget > 0:
        can_afford = []
        weights = []
        for zombie in zombie_types.keys():
          if config_data.get_zombie_config(zombie)["cost"] <= remaining_budget and ("max_cost" not in interval_config or config_data.get_zombie_config(zombie)["cost"] <= interval_config["max_cost"]) and ("banned_zombies" not in interval_config or zombie not in interval_config["banned_zombies"]):
            if zombie == "kanishk" and not self.lanes.has_expensive_plant():
              continue
            can_afford.append(zombie)
            weights.append(zombie_types[zombie])
        if len(can_afford) == 0:
          break
        zombie = random.choices(can_afford, weights=weights, k=1)[0]
        zombie_cost = config_data.get_zombie_config(zombie)["cost"]
        zombies_to_spawn.append(zombie)
        remaining_budget -= zombie_cost
      
      spawn_delay = 20 / len(zombies_to_spawn)
      if interval_config["type"] == "wave":
        spawn_delay /= 4
        if interval_config["wave_type"] == "huge":
          self.lanes.gui_controller.dispay_wave_message("A Huge wave of opps is approaching!")
          renpy.play(AUDIO_DIR + "metal-pipe.mp3", channel = "audio")
        else:
          self.lanes.gui_controller.dispay_wave_message("Final Wave!")
          renpy.play(AUDIO_DIR + "alarm.mp3", channel = "audio")
      random.shuffle(zombies_to_spawn)
      for i, zombie in enumerate(zombies_to_spawn):
        # Adding a small constant to prevent division by zero
        adjusted_spent_per_lane = [spent + 0.01 for spent in self.spent_per_lane]
        total_spent = sum(adjusted_spent_per_lane)

        # Using the inverse of spending to calculate probabilities
        probabilities = [1/(spent**2) for spent in adjusted_spent_per_lane]
        probabilities = [prob/sum(probabilities) for prob in probabilities]  # normalize probabilities
        self.displayed_probs = probabilities

        lane = random.choices(range(len(self.spent_per_lane)), weights=probabilities, k=1)[0]
        if zombie == "kanishk":
          lane = random.choices(self.lanes.lane_indexes_with_expensive_plants(), k=1)[0]
        self.spent_per_lane[lane] += config_data.get_zombie_config(zombie)["cost"]
        spawn_time = current_time + (i) * spawn_delay
        self.buffered_zombies.append(BufferedZombie(self, zombie, self.lanes.lanes[lane], spawn_time))

      
    def check_interval(self):
      interval = self.calculate_interval()
      if interval > self.interval:
        self.interval = interval
        self.prepare_zombie_interval()
        self.allow_fast_forward_timer = time.time()

    def check_fast_forward(self):
      if self.interval > 0 and self.fast_forward_seconds < 1000:
        if time.time() - self.allow_fast_forward_timer > 2:
          if not self.lanes.get_all_zombies():
            seconds_until_next_interval = 20 - (time.time() - self.start_time) % 20
            self.fast_forward_seconds += seconds_until_next_interval

    def update(self):
      for buffered_zombie in self.buffered_zombies:
        buffered_zombie.update()

      self.buffered_zombies = [buffered_zombie for buffered_zombie in self.buffered_zombies if not buffered_zombie.should_delete]
      self.check_interval()
      self.check_fast_forward()

    def render(self, render):
      # interval_text = Text((str(self.interval) + "-" + ",".join(str(item) for item in self.spent_per_lane)), size = 30)
      # render.place(interval_text, x = 1500, y = 100)

      progress_bar_y = 70
      progress_bar_x = 1500
      
      time_elapsed = time.time() - self.start_time + self.fast_forward_seconds
      text = Text(str(time_elapsed), size = 30)
      render.place(text, x = progress_bar_x, y = progress_bar_y+70)

      text = Text("Progress against the OPPS", size = 20)
      render.place(text, x = progress_bar_x, y = progress_bar_y-30)

      render.place(self.progress_bar_background, x = progress_bar_x, y = progress_bar_y)

      red_wave_ticks = Solid((255, 0, 0, 255), xsize=5, ysize=44)
      for wave_interval in self.wave_intervals:
        if wave_interval > self.interval:
          render.place(red_wave_ticks, x = ((400/self.max_interval) * wave_interval) + progress_bar_x, y = progress_bar_y)

      progress_bar_width = int((self.interval/self.max_interval) * 400)
      progress_bar = Solid((0, 255, 0, 255), xsize=progress_bar_width, ysize=40)
      render.place(progress_bar, x = progress_bar_x+2, y = progress_bar_y+2)

      difficulty_text = Text("Difficulty: " + str(difficulty_multiplier_to_str(self.difficulty_multiplier)), size = 30)
      render.place(difficulty_text, x = progress_bar_x, y = progress_bar_y+120)
      
      delta_time_to_fps = 1/delta_time
      fps_text = Text("FPS: " + str(int(delta_time_to_fps)), size = 30, color = (255, 255, 255))
      render.place(fps_text, x = progress_bar_x+200, y = 1000)
      return render


  class PvzGameDisplayable(renpy.Displayable):
    def __init__(self, level, loaded_plants, difficulty_multiplier):
      super(PvzGameDisplayable, self).__init__()
      level_config = load_json_from_file(path=JSON_DIR + "levels.json")
      zombie_config = load_json_from_file(path=JSON_DIR + "zombies.json")
      plant_config = load_json_from_file(path=JSON_DIR + "plants.json")
      projectile_config = load_json_from_file(path=JSON_DIR + "projectiles.json")
      explosion_config = load_json_from_file(path=JSON_DIR + "explosions.json")

      global config_data
      config_data = ConfigLoader(level_config, zombie_config, plant_config, projectile_config, explosion_config)

      self.has_ended_timer = None
      self.difficulty_multiplier = difficulty_multiplier
      particleSystem.clear()

      self.level_config = config_data.get_level_config(level)
      renpy.audio.music.play(AUDIO_DIR + self.level_config["music"], channel = "music", loop = True, fadein = 1.0, relative_volume = 0.6)

      self.mouseX = 0
      self.mouseY = 0
      self.plant_selected = None
      self.plant_seed_slot_selected = None
      self.is_targeting = False
      self.is_shovelling = False
      self.sun_amount = self.level_config["starting_sun"]

      self.final_outcome = None

      self.last_time = time.time()

      loaded_plants.extend(self.get_protected_plant_names())
      self.loaded_plants = list(set(loaded_plants))

      all_images.load_zombies(self.level_config["zombies"])
      all_images.load_plants(self.loaded_plants)
      all_images.load_explosions()
      all_images.load_gui()

      self.environment = EnvironmentBuilder(self.level_config, self)
      self.lanes = self.environment.gen_lanes()
      self.explosion_controller = ExplosionController(self.lanes)

      self.gui_controller = GUIController(self.loaded_plants, self.level_config)
      self.gui_controller.lanes = self.lanes
      self.lanes.set_gui_controller(self.gui_controller)
      self.gui_controller.explosion_controller = self.explosion_controller

      self.zombie_spawner = ZombieSpawner(self.level_config, self.lanes,self.gui_controller, self.difficulty_multiplier)

      self.has_protected_plant_died = False
      self.handle_protected_plants()

    def handle_protected_plants(self):
      # check if protected plants in level
      if "protect" in self.level_config:
        protected_plants = self.level_config["protect"]
        for protected_plant in protected_plants:
          plant_name = protected_plant[0]
          lane_id = protected_plant[2]
          tile_id = protected_plant[1]
          tile = self.lanes.lane_id_and_tile_id_to_tile(lane_id, tile_id)
          plant = self.lanes.add_plant_tile(tile, plant_name, is_protected = True)
          plant.game = self

    def get_protected_plant_names(self):
      protected_plants = []
      if "protect" in self.level_config:
        protected_plants = self.level_config["protect"]
      return [protected_plant[0] for protected_plant in protected_plants]
        
    def visit(self):
      return self.environment.visit()

    def make_state(self):
      return {
        "mouseX": self.mouseX,
        "mouseY": self.mouseY,
        "plant_selected": self.plant_selected,
        "sun_amount": self.sun_amount,
        "plant_seed_slot_selected": self.plant_seed_slot_selected,
        "is_targeting": self.is_targeting,
        "is_shovelling": self.is_shovelling,
      }

    def alter_state(self, state):
      self.mouseX = state["mouseX"]
      self.mouseY = state["mouseY"]
      self.plant_selected = state["plant_selected"]
      self.sun_amount = state["sun_amount"]
      self.plant_seed_slot_selected = state["plant_seed_slot_selected"]
      self.is_targeting = state["is_targeting"]
      self.is_shovelling = state["is_shovelling"]

    def process_click(self):
      current_state = self.make_state()
      current_state = self.gui_controller.process_click(current_state)

      if self.gui_controller.is_targeting:
        return

      if self.is_shovelling:
        tile = self.lanes.pos_to_tile(self.mouseX, self.mouseY)
        if tile:
          if tile.is_planted:
            if tile.get_plant_on_tile().is_protected:
              self.gui_controller.display_notification("Can't remove protected plants!")
            else:
              tile.is_planted = False
              tile.get_plant_on_tile().is_dead = True
              tile.plant_on_tile = None
          else:
            self.gui_controller.display_notification("Nothing to remove!")
        current_state["is_shovelling"] = False
        self.alter_state(current_state)
        return

      if not self.gui_controller.is_targeting and not self.gui_controller.targeted_location_x:
        tile = self.lanes.pos_to_tile(self.mouseX, self.mouseY)
        if tile:
          plant_on_tile = tile.get_plant_on_tile()
          if plant_on_tile:
            if plant_on_tile.plant_type == "cobcannon":
              current_state["plant_seed_slot_selected"] = None
              current_state["plant_selected"] = None
              self.alter_state(current_state)
              if plant_on_tile.is_ready_to_fire:
                plant_on_tile.prepare_missile()
                self.gui_controller.is_targeting = True
              else:
                self.gui_controller.display_notification("He isn't ready yet!")
              return

      if self.plant_selected is not None and self.plant_seed_slot_selected is not None:
        tile = self.lanes.pos_to_tile(self.mouseX, self.mouseY)
        if tile:
          if current_state["sun_amount"] >= self.plant_seed_slot_selected.plant_config["cost"] and self.plant_seed_slot_selected.is_recharge_ready:
            if not tile.is_planted:
              tile.is_planted = True
              self.lanes.add_plant_tile(tile, self.plant_selected)
              self.plant_seed_slot_selected.reset_recharge_timer()
              current_state["sun_amount"] -= self.plant_seed_slot_selected.plant_config["cost"]
            else:
              self.gui_controller.display_notification("Can't place him there!")
        current_state["plant_seed_slot_selected"] = None
        current_state["plant_selected"] = None

      self.alter_state(current_state)

    def check_end(self):
      if self.has_protected_plant_died:
        renpy.play(AUDIO_DIR + "moan.mp3", channel = "audio")
        self.has_ended_timer = time.time()
        self.gui_controller.dispay_wave_message("You lost!")
        return "lost"

      all_zombies = self.lanes.get_all_zombies()
      for zombie in all_zombies:
        if zombie.x_location < 150:
          self.has_ended_timer = time.time()
          self.gui_controller.dispay_wave_message("You lost!")
          return "lost"

      if self.zombie_spawner.has_finished:
        if len(all_zombies) == 0:
          self.has_ended_timer = time.time()
          self.gui_controller.dispay_wave_message("You won!")
          return "won"

    def render(self, width, height, st, at):
      global delta_time
      current_time = time.time()
      delta_time = (current_time - self.last_time)
      self.last_time = current_time

      current_state = self.make_state()
      self.environment.update(current_state)
      self.lanes.update()
      self.explosion_controller.update()
      self.zombie_spawner.update()
      new_state = self.gui_controller.update(state=current_state)
      if not self.final_outcome:
        self.final_outcome = self.check_end()
      self.alter_state(new_state)

      r = renpy.Render(width, height)
      # r = self.environment.render(r)
      r = self.lanes.render(r)
      r = self.explosion_controller.render(r)

      if self.has_ended_timer:
        opacity = 255 * ((time.time() - self.has_ended_timer) / 3)
        white_screen_overlay = Solid((255, 255, 255, opacity), xsize=1950, ysize=1080)
        r.place(white_screen_overlay, 0, 0)
        if time.time() - self.has_ended_timer > 2:
          text = Text("Move the mouse to continue", size=50, color=(0, 0, 0))
          r.place(text, x = self.mouseX, y = self.mouseY)

      r = self.gui_controller.render(r, new_state)
      r = self.zombie_spawner.render(r)

      renpy.redraw(self, 0)
      return r

    def event(self, ev, x, y, st):
      import pygame
      self.mouseX = x
      self.mouseY = y

      if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
        self.process_click()

      if self.has_ended_timer and time.time() - self.has_ended_timer > 3:
        return self.final_outcome

      # send_to_file("logz.txt", str(self.mouseX) + " " + str(self.mouseY) + "\n")
    
screen pvz_game_menu():
  modal True
  $ game = PvzGameDisplayable(current_level, chosen_plants, current_difficulty)
  add game

label test_game_entry_label:
  window hide
  $ quick_menu = False
  $ _game_menu_screen = None
  $ level_outcome = renpy.call_screen(_screen_name='pvz_game_menu')
  $ quick_menu = True
  return