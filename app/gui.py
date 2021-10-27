"""
Module containing GUI elements and other settings
"""

# Modules
import pygame

from pygame_gui import UIManager
from pygame_gui.elements import UILabel, UIButton, UIHorizontalSlider

from app.config import *


class GUI:
    def __init__(self):
        # GUI manager
        self.manager = UIManager(WINDOW_SIZE, 'data/themes/theme.json')
        self.gui_rect_color = pygame.Color('#0d1419')  # Color
        self.gui_rects = []  # Array with all rects

        self.info_block = {
            'elements': {

                'FPS_counter': UILabel(relative_rect=pygame.Rect(10, 10, 200, 40),
                                       text='FPS: None', manager=self.manager, object_id='#fps_counter'),
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
                # Planet
                'title': UILabel(relative_rect=pygame.Rect(10, 180, 200, 40),
                                 text='Settings', manager=self.manager, object_id='#title'),
                'planet_title': UILabel(relative_rect=pygame.Rect(10, 222, 200, 30),
                                        text='Planet', manager=self.manager, object_id="#subtitle"),
                'planet_mass_label': UILabel(relative_rect=pygame.Rect(10, 254, 50, 30),
                                             text='Mass:', manager=self.manager, object_id='#settings_label'),
                'planet_mass_slider': UIHorizontalSlider(relative_rect=pygame.Rect(65, 260, 145, 20),
                                                         start_value=150,
                                                         value_range=(50, 450),
                                                         manager=self.manager),
                'planet_color_button': UIButton(relative_rect=pygame.Rect(10, 290, 160, 30),
                                                text='Choose color',
                                                manager=self.manager),
                'planet_color_surface': UILabel(relative_rect=pygame.Rect(177, 290, 30, 30),
                                                text='', manager=self.manager),

                # Star
                'star_title': UILabel(relative_rect=pygame.Rect(10, 332, 200, 30),
                                      text='Star', manager=self.manager, object_id="#subtitle"),
                'star_mass_label': UILabel(relative_rect=pygame.Rect(10, 365, 50, 30),
                                           text='Mass:', manager=self.manager, object_id='#settings_label'),
                'star_mass_slider': UIHorizontalSlider(relative_rect=pygame.Rect(65, 370, 145, 20),
                                                       start_value=20000,
                                                       value_range=(10000, 30000),
                                                       manager=self.manager),
                'star_color_button': UIButton(relative_rect=pygame.Rect(10, 400, 160, 30),
                                              text='Choose color',
                                              manager=self.manager),
                'star_color_surface': UILabel(relative_rect=pygame.Rect(177, 400, 30, 30),
                                              text='', manager=self.manager),

                # General
                'general_title': UILabel(relative_rect=pygame.Rect(10, 447, 200, 30),
                                         text='General', manager=self.manager, object_id="#subtitle"),
                'grid_label': UILabel(relative_rect=pygame.Rect(10, 482.5, 50, 20),
                                      text='Grid: ', manager=self.manager, object_id='#settings_label'),
                'grid_button': UIButton(relative_rect=pygame.Rect(60, 480, 25, 25),
                                        text='',
                                        manager=self.manager),
            }
        }

    # GUI rect
    def get_gui_rect(self, gui_dictionary: dict, padding: int) -> pygame.Rect:
        """
        Method that returns Rect of block of GUI.
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

        self.gui_rects.append(gui_rect)
        return gui_rect
