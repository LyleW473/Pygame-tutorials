import pygame, sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from settings import *
from menu import Menu

class Editor: 
    def __init__(self):
        # Main set-up
        self.display_surface = pygame.display.get_surface()

        # Navigation 
        self.origin = vector() # Origin is a vector
        self.pan_active = False # Used when panning around screen
        self.pan_offset = vector() # The distance/offset between the mouse pos and the origin

        # Support lines
        self.support_line_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surface.set_colorkey("green") # Removes any colour with the colour green
        self.support_line_surface.set_alpha(30) # Set the transparency of the support line surface

        # Selection
        self.selection_index = 2

        # Menu
        self.menu = Menu()

    # ------------------------------------------------------------------------------------------------------------------------
    # INPUT
    def event_loop(self):
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.pan_input(event)
            self.selection_hotkeys(event)
            self.menu_click(event)

    # Used to move the origin 
    def pan_input(self, event): 
        
        # Middle mouse button pressed / released
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            # Calculate the offset between the mouse position and the origin
            self.pan_offset = vector(mouse_pos()) - self.origin

        # Middle mouse button is released
        if not mouse_buttons()[1]:
            self.pan_active = False

        # Mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            """ Event.y refers to the mousewheel moving up and down. Up = 1, Down = -1
            - Move the origin's x co-ordinate based on whether the mousewheel moves up or down
            - It is decrementing because when we are scrolling right, all elements would move left"""

            # If the Left CTRL button is being pressed (and the mouse wheel is being moved), move it up or down based on the action
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * 50
            else:
                self.origin.x -= event.y * 50 

        # Panning update
        if self.pan_active:
            # Move the origin by the distance that the mouse position has moved
            self.origin = vector(mouse_pos()) - self.pan_offset
    
    def selection_hotkeys(self, event):
        # Check for if a key is being pressed (This is checking if a key is being pressed, not held)
        if event.type == pygame.KEYDOWN:
            # Check if the right arrow key has been pressed
            if event.key == pygame.K_RIGHT: # and self.selection_index < 18: # Limit the highest the index can be to 18
                self.selection_index += 1
            # Check if the left arrow key has been pressed
            if event.key == pygame.K_LEFT: # and self.selection_index > 2: # Limit the lowest the index can be to 2
                self.selection_index -= 1    
            # Limit the highest and lowest the index can be
            self.selection_index = max(2, min(self.selection_index, 18)) 


    def menu_click(self, event):
        # If the button has been clicked
        if event.type == pygame.MOUSEBUTTONDOWN and self.menu.rect.collidepoint(mouse_pos()):
            # Call the click method inside menus, which will check if the button is colliding with the mouse position
            self.selection_index = self.menu.click(mouse_pos(), mouse_buttons())
    # ------------------------------------------------------------------------------------------------------------------------
    # Drawing
    def draw_tile_lines(self):
        columns = WINDOW_WIDTH // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE

        """ 
        The main idea is that we create a new point to start drawing columns from, which is before the origin point. That way, we will always have tile lines on the screen.
        This new point is created from finding the difference between the column before the origin point and where the origin point is
        origin_offset.x = vector(x = 100 - int(100 / 64) * 64) ---> 100 - 64 = 36
        origin_offset.x = vector(x = 128 - int(128 / 64) * 64) ---> 128 - 128 = 0

        """ 
        origin_offset = vector(x = self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE , y = self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE)
    
        pygame.draw.circle(self.display_surface, "blue", (origin_offset.x, origin_offset.y), 10) #un-comment this to visualise it

        # Used to make the lines transparent
        self.support_line_surface.fill("green")

        # Draw a line for each column in the amount of columns
        for column in range(columns + 1): # The plus 1 is so that an extra column is being drawn at the end of the screen when we scroll right
            # Draw the columns from the offset x position
            x = origin_offset.x + column *  TILE_SIZE
            pygame.draw.line(self.support_line_surface, LINE_COLOUR, (x, 0), (x, WINDOW_HEIGHT)) # The x co-ordinate should be the same for columns

        # Do the same for the rows
        for row in range(rows + 1):
            y = origin_offset.y + row * TILE_SIZE
            pygame.draw.line(self.support_line_surface, LINE_COLOUR, (0, y), (WINDOW_WIDTH, y)) 

        # Draw the transparent surface onto the main surface
        self.display_surface.blit(self.support_line_surface, (0, 0))


    def run(self, dt):
        self.display_surface.fill("blue")
        self.draw_tile_lines()
        self.event_loop()
        pygame.draw.circle(self.display_surface, "red", self.origin, 10)
        self.menu.display(index = self.selection_index)
