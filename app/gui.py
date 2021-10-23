"""
Module containing GUI elements and other settings
"""

# Modules
import pygame
import pygame_gui

from config import *


class GUIManager:
    def __init__(self):
        # GUI manager
        self.manager = pygame_gui.UIManager(WINDOW_SIZE)
        self.manager_rect_color = pygame.Color(0, 10, 26)  # Color

        self.info_block = {
            'elements_dict': {
                # GUI
                'velocity_x_label': pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 10, 200, 20),
                                                                text='X velocity: None', manager=self.manager),
                'velocity_y_label': pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 35, 200, 20),
                                                                text='Y velocity: None', manager=self.manager),
                'G_label': pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 60, 200, 20),
                                                       text=f'G = {G}', manager=self.manager),
                'K_label': pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 85, 200, 20),
                                                       text=f'Distance coef = {K_value}', manager=self.manager)
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

        elements_array = gui_dictionary['elements_dict'].values()  # Array of GUI elements

        # GUI rect with biggest Y value
        last_rect = sorted(
            [element.rect for element in elements_array],
            key=lambda x: x[1]
        )[-1]

        rect_x = min([element.rect.x for element in elements_array])  # Top left X
        rect_y = min([element.rect.y for element in elements_array])  # Top left Y
        rect_width = max([element.rect.width for element in elements_array])  # Width
        rect_height = last_rect.y - rect_y + last_rect.height  # Height

        # Rect
        gui_rect = pygame.Rect(rect_x - padding,  # X
                               rect_y - padding,  # Y
                               rect_width + 2 * padding,  # Width
                               rect_height + 2 * padding  # Height
                               )
        return gui_rect
