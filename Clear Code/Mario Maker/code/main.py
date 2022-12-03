import pygame, sys 
from settings import *
from editor import Editor
from pygame.image import load

class Main:
    def __init__(self):
        # Pygame set-up
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # Editor
        self.editor = Editor()

        # Cursor
        cursor_image = load("graphics/cursors/mouse.png").convert_alpha()

        # Creating a cursor object
        cursor = pygame.cursors.Cursor((0,0), cursor_image) # (0,0) is the part of the image which will be where the click is initiated from
        pygame.mouse.set_cursor(cursor)


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