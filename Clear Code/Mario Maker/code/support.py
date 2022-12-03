import pygame
from os import walk # Access to the file system


def import_folder(path):
    # Any picture inside of path will be imported and placed in surface_list
    surface_list = []
    # Extract only the image files
    for folder_name, sub_folders, image_files in walk(path):
        for image_name in image_files:
            # Find the full path of the image
            full_path = path + "/" + image_name
            # Use the full path to load an image
            image_surface = pygame.image.load(full_path)
            # Add image surface to the surface list
            surface_list.append(image_surface)

    return surface_list
        
# Used for the land tiles
def import_folder_dict(path):
    surface_dict = {}

    for folder_name, sub_folders, image_files in walk(path):
        for image_name in image_files:
            full_path = path + "/" + image_name
            image_surface = pygame.image.load(full_path)
            # Create a new key: value pair
            surface_dict[image_name.split(".")[0]] = image_surface # Get rid of the .png with .split
            
    return surface_dict
