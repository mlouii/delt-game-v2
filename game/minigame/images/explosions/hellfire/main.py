import os

dir_path = r'C:\Users\mark_\OneDrive\Documents\My Games\renpy-8.0.3-sdk\deltGamev2\game\minigame\images\explosions'

for filename in os.listdir(dir_path):
    if filename.endswith('_delay-0.04s.png'): # change this to match the file extension of your images
        new_filename = filename[:-16] + '.png' # remove the "_delay-0.04s" suffix and add the file extension back
        os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_filename))
