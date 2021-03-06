"""
Main project file, that containing game loop
"""

# Modules
from copy import copy

import pygame
from pygame.math import Vector2  # 2D vector
from pygame_gui.windows import UIColourPickerDialog  # Windows
from pygame_gui import UI_BUTTON_PRESSED, UI_COLOUR_PICKER_COLOUR_PICKED, UI_WINDOW_CLOSE  # GUI events

pygame.init()

from app.scripts.simulation import SimulationManager, Planet, Star  # Classes
from app.scripts.grid import Grid  # Background grid
from app.scripts.gui import GUI  # GUI
from app.scripts.config import Config  # Config
from app.scripts.events import CustomEvents  # Custom events


class Game:
    def __init__(self):
        # PyGame settings
        self.screen = pygame.display.set_mode(Config.WINDOW_SIZE)  # Initialize screen
        self.icon = pygame.image.load('../data/images/logo.png')  # icon
        pygame.display.set_icon(self.icon)  # Setting icon
        pygame.display.set_caption("Gravity Simulation")  # Caption
        self.clock = pygame.time.Clock()  # Clock

        # Grid
        self.grid = Grid(color=Config.GRID_COLOR, distance=Config.GRID_DISTANCE)  # Creating object of Grid class
        self.grid.calculate_grid_dots()  # Calculating dots

        self.animation_speed = 1  # Animation speed

        self.init_gui()  # Initiating GUI

    @staticmethod
    def mouse_collision_with_gui(mouse_position: tuple, gui_rects: list) -> bool:
        """
        Return True if mouse on any of GUI rects and False if it isn't
        :param gui_rects: Rect of group of GUI elements
        :param mouse_position: Mouse position (x, y)
        :return: bool
        """

        return any([rect.collidepoint(mouse_position) for rect in gui_rects])

    def init_gui(self) -> None:
        self.gui = GUI()  # Creating object of GUI class

        # Initiating beginning colors
        self.current_planet_color = copy(Config.PLANET_COLOR)
        self.current_star_color = copy(Config.STAR_COLOR)

        # Statements of window
        self.is_dialogue_open = False
        self.is_planet_window_open = False
        self.is_star_window_open = False

        # GUI rects
        self.gui.get_gui_rect(self.gui.info, 5)
        self.gui.get_gui_rect(self.gui.settings, 5)

        # GUI elements
        self.info_gui_elements = self.gui.info['elements']
        self.settings_gui_elements = self.gui.settings['elements']

        # Planet
        self.gui.set_label_color(self.settings_gui_elements['planet_color_surface'], self.current_planet_color)
        self.planet_color_button = self.settings_gui_elements['planet_color_button']
        self.planet_color_picker = None

        # Star
        self.gui.set_label_color(self.settings_gui_elements['star_color_surface'], self.current_star_color)
        self.star_color_button = self.settings_gui_elements['star_color_button']
        self.star_color_picker = None

        # General
        self.grid_button = self.settings_gui_elements['grid_button']
        self.glow_button = self.settings_gui_elements['glow_button']
        self.trace_button = self.settings_gui_elements['trace_button']
        self.curvature_button = self.settings_gui_elements['curvature_button']

        # Dictionary that contains {key:value} pairs of the form {button: is_drawing_this_surface}
        self.radio_buttons = {
            self.grid_button: True,
            self.glow_button: True,
            self.trace_button: True,
            self.curvature_button: True
        }

        # Making all buttons green
        for button in self.radio_buttons.keys():
            self.gui.set_button_color(button, Config.BUTTON_GREEN)

        # Simulation speed
        self.pause_button = self.settings_gui_elements['pause_button']
        self.play_button = self.settings_gui_elements['play_button']
        self.faster_x2_button = self.settings_gui_elements['faster_x2_button']
        self.faster_x3_button = self.settings_gui_elements['faster_x3_button']

        self.play_button.disable()

        self.multimedia_buttons = {
            self.pause_button: 0,
            self.play_button: 1,
            self.faster_x2_button: 2,
            self.faster_x3_button: 3
        }

    def restart(self) -> None:

        # Cleaning groups of sprites
        SimulationManager.stars.empty()
        SimulationManager.planets.empty()
        SimulationManager.celestial_bodies.empty()

        # Initiating beginning colors
        self.current_planet_color = copy(Config.PLANET_COLOR)
        self.gui.set_label_color(self.settings_gui_elements['planet_color_surface'], self.current_planet_color)
        self.current_star_color = copy(Config.STAR_COLOR)
        self.gui.set_label_color(self.settings_gui_elements['star_color_surface'], self.current_star_color)

        # Resetting UIHorizontalSliders
        self.settings_gui_elements['planet_mass_slider'].set_current_value(Config.PLANET_DEFAULT_MASS)
        self.settings_gui_elements['star_mass_slider'].set_current_value(Config.STAR_DEFAULT_MASS)

        # Dictionary that contains {key:value} pairs of the form {button: is_drawing_this_surface}
        self.radio_buttons = {
            self.grid_button: True,
            self.glow_button: True,
            self.trace_button: True,
            self.curvature_button: True
        }

        # Making all radio buttons green as a default
        for button in self.radio_buttons.keys():
            self.gui.set_button_color(button, Config.BUTTON_GREEN)

        # Resetting media buttons
        for button in self.multimedia_buttons:
            button.enable()

        self.play_button.disable()
        self.animation_speed = 1

        # Resetting background grid dots
        self.grid.calculate_grid_dots()

    def clear_surfaces(self) -> None:
        # Filling surfaces
        SimulationManager.glow_surface.fill(Config.TRANSPARENT)
        SimulationManager.trace_surface.fill(Config.TRANSPARENT)
        self.grid.surface.fill(Config.TRANSPARENT)
        self.screen.fill(Config.DARK_BLUE)

    def handle_events(self) -> None:
        # Checking if any of windows are open
        self.is_dialogue_open = self.is_planet_window_open or self.is_star_window_open

        # Event loop
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                self.is_running = False
                print('Simulation has ended')

            # User events
            if event.type == pygame.USEREVENT:
                if event.user_type == UI_BUTTON_PRESSED:
                    # If pressed planet's "choose color" button
                    if event.ui_element == self.planet_color_button:
                        self.is_planet_window_open = True
                        self.planet_color_picker = UIColourPickerDialog(pygame.Rect(210, 0, 390, 390),
                                                                        window_title='Planet color ...',
                                                                        initial_colour=self.current_planet_color,
                                                                        manager=self.gui.manager)
                        self.planet_color_button.disable()

                    # If pressed star's "choose color" button
                    if event.ui_element == self.star_color_button:
                        self.is_star_window_open = True
                        self.star_color_picker = UIColourPickerDialog(pygame.Rect(230, 30, 390, 390),
                                                                      window_title='Star color ...',
                                                                      initial_colour=self.current_star_color,
                                                                      manager=self.gui.manager)
                        self.star_color_button.disable()

                    # if pressed button in dict of radio buttons
                    if event.ui_element in self.radio_buttons:
                        if self.radio_buttons[event.ui_element]:
                            self.gui.set_button_color(event.ui_element, Config.BUTTON_RED)
                        else:
                            self.gui.set_button_color(event.ui_element, Config.BUTTON_GREEN)

                        self.radio_buttons[event.ui_element] = not self.radio_buttons[event.ui_element]

                    # If pressed button in dict of multimedia buttons
                    if event.ui_element in self.multimedia_buttons:
                        self.animation_speed = self.multimedia_buttons[event.ui_element]
                        for button in self.multimedia_buttons:
                            button.enable()
                        event.ui_element.disable()

                    # Restart button
                    if event.ui_element == self.settings_gui_elements['restart_button']:
                        self.restart()

                if event.user_type == UI_COLOUR_PICKER_COLOUR_PICKED:
                    # If picked color of planet
                    if event.ui_element == self.planet_color_picker:
                        self.current_planet_color = event.colour
                        self.gui.set_label_color(self.settings_gui_elements['planet_color_surface'],
                                                 self.current_planet_color)

                    # If picked color of star
                    if event.ui_element == self.star_color_picker:
                        self.current_star_color = event.colour
                        self.gui.set_label_color(self.settings_gui_elements['star_color_surface'],
                                                 self.current_star_color)

                if event.user_type == UI_WINDOW_CLOSE:
                    # If closed planet's "Colour Picker Dialog"
                    if event.ui_element == self.planet_color_picker:
                        self.is_planet_window_open = False
                        self.planet_color_button.enable()
                        self.planet_color_picker = None

                    # If closed star's "Colour Picker Dialog"
                    if event.ui_element == self.star_color_picker:
                        self.is_star_window_open = False
                        self.star_color_button.enable()
                        self.star_color_picker = None

            # Mouse button down event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Mouse position
                pressed_mouse_position = pygame.mouse.get_pos()
                self.mouse_x, self.mouse_y = pressed_mouse_position

                # Checking if mouse on GUI
                self.is_mouse_on_gui = self.mouse_collision_with_gui(
                    mouse_position=pressed_mouse_position,
                    gui_rects=self.gui.gui_rects) or self.is_dialogue_open

                if event.button == 3 and not self.is_mouse_on_gui:
                    # Creating a star
                    Star(
                        x=self.mouse_x,
                        y=self.mouse_y,
                        mass=self.settings_gui_elements['star_mass_slider'].get_current_value(),
                        color=copy(self.current_star_color)
                    )

            # Mouse button up event
            elif event.type == pygame.MOUSEBUTTONUP and not self.is_mouse_on_gui:
                if event.button == 1:
                    try:
                        # Creating a planet
                        Planet(
                            x=self.mouse_x,
                            y=self.mouse_y,
                            velocity=self.velocity_vector,
                            mass=self.settings_gui_elements['planet_mass_slider'].get_current_value(),
                            color=copy(self.current_planet_color)
                        )

                        # Setting labels
                        self.info_gui_elements['velocity_x_label'].set_text('X velocity: None')
                        self.info_gui_elements['velocity_y_label'].set_text('Y velocity: None')

                    except Exception as error:
                        print(f'Velocity vector is not defined. Error: {error}')

            elif event.type == CustomEvents.ADDED_NEW_STAR or event.type == CustomEvents.CHANGED_STAR_MASS:
                self.grid.calculate_grid_dots()  # Calculating dots

            self.gui.manager.process_events(event)

        # Drawing preview line of velocity of new planet
        pressed = pygame.mouse.get_pressed()  # Pressed buttons
        if pressed[0] and not self.is_mouse_on_gui:
            # Mouse position (x, y)
            current_mouse_position = pygame.mouse.get_pos()
            current_mouse_x, current_mouse_y = current_mouse_position

            # Calculating velocity vector
            current_pos_vector = Vector2(current_mouse_x, current_mouse_y)
            pressed_pos_vector = Vector2(self.mouse_x, self.mouse_y)
            self.velocity_vector = -(current_pos_vector - pressed_pos_vector) * Config.PV_VELOCITY_COEF

            # Setting labels
            self.info_gui_elements['velocity_x_label'].set_text(f'X velocity: {round(self.velocity_vector.x, 4)}')
            self.info_gui_elements['velocity_y_label'].set_text(f'Y velocity: {-round(self.velocity_vector.y, 4)}')

            # Drawing preview
            preview_radius = Planet.get_radius(self.settings_gui_elements['planet_mass_slider'].get_current_value())
            pygame.draw.circle(self.screen, Config.WHITE, (self.mouse_x, self.mouse_y), preview_radius)
            pygame.draw.line(self.screen, Config.WHITE,
                             (self.mouse_x, self.mouse_y),
                             (self.mouse_x + self.velocity_vector.x * Config.PV_LENGTH_COEF,
                              self.mouse_y + self.velocity_vector.y * Config.PV_LENGTH_COEF),
                             Config.PV_LINE_THICKNESS)

    def update(self) -> None:
        # Drawing grid
        if self.radio_buttons[self.grid_button]:
            if self.radio_buttons[self.curvature_button]:
                self.grid.draw_curved_grid()  # Drawing curved grid on grid.surface
            else:
                self.grid.draw_normal_grid()  # Drawing normal grid on grid.surface

            self.screen.blit(self.grid.surface, (0, 0))  # Drawing grid.surface on screen

        # Simulation objects
        SimulationManager.celestial_bodies.update(dt=self.animation_speed * self.time_delta)

        if self.radio_buttons[self.glow_button]:
            self.screen.blit(SimulationManager.glow_surface, (0, 0))  # Blit glow surface
        if self.radio_buttons[self.trace_button]:
            self.screen.blit(SimulationManager.trace_surface, (0, 0))  # Blit trace surface

        SimulationManager.celestial_bodies.draw(self.screen)

        # GUI
        for rect in self.gui.gui_rects:
            pygame.draw.rect(self.screen, self.gui.gui_rect_color, rect)

        self.info_gui_elements['FPS_counter'].set_text(f'FPS: {int(self.clock.get_fps())}')  # FPS
        self.gui.manager.update(self.time_delta)
        self.gui.manager.draw_ui(self.screen)

        # Display
        pygame.display.flip()

    def run(self) -> None:
        # Game loop
        self.is_running = True

        while self.is_running:
            self.clock.tick(Config.FPS)
            self.time_delta = self.clock.tick(Config.FPS) / 1000.0

            self.clear_surfaces()  # Clearing surfaces
            self.handle_events()  # Handling events
            self.update()  # Updating

        pygame.quit()  # Quit


if __name__ == "__main__":
    print('Simulation has been started!')
    game = Game()
    game.run()
