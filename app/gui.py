"""
Module containing GUI elements and other settings
"""

# Modules
import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UILabel, UIButton, UIHorizontalSlider
from pygame_gui.windows import UIColourPickerDialog

from config import *


class GUIManager:
    def __init__(self):
        # GUI manager
        self.manager = UIManager(WINDOW_SIZE)
        self.gui_rect_color = pygame.Color('#0d1419')  # Color

        self.info_block = {
            'elements': {

                'FPS_counter': UILabel(relative_rect=pygame.Rect(10, 10, 200, 40),
                                       text='FPS: None', manager=self.manager),
                'velocity_x_label': UILabel(relative_rect=pygame.Rect(10, 55, 200, 20),
                                            text='X velocity: None', manager=self.manager),
                'velocity_y_label': UILabel(relative_rect=pygame.Rect(10, 80, 200, 20),
                                            text='Y velocity: None', manager=self.manager),
                'G_label': UILabel(relative_rect=pygame.Rect(10, 105, 200, 20),
                                   text=f'G = {G}', manager=self.manager),
                'K_label': UILabel(relative_rect=pygame.Rect(10, 130, 200, 20),
                                   text=f'Distance coef = {K_value}', manager=self.manager),
            }
        }

        self.settings_block = {
            'elements': {

                'title': UILabel(relative_rect=pygame.Rect(10, 180, 200, 40),
                                 text='Settings', manager=self.manager),
                'planet_title': UILabel(relative_rect=pygame.Rect(10, 225, 200, 30),
                                        text='Planet:', manager=self.manager),
                'mass_label': UILabel(relative_rect=pygame.Rect(10, 254, 50, 30),
                                      text='Mass:', manager=self.manager),
                'mass_slider': UIHorizontalSlider(relative_rect=pygame.Rect(65, 260, 145, 20),
                                                  start_value=150,
                                                  value_range=(50, 450),
                                                  manager=self.manager),
                'planet_color_button': UIButton(relative_rect=pygame.Rect(10, 295, 200, 30),
                                                text='Choose color',
                                                manager=self.manager)

            },

            'windows': {

                'planet_color_picker': UIColourPickerDialog(pygame.Rect(10, 295, 200, 200),
                                                            window_title='Planet color ...',
                                                            initial_colour=FOREST_GREEN,
                                                            manager=self.manager)
            }
        }

    # GUI rect
    @staticmethod
    def get_gui_rect(gui_dictionary: dict, padding: int) -> pygame.Rect:
        """
        Static method that returns Rect of block of GUI.
        :param gui_dictionary: Dictionary with GUI elements
        :param padding: Integer value of inner padding
        :return: pygame.Rect
        """

        elements_array = gui_dictionary['elements'].values()  # Array of GUI elements

        # Array of rectangles of  GUI
        rect_array = [element.rect for element in elements_array]
        # GUI rect with biggest (Y + height) value
        max_y_rect = sorted(rect_array, key=lambda x: x[1] + x[3])[-1]
        # GUI rect with biggest (X + width) value
        max_x_rect = sorted(rect_array, key=lambda x: x[0] + x[2])[-1]

        rect_x = min([element.rect.x for element in elements_array])  # Top left X
        rect_y = min([element.rect.y for element in elements_array])  # Top left Y
        rect_width = max_x_rect.x - rect_x + max_x_rect.width  # Width
        rect_height = max_y_rect.y - rect_y + max_y_rect.height  # Height

        # GUI Rect
        gui_rect = pygame.Rect(rect_x - padding,  # X
                               rect_y - padding,  # Y
                               rect_width + 2 * padding,  # Width
                               rect_height + 2 * padding  # Height
                               )
        return gui_rect
