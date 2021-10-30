"""
Main project file, that containing game loop
"""

# Modules
import copy

from pygame.math import Vector2
import pygame_gui
from pygame_gui.windows import UIColourPickerDialog

from app.config import *
from app.gui import GUI  # Importing entire GUI

pygame.init()


class Game:
    def __init__(self):
        # PyGame screen variables
        self.screen = pygame.display.set_mode(WINDOW_SIZE)  # Initialize screen
        pygame.display.set_caption("Gravity Simulation")  # Caption
        self.icon = pygame.image.load('data/images/logo.png')  # icon
        pygame.display.set_icon(self.icon)  # Setting icon
        self.clock = pygame.time.Clock()  # Clock

        # Initiating beginning colors
        self.current_planet_color = copy.copy(PLANET_COLOR)
        self.current_star_color = copy.copy(STAR_COLOR)

        # Grid surface
        self.is_drawing_grid = True
        self.grid_surface = pygame.Surface(WINDOW_SIZE).convert_alpha()
        self.grid_surface.fill((0, 0, 0, 0))

        # Simulation surfaces
        self.is_drawing_glow = True
        self.is_drawing_trace = True

        self.init_gui()  # Initiating GUI

    @staticmethod
    def set_label_color(element: pygame_gui.elements, bg_color: pygame.Color) -> None:
        """
        Static method that applying style to element of GUI
        :param element: element of GUI
        :param bg_color: Background color of element
        :return: None
        """

        element.bg_colour = pygame.Color(bg_color)
        element.rebuild()

    @staticmethod
    def set_button_color(button: pygame_gui.elements.UIButton, color: pygame.Color) -> None:
        button.colours['normal_bg'] = color
        button.rebuild()

    @staticmethod
    def mouse_collision_with_gui(mouse_position: tuple, gui_rects: list) -> bool:
        """
        Return True if mouse on any of GUI rects and False if it isn't
        :param gui_rects: Rect of group of GUI elements
        :param mouse_position: Mouse position (x, y)
        :return: bool
        """

        return any([rect.collidepoint(mouse_position) for rect in gui_rects])

    @staticmethod
    def draw_grid(surface: pygame.Surface, color: pygame.Color, distance: int) -> None:
        """
        Static method that draws grid
        :param surface: The surface on which the grid will be drawn
        :param color: Color of grid
        :param distance: Distance between lines of grid
        :return: None
        """
        for x in range(int(WIDTH / distance) + 2):
            pygame.draw.line(surface, color, (x * distance, 0), (x * distance, HEIGHT), 1)
        for y in range(int(HEIGHT / distance) + 2):
            pygame.draw.line(surface, color, (0, y * distance), (WIDTH, y * distance), 1)

    def init_gui(self) -> None:
        # Statements of window
        self.is_dialogue_open = False
        self.is_planet_window_open = False
        self.is_star_window_open = False

        self.gui = GUI()  # Creating object of GUI class

        # GUI rects
        self.info_gui_rect = self.gui.get_gui_rect(self.gui.info_block, 5)
        self.settings_gui_rect = self.gui.get_gui_rect(self.gui.settings_block, 5)

        # GUI elements
        self.info_gui_elements = self.gui.info_block['elements']
        self.settings_gui_elements = self.gui.settings_block['elements']

        # Planet
        self.set_label_color(self.settings_gui_elements['planet_color_surface'], self.current_planet_color)
        self.planet_color_button = self.settings_gui_elements['planet_color_button']
        self.planet_color_picker = None

        # Star
        self.set_label_color(self.settings_gui_elements['star_color_surface'], self.current_star_color)
        self.star_color_button = self.settings_gui_elements['star_color_button']
        self.star_color_picker = None

        # General
        self.grid_button = self.settings_gui_elements['grid_button']
        self.glow_button = self.settings_gui_elements['glow_button']
        self.trace_button = self.settings_gui_elements['trace_button']

        # Dictionary that contains {key:value} pairs of the form {button: is_drawing_this_surface}
        self.radio_buttons = {
            self.grid_button: True,
            self.glow_button: True,
            self.trace_button: True
        }

        # Making all buttons green
        for button in self.radio_buttons.keys():
            self.set_button_color(button, BUTTON_GREEN)

    def restart(self) -> None:
        # Cleaning groups of sprites
        self.simulation_manager.stars.empty()
        self.simulation_manager.planets.empty()
        self.simulation_manager.celestial_bodies.empty()

        # Initiating beginning colors
        self.current_planet_color = copy.copy(PLANET_COLOR)
        self.set_label_color(self.settings_gui_elements['planet_color_surface'], self.current_planet_color)
        self.current_star_color = copy.copy(STAR_COLOR)
        self.set_label_color(self.settings_gui_elements['star_color_surface'], self.current_star_color)

        # Resetting UIHorizontalSliders
        self.settings_gui_elements['planet_mass_slider'].set_current_value(PLANET_DEFAULT_MASS)
        self.settings_gui_elements['star_mass_slider'].set_current_value(STAR_DEFAULT_MASS)

        # Dictionary that contains {key:value} pairs of the form {button: is_drawing_this_surface}
        self.radio_buttons = {
            self.grid_button: True,
            self.glow_button: True,
            self.trace_button: True
        }

        # Making all radio buttons green as a default
        for button in self.radio_buttons.keys():
            self.set_button_color(button, BUTTON_GREEN)

    def run(self) -> None:
        # Import everything necessary from objects
        from app.objects import simulation_manager, Planet, Star
        self.simulation_manager = simulation_manager  # Creating 'local copy' of simulation manager

        # Game loop
        self.is_running = True
        while self.is_running:

            # Checking if any of windows are open
            self.is_dialogue_open = self.is_planet_window_open or self.is_star_window_open

            # Filling surfaces
            self.simulation_manager.glow_surface.fill((0, 0, 0, 0))
            self.simulation_manager.trace_surface.fill((0, 0, 0, 0))
            self.grid_surface.fill((0, 0, 0, 0))
            self.screen.fill(DARK_BLUE)

            # Drawing grid
            self.draw_grid(self.grid_surface, grid_color, grid_distance)

            self.clock.tick(FPS)
            self.time_delta = self.clock.tick(FPS) / 1000.0

            # Event loop
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    self.is_running = False

                # User events
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
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
                                self.set_button_color(event.ui_element, BUTTON_RED)
                            else:
                                self.set_button_color(event.ui_element, BUTTON_GREEN)

                            self.radio_buttons[event.ui_element] = not self.radio_buttons[event.ui_element]

                        if event.ui_element == self.settings_gui_elements['restart_button']:
                            self.restart()

                    if event.user_type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                        # If picked color of planet
                        if event.ui_element == self.planet_color_picker:
                            self.current_planet_color = event.colour
                            self.set_label_color(self.settings_gui_elements['planet_color_surface'],
                                                 self.current_planet_color)

                        # If picked color of star
                        if event.ui_element == self.star_color_picker:
                            self.current_star_color = event.colour
                            self.set_label_color(self.settings_gui_elements['star_color_surface'],
                                                 self.current_star_color)

                    if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
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

                # Mouse events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Mouse position
                    pressed_mouse_position = pygame.mouse.get_pos()
                    mouse_x, mouse_y = pressed_mouse_position

                    # Checking if mouse on GUI
                    is_mouse_on_gui = self.mouse_collision_with_gui(
                        mouse_position=pressed_mouse_position,
                        gui_rects=self.gui.gui_rects) or self.is_dialogue_open

                    if event.button == 3 and not is_mouse_on_gui:
                        # Creating a star
                        Star(
                            x=mouse_x,
                            y=mouse_y,
                            mass=self.settings_gui_elements['star_mass_slider'].get_current_value(),
                            color=self.current_star_color
                        )

                if event.type == pygame.MOUSEBUTTONUP and not is_mouse_on_gui:
                    if event.button == 1:
                        try:
                            # Creating a planet
                            Planet(
                                x=mouse_x,
                                y=mouse_y,
                                velocity=velocity_vector,
                                mass=self.settings_gui_elements['planet_mass_slider'].get_current_value(),
                                color=self.current_planet_color
                            )

                            # Setting labels
                            self.info_gui_elements['velocity_x_label'].set_text('X velocity: None')
                            self.info_gui_elements['velocity_y_label'].set_text('Y velocity: None')

                        except Exception as error:
                            print(f'Velocity vector is not defined. Error: {error}')

                self.gui.manager.process_events(event)

            # Drawing line of velocity of new planet
            pressed = pygame.mouse.get_pressed()  # Pressed buttons
            if pressed[0] and not is_mouse_on_gui:
                # Mouse position (x, y)
                current_mouse_position = pygame.mouse.get_pos()
                current_mouse_x, current_mouse_y = current_mouse_position

                # Calculating velocity vector
                current_pos_vector = Vector2(current_mouse_x, current_mouse_y)
                pressed_pos_vector = Vector2(mouse_x, mouse_y)
                velocity_vector = -(current_pos_vector - pressed_pos_vector) * pv_velocity_value_coef

                # Setting labels
                self.info_gui_elements['velocity_x_label'].set_text(f'X velocity: {round(velocity_vector.x, 4)}')
                self.info_gui_elements['velocity_y_label'].set_text(f'Y velocity: {-round(velocity_vector.y, 4)}')

                # Drawing preview
                pygame.draw.circle(self.screen, WHITE, (mouse_x, mouse_y), pv_radius)
                pygame.draw.line(self.screen, WHITE,
                                 (mouse_x, mouse_y),
                                 (mouse_x + velocity_vector.x * pv_line_length_coef,
                                  mouse_y + velocity_vector.y * pv_line_length_coef), pv_line_thickness)

            # --- Updating elements of game --- #
            if self.radio_buttons[self.grid_button]:
                self.screen.blit(self.grid_surface, (0, 0))  # Drawing grid

            # Simulation objects
            self.simulation_manager.celestial_bodies.update(dt=self.time_delta)

            if self.radio_buttons[self.glow_button]:
                self.screen.blit(self.simulation_manager.glow_surface, (0, 0))  # Blit glow surface
            if self.radio_buttons[self.trace_button]:
                self.screen.blit(self.simulation_manager.trace_surface, (0, 0))  # Blit trace surface

            self.simulation_manager.celestial_bodies.draw(self.screen)

            # GUI
            for rect in self.gui.gui_rects:
                pygame.draw.rect(self.screen, self.gui.gui_rect_color, rect)

            self.info_gui_elements['FPS_counter'].set_text(f'FPS: {int(self.clock.get_fps())}')  # FPS
            self.gui.manager.update(self.time_delta)
            self.gui.manager.draw_ui(self.screen)

            # Display
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    print('Simulation has been started!')
    game = Game()
    game.run()
