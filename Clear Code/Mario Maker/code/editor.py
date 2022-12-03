import pygame, sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from settings import *
from menu import Menu

class Editor: 
    def __init__(self, land_tiles):
        # Main set-up
        self.display_surface = pygame.display.get_surface()
        self.canvas_data = {}

        # Imports
        self.land_tiles = land_tiles # Import graphics

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
        self.last_selected_cell = None

        # Menu
        self.menu = Menu()
    # ------------------------------------------------------------------------------------------------------------------------
    # SUPPORT
    def get_current_cell(self):
        distance_to_origin = vector(mouse_pos()) - self.origin # vector(x = mouse_pos()[0] - self.origin.x , y = mouse_pos()[1] - self.origin.y)
        #print(distance_to_origin, self.origin)

        # In the case that the column not negative 
        if distance_to_origin.x > 0:
            # Find the column cell that was clicked
            column = int(distance_to_origin.x / TILE_SIZE)
        # In the case that the column is negative
        else:
            # For more info go to 1:54:00 in the video
            column = int(distance_to_origin.x / TILE_SIZE) - 1

        # Do the same for the rows
        if distance_to_origin.y > 0:
            row = int(distance_to_origin.y / TILE_SIZE)
        else: 
            row = int(distance_to_origin.y / TILE_SIZE) - 1


        return column, row
    
    def check_neighbours(self, cell_pos):

        # Create a local cluster (the cells around the cell we are looking at)
        cluster_size = 3
        # List comprehension to make a list with the local cluster
        local_cluster = [(cell_pos[0] + col - int(cluster_size / 2), cell_pos[1] + row - int(cluster_size / 2)) 
        for col in range(cluster_size) 
        for row in range(cluster_size)]

        # Check neighbours of the cell
        for cell in local_cluster:
            # Check if any of the cells are an existing tile on the canvas
            if cell in self.canvas_data:
                # Set terrain neighbours to an empty list (to avoid adding pointless data)
                self.canvas_data[cell].terrain_neighbours = []

                # Check neighbours
                for name, side in NEIGHBOR_DIRECTIONS.items():
                    neighbour_cell = (cell[0] + side[0], cell[1] + side[1]) # Check all possibilities using neighbour directions
                    # If the neighbour cell is an existing tile
                    if neighbour_cell in self.canvas_data:
                        # If it is a terrain tile
                        if self.canvas_data[neighbour_cell].has_terrain: 
                            self.canvas_data[cell].terrain_neighbours.append(name)
        
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
            self.canvas_add()

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

    # Triggered when clicking on the canvas
    def canvas_add(self):
        if mouse_buttons()[0] and not self.menu.rect.collidepoint(mouse_pos()): # If we are left-clicking and not clicking on the menu
            current_cell = self.get_current_cell() 

            # If we have changed a cell that is different from the last cell (This additional check is to improve performance)
            if current_cell != self.last_selected_cell:
                # If the cell already has a canvas tile
                if current_cell in self.canvas_data:
                    self.canvas_data[current_cell].add_id(self.selection_index) # This is basically updating an existing tile
                else:
                    # Create a canvas tile, passing the index into the tile (which will determine what tile it is)
                    self.canvas_data[current_cell] = CanvasTile(self.selection_index) # This is creating a new tile (as there isn't an existing tile there)

                # Check the neighbours of the current cell
                self.check_neighbours(current_cell)
                # Set the last selected cell as the current cell
                self.last_selected_cell = current_cell


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
    
    def draw_level(self):
        # Iterate through the cell position and the tile index in the canvas items
        for cell_pos, tile in self.canvas_data.items():
            # Start from the origin point, not the start of the screen
            pos = self.origin + vector(cell_pos) * TILE_SIZE # Cell pos is converted to a vector because you cannot multiply a tuple by something

            # Terrain
            if tile.has_terrain:
                # Making a string following the graphics names e.g. ABCDE
                terrain_string = "".join(tile.terrain_neighbours)
                # If the terrain string does not exist in the imported graphics, use the generic tile "X"
                terrain_style = terrain_string if terrain_string in self.land_tiles else "X"
                self.display_surface.blit(self.land_tiles[terrain_style], pos)

            # Water
            if tile.has_water:
                test_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                test_surface.fill("blue")
                self.display_surface.blit(test_surface, pos)

            # Coins
            if tile.coin:
                test_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                test_surface.fill("yellow")
                self.display_surface.blit(test_surface, pos)

            # Enemies
            if tile.enemy:
                test_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                test_surface.fill("red")
                self.display_surface.blit(test_surface, pos)


    # ------------------------------------------------------------------------------------------------------------------------
    # Updating
    def run(self, dt):
        self.display_surface.fill("white")
        self.draw_level()
        self.draw_tile_lines()
        self.event_loop()
        pygame.draw.circle(self.display_surface, "red", self.origin, 10)
        self.menu.display(index = self.selection_index)



class CanvasTile:
    def __init__(self, tile_id):
        # Terrain
        self.has_terrain = False
        self.terrain_neighbours = []

        # Water 
        self.has_water = False
        self.water_on_top = False

        # Coin
        self.coin = None # Only one kind of coin on the same tile. The value can be 4, 5 or 6

        # Enemy 
        self.enemy = None # Same logic as the coin (only one type of enemy per tile)

        # Objects
        self.objects = []

        self.add_id(tile_id)


    def add_id(self, tile_id):
        # Create a new dictionary only with the index and the value inside of the values in "style" (Because it is a dictionary inside of a dictionary)
        options = {key:value["style"] for key, value in EDITOR_DATA.items()}
        # Match case
        match options[tile_id]: 
            case "terrain": self.has_terrain = True
            case "water": self.has_water = True
            case "coin": self.coin = tile_id # Change id of the coin (because there are different variants of coins)
            case "enemy": self.enemy = tile_id # Change id of the enemies (because there are different variants of enemies)

