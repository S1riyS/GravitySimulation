"""
Module containing GUI elements and other settings
"""

# Modules
import pygame
import pygame_gui

from config import *

# GUI manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

GUI_margin = 10  # Margin of GUI
GUI_array = []  # Array of GUI elements

# GUI
velocity_x_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 10, 200, 20),
                                               text='X velocity: None', manager=manager)
velocity_y_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 35, 200, 20),
                                               text='Y velocity: None', manager=manager)
G_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 60, 200, 20),
                                      text=f'G = {G}', manager=manager)
K_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 85, 200, 20),
                                      text=f'Distance coef = {K_value}', manager=manager)

GUI_array.extend([velocity_x_label, velocity_x_label, G_label, K_label])  # Adding elements to array

# Manager rect
manager_rect_indent = 10  # Indent
manager_rect_color = pygame.Color(0, 0, 11)  # Color
manager_rect_width = max([element.rect.width for element in GUI_array]) + manager_rect_indent + GUI_margin  # Width
manager_rect_height = GUI_array[-1].rect.y + GUI_array[-1].rect.height + manager_rect_indent  # Height
manager_rect = pygame.Rect(0, 0, manager_rect_width, manager_rect_height)  # Rect
