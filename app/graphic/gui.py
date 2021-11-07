"""
Module containing GUI elements and other settings
"""

# Modules
import os

import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UILabel, UIButton, UIHorizontalSlider

from app.config import Config


class GUI:
    def __init__(self):
        # GUI manager
        self.theme_path = os.path.join("data", "themes", "theme.json")  # Path to theme
        self.manager = UIManager(Config.WINDOW_SIZE, self.theme_path)  # UI manager
        self.gui_rect_color = Config.GUI_BG_COLOR  # BG color
        self.gui_rects = []  # Array with all BG rects

        self.info = {
            'elements': {

                'FPS_counter': UILabel(relative_rect=pygame.Rect(10, 10, 200, 40), text='FPS: None',
                                       manager=self.manager, object_id='#fps_counter'),
                'velocity_x_label': UILabel(relative_rect=pygame.Rect(10, 55, 200, 20), text='X velocity: None',
                                            manager=self.manager),
                'velocity_y_label': UILabel(relative_rect=pygame.Rect(10, 80, 200, 20), text='Y velocity: None',
                                            manager=self.manager),
                'G_label': UILabel(relative_rect=pygame.Rect(10, 105, 200, 20), text=f'G = {Config.G}',
                                   manager=self.manager),
                'K_label': UILabel(relative_rect=pygame.Rect(10, 130, 200, 20),
                                   text=f'Distance = {100 * Config.K}%',
                                   manager=self.manager),
            }
        }

        self.settings = {
            'elements': {
                # Planet
                'title': UILabel(relative_rect=pygame.Rect(10, 180, 200, 40), text='Settings',
                                 manager=self.manager, object_id='#title'),
                'planet_title': UILabel(relative_rect=pygame.Rect(10, 222, 200, 30), text='Planet',
                                        manager=self.manager, object_id="#subtitle"),
                'planet_mass_label': UILabel(relative_rect=pygame.Rect(10, 254, 50, 30), text='Mass:',
                                             manager=self.manager, object_id='#settings_label'),
                'planet_mass_slider': UIHorizontalSlider(relative_rect=pygame.Rect(65, 260, 145, 20),
                                                         start_value=Config.PLANET_DEFAULT_MASS,
                                                         value_range=(Config.PLANET_MIN_MASS, Config.PLANET_MAX_MASS),
                                                         manager=self.manager),
                'planet_color_button': UIButton(relative_rect=pygame.Rect(10, 290, 160, 30), text='Choose color',
                                                manager=self.manager),
                'planet_color_surface': UILabel(relative_rect=pygame.Rect(177, 290, 30, 30), text='',
                                                manager=self.manager, object_id='#color_surface'),

                # Star
                'star_title': UILabel(relative_rect=pygame.Rect(10, 332, 200, 30), text='Star',
                                      manager=self.manager, object_id="#subtitle"),
                'star_mass_label': UILabel(relative_rect=pygame.Rect(10, 365, 50, 30), text='Mass:',
                                           manager=self.manager, object_id='#settings_label'),
                'star_mass_slider': UIHorizontalSlider(relative_rect=pygame.Rect(65, 370, 145, 20),
                                                       start_value=Config.STAR_DEFAULT_MASS,
                                                       value_range=(Config.STAR_MIN_MASS, Config.STAR_MAX_MASS),
                                                       manager=self.manager),
                'star_color_button': UIButton(relative_rect=pygame.Rect(10, 400, 160, 30), text='Choose color',
                                              manager=self.manager),
                'star_color_surface': UILabel(relative_rect=pygame.Rect(177, 400, 30, 30), text='',
                                              manager=self.manager, object_id='#color_surface'),

                # General
                'general_title': UILabel(relative_rect=pygame.Rect(10, 447, 200, 30), text='General',
                                         manager=self.manager, object_id="#subtitle"),
                'glow_label': UILabel(relative_rect=pygame.Rect(10, 485.5, 50, 20), text='Glow: ',
                                      manager=self.manager, object_id='#settings_label'),
                'glow_button': UIButton(relative_rect=pygame.Rect(60, 483, 25, 25), text='',
                                        tool_tip_text='Turn on/off glow', manager=self.manager,
                                        object_id='#radio_button'),
                'grid_label': UILabel(relative_rect=pygame.Rect(100, 485.5, 50, 20), text='Grid: ',
                                      manager=self.manager, object_id='#settings_label'),
                'grid_button': UIButton(relative_rect=pygame.Rect(150, 483, 25, 25), text='',
                                        tool_tip_text='Turn on/off grid', manager=self.manager,
                                        object_id='#radio_button'),
                'trace_label': UILabel(relative_rect=pygame.Rect(10, 513.5, 50, 20), text='Trace: ',
                                       manager=self.manager, object_id='#settings_label'),
                'trace_button': UIButton(relative_rect=pygame.Rect(60, 511, 25, 25), text='',
                                         tool_tip_text='Turn on/off traces', manager=self.manager,
                                         object_id='#radio_button'),

                #  Simulation control
                'pause_button': UIButton(relative_rect=pygame.Rect(40, 550, 35, 35), text='',
                                         tool_tip_text='Pause', manager=self.manager, object_id='#pause_button'),
                'play_button': UIButton(relative_rect=pygame.Rect(75, 550, 35, 35), text='',
                                        tool_tip_text='Play', manager=self.manager, object_id='#play_button'),
                'faster_x2_button': UIButton(relative_rect=pygame.Rect(110, 550, 35, 35), text='',
                                             tool_tip_text='Speed up 2X', manager=self.manager,
                                             object_id='#faster_x2_button'),
                'faster_x3_button': UIButton(relative_rect=pygame.Rect(145, 550, 35, 35), text='',
                                             tool_tip_text='Speed up 3X', manager=self.manager,
                                             object_id='#faster_x3_button'),
                'restart_button': UIButton(relative_rect=pygame.Rect(40, 590, 140, 30), text='Restart',
                                           tool_tip_text='Restart simulation', manager=self.manager),
            }
        }

        self.developer = {
            'elements': {
                'dev_label': UILabel(relative_rect=pygame.Rect(0, 680, 200, 30), text='Created by S1riyS',
                                     manager=self.manager, object_id="#subtitle"),
            }
        }

    @staticmethod
    def set_label_color(element: UILabel, bg_color: pygame.Color) -> None:
        """
        Static method that applying style to element of GUI
        :param element: element of GUI
        :param bg_color: Background color of element
        :return: None
        """

        element.bg_colour = pygame.Color(bg_color)
        element.rebuild()

    @staticmethod
    def set_button_color(button: UIButton, color: pygame.Color) -> None:
        button.colours['normal_bg'] = color
        button.rebuild()

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
        # GUI element with biggest (Y + height) value
        max_y_rect = sorted(rect_array, key=lambda x: x[1] + x[3])[-1]
        # GUI element with biggest (X + width) value
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
