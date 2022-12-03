import pygame, sys 
from settings import *
from editor import Editor
from pygame.image import load
from support import *

class Main:
    def __init__(self):
        # Pygame set-up
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.imports()

        # Editor
        self.editor = Editor(self.land_tiles) # Pass in the land tiles so that the images can be operated on inside the editor file

        # Cursor
        cursor_image = load("graphics/cursors/mouse.png").convert_alpha()

        # Creating a cursor object
        cursor = pygame.cursors.Cursor((0,0), cursor_image) # (0,0) is the part of the image which will be where the click is initiated from
        pygame.mouse.set_cursor(cursor)
        
    # Importing data (this is in main because there are alot of files which the level and editor will both need later on)
    def imports(self):
        self.land_tiles = import_folder_dict("graphics/terrain/land")


    def run(self):
        while True:
            # Delta time, used to keep our framerate independent
            dt = self.clock.tick() / 1000 

            self.editor.run(dt)
            
            pygame.display.update()

# If we are in the main file
if __name__ == "__main__":
    # Create an instance of the Main class
    main = Main()
    # Call the run method
    main.run()