import pygame
from settings import *
from pygame.image import load

class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_data() # Import data of tiles, needs to be before the buttons, because we need the data to make the buttons properly
        self.create_buttons() # Call the method to create buttons

    # Importing items
    def create_data(self):
        self.menu_surfaces = {}
        # Iterate through each key:value pair in the editor data dictionary
        for key, value in EDITOR_DATA.items():
            # If the value inside of the value "menu" has a value i.e not "None"
            if value["menu"]:
                # If this value isn't already in the self.menu_surfaces dictionary
                if not value["menu"] in self.menu_surfaces:
                    self.menu_surfaces[value["menu"]] = [(key, load(value["menu_surf"]))]
                # In case that they both have "terrain" for example as the value["menu"], the "water" surface would be ignored without this second condition
                else:
                    self.menu_surfaces[value["menu"]].append((key, load(value["menu_surf"])))

    # Change self.index to change items
    def click(self, mouse_pos, mouse_button):
        for sprite in self.buttons:
            if sprite.rect.collidepoint(mouse_pos):
                # Check for different mouse clicks
                if mouse_button[1]: # Middle mouse click
                    sprite.main_active = not sprite.main_active if sprite.items["alt"] else True # Turn main_active on/off only if the button has alternative items
                if mouse_button[2]: # Right click
                    sprite.switch()

                return sprite.get_id()

    def create_buttons(self):
        # Menu area
        size = 180
        margin = 6
        topleft = (WINDOW_WIDTH - size - margin, WINDOW_HEIGHT - size - margin)
        self.rect = pygame.Rect(topleft, (size, size))

        # Button area
        generic_button_rect = pygame.Rect(self.rect.topleft, (self.rect.width / 2, self.rect.height / 2))
        button_margin = 5
        self.tile_button_rect = generic_button_rect.copy().inflate(-button_margin, -button_margin) # Inflate increases or decreases the size of the rectangle, parameters are x and y
        self.coin_button_rect = generic_button_rect.move(self.rect.width / 2, 0).inflate(-button_margin, -button_margin)  # The move method returns a new rect object

        self.enemy_button_rect = generic_button_rect.copy().move(0, self.rect.height / 2).inflate(-button_margin, -button_margin)
        self.palm_button_rect = generic_button_rect.move(self.rect.width / 2, self.rect.height / 2).inflate(-button_margin, -button_margin)  

        # Create the buttons
        self.buttons = pygame.sprite.Group()
        Button(rect = self.tile_button_rect, group = self.buttons, items = self.menu_surfaces["terrain"]) # First button
        Button(rect = self.coin_button_rect, group = self.buttons, items = self.menu_surfaces["coin"])
        Button(rect = self.enemy_button_rect, group = self.buttons, items = self.menu_surfaces["enemy"])
        Button(rect = self.palm_button_rect, group = self.buttons, items = self.menu_surfaces["palm fg"],items_alt = self.menu_surfaces["palm bg"])

    # Highlights the currently selected button
    def highlight_indicator(self, index):
        if EDITOR_DATA[index]["menu"] == "terrain":
            pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOUR, self.tile_button_rect.inflate(4, 4), 5, 4) # Last parameter is border rounding
        if EDITOR_DATA[index]["menu"] == "coin":
            pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOUR, self.coin_button_rect.inflate(4, 4), 5, 4) # Last parameter is border rounding
        if EDITOR_DATA[index]["menu"] == "enemy":
            pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOUR, self.enemy_button_rect.inflate(4, 4), 5, 4) # Last parameter is border rounding
        if EDITOR_DATA[index]["menu"] in ("palm bg", "palm fg"): # Check if the value selected is either in palm bg or palm fg
            pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOUR, self.palm_button_rect.inflate(4, 4), 5, 4) # Last parameter is border rounding      

    def display(self, index):
        # pygame.draw.rect(self.display_surface, "red", self.rect)
        # pygame.draw.rect(self.display_surface, "green", self.tile_button_rect)
        # pygame.draw.rect(self.display_surface, "blue", self.coin_button_rect)
        # pygame.draw.rect(self.display_surface, "yellow", self.enemy_button_rect)
        # pygame.draw.rect(self.display_surface, "brown", self.palm_button_rect)

        self.buttons.update()
        self.buttons.draw(self.display_surface)
        self.highlight_indicator(index)
        

class Button(pygame.sprite.Sprite): 
    # Items = foreground palm trees items_alt = background palm trees
    def __init__(self, rect, group, items, items_alt = None): # group = the group that this button sprite is part off
        super().__init__(group) 
        self.image = pygame.Surface(rect.size) # Will be a plain surface with the size of the button rectangle(created above)
        self.rect = rect

        # Items
        self.items = {"main": items, "alt": items_alt}
        self.index = 0 # Determines the item we are looking at
        self.main_active = True # Determines whether we are looking at the main items or alternative items

    # Get the id (the self.index)
    def get_id(self):
        return self.items["main" if self.main_active else "alt"][self.index][0] # If self.main is active, we return items or items_alt
    
    # Switch index 
    def switch(self):
        self.index += 1
        # Limit the index
        """ Set self.index to 0 if the self.index exceeds the number of items inside main or alt. If it hasn't exceeded, don't make any changes to self.index.
        This means that if terrain had 3 items. After the 3rd item, it will loop back to the 1st item
        """
        self.index = 0 if self.index >= len(self.items["main" if self.main_active else "alt"]) else self.index 

    # Display what we have inside of the sprite
    def update(self):
        # Fill the background of the button with this colour
        self.image.fill(BUTTON_BG_COLOUR)
        surface = self.items["main" if self.main_active else "alt"][self.index][1] # The graphic of the surface tuple
        #print(surface)
        rect = surface.get_rect(center = (self.rect.width / 2, self.rect.height / 2))
        # Draw the image icon onto the button box
        self.image.blit(surface, rect)

