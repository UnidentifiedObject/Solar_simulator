import pygame
import pygame_gui
from pygame_gui.windows.ui_colour_picker_dialog import UIColourPickerDialog
import random


pygame.init()

# === CONFIGURATION ===
# constants, screen size, etc.

WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 920
FPS = 60

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Solar System Simulator")
clock = pygame.time.Clock()
STAR_POS = pygame.Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
STAR_RADIUS = 40
STAR_COLOR = (255, 255, 100)  # yellowish star
G = 0.1  # gravitational constant (adjust for realism/speed)
STAR_MASS = 10000  # arbitrary large mass of central star

def rel(x_perc, y_perc, w_perc, h_perc):
    return pygame.Rect(
        WINDOW_WIDTH * x_perc,
        WINDOW_HEIGHT * y_perc,
        WINDOW_WIDTH * w_perc,
        WINDOW_HEIGHT * h_perc
    )



planets = []  # will hold planet dicts with position and velocity vectors
planet_configs = []
current_screen = "welcome"


simulation_running = True

# === UI SETUP ===

ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
# Welcome screen
welcome_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.25, 0.1, 0.5, 0.06),
    text=" Welcome to Solar System Simulator ",
    manager=ui_manager
)

proceed_button = pygame_gui.elements.UIButton(
    relative_rect=rel(0.35, 0.2, 0.3, 0.06),
    text="Start Configuration",
    manager=ui_manager
)

name_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.19, 0.08, 0.08, 0.04),
    text="Name:",
    manager=ui_manager,
    visible=0
)

name_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=rel(0.25, 0.08, 0.15, 0.04),
    manager=ui_manager,
    visible=0
)

planet_title = pygame_gui.elements.UILabel(
    relative_rect=rel(0.25, 0.03, 0.5, 0.05),
    text="Configure Planet 1",
    manager=ui_manager,
    visible=0
)

radius_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=rel(0.25, 0.13, 0.5, 0.05),
    start_value=20,
    value_range=(5, 100),
    manager=ui_manager,
    visible=0
)

radius_value_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.78, 0.13, 0.05, 0.05),
    text="20",
    manager=ui_manager,
    visible=0
)

mass_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=rel(0.25, 0.2, 0.5, 0.05),
    start_value=10,
    value_range=(1, 200),
    manager=ui_manager,
    visible=0
)

radius_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.18, 0.13, 0.1, 0.05),
    text="Radius:",
    manager=ui_manager,
    visible=0
)

mass_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.18, 0.20, 0.1, 0.05),
    text="Mass:",
    manager=ui_manager,
    visible=0
)


mass_value_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.78, 0.2, 0.05, 0.05),
    text="10",
    manager=ui_manager,
    visible=0
)

radius_help_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.25, 0.18, 0.4, 0.03),
    text=" Radius affects how large the planet appears",
    manager=ui_manager,
    visible=0
)

mass_help_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.25, 0.25, 0.5, 0.03),
    text=" Mass determines the planet's gravity strength",
    manager=ui_manager,
    visible=0
)

x_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=rel(0.25, 0.32, 0.12, 0.05),
    manager=ui_manager,
    visible=0
)

y_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=rel(0.38, 0.32, 0.12, 0.05),
    manager=ui_manager,
    visible=0
)

vx_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=rel(0.25, 0.39, 0.12, 0.05),
    manager=ui_manager,
    visible=0
)

vy_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=rel(0.38, 0.39, 0.12, 0.05),
    manager=ui_manager,
    visible=0
)

pos_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.19, 0.32, 0.06, 0.05),
    text="Pos X,Y:",
    manager=ui_manager,
    visible=0
)

vel_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.19, 0.39, 0.06, 0.05),
    text="Vel VX,VY:",
    manager=ui_manager,
    visible=0
)

x_help_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.52, 0.32, 0.25, 0.03),
    text="Increase X to move planet right",
    manager=ui_manager,
    visible=0
)

y_help_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.52, 0.35, 0.25, 0.03),
    text="Increase Y to move planet down",
    manager=ui_manager,
    visible=0
)

vx_help_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.52, 0.39, 0.35, 0.03),
    text="Increase VX to move planet horizontally",
    manager=ui_manager,
    visible=0
)

vy_help_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.52, 0.42, 0.35, 0.03),
    text="Increase VY to move planet vertically",
    manager=ui_manager,
    visible=0
)

color_button = pygame_gui.elements.UIButton(
    relative_rect=rel(0.09, 0.13, 0.12, 0.05),
    text="Pick Color",
    manager=ui_manager,
    visible=0
)

next_planet_button = pygame_gui.elements.UIButton(
    relative_rect=rel(0.35, 0.5, 0.3, 0.06),
    text="Next Planet",
    manager=ui_manager,
    visible=0
)

randomize_button = pygame_gui.elements.UIButton(
    relative_rect=rel(0.35, 0.58, 0.3, 0.06),
    text="Randomize Planet",
    manager=ui_manager,
    visible=0
)

number_label = pygame_gui.elements.UILabel(
    relative_rect=rel(0.3, 0.1, 0.4, 0.05),
    text="Enter number of planets (1–10):",
    manager=ui_manager,
    visible=0
)

number_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=rel(0.35, 0.16, 0.3, 0.05),
    manager=ui_manager,
    visible=0
)
number_input.set_text("3")

number_submit = pygame_gui.elements.UIButton(
    relative_rect=rel(0.35, 0.23, 0.3, 0.05),
    text="Configure Planets",
    manager=ui_manager,
    visible=0
)

# === HELPER FUNCTIONS ===

def show_planet_config(index):
    planet_title.set_text(f"Configure Planet {index + 1}")
    planet_title.show()
    color_button.show()
    name_label.show()
    name_input.show()
    radius_label.show()
    mass_label.show()
    pos_label.show()
    vel_label.show()
    radius_slider.show()
    mass_slider.show()
    x_input.show()
    y_input.show()
    vx_input.show()
    vy_input.show()
    next_planet_button.show()
    randomize_button.show()
    radius_value_label.show()
    mass_value_label.show()
    radius_help_label.show()
    mass_help_label.show()
    x_help_label.show()
    y_help_label.show()
    vx_help_label.show()
    vy_help_label.show()


def hide_planet_config():
    planet_title.hide()
    color_button.hide()
    name_label.hide()
    name_input.hide()
    radius_label.hide()
    mass_label.hide()
    pos_label.hide()
    vel_label.hide()
    radius_slider.hide()
    mass_slider.hide()
    x_input.hide()
    y_input.hide()
    vx_input.hide()
    vy_input.hide()
    next_planet_button.hide()
    radius_value_label.hide()
    mass_value_label.hide()
    radius_help_label.hide()
    mass_help_label.hide()
    x_help_label.hide()
    y_help_label.hide()
    vx_help_label.hide()
    vy_help_label.hide()

def randomize_planet():
    radius = random.randint(5, 100)
    mass = random.randint(1, 200)
    x = random.uniform(100, WINDOW_WIDTH - 100)
    y = random.uniform(100, WINDOW_HEIGHT - 100)
    vx = random.uniform(-2, 2)
    vy = random.uniform(-2, 2)
    name = f"Planet{random.randint(1, 999)}"
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    # Update UI inputs
    radius_slider.set_current_value(radius)
    mass_slider.set_current_value(mass)
    x_input.set_text(str(round(x, 1)))
    y_input.set_text(str(round(y, 1)))
    vx_input.set_text(str(round(vx, 2)))
    vy_input.set_text(str(round(vy, 2)))
    name_input.set_text(name)

    # Update global color variable and color preview rectangle fill
    global planet_color
    planet_color = color


# ---------- Main Loop ----------
color_picker_dialog = None  # global color picker dialog
planet_color = (100, 100, 255)  # default color
color_preview_rect = pygame.Rect(1020, 120, 60, 60)  # color preview rectangle
font = pygame.font.SysFont(None, 20)  # font for planet names
NUM_STARS = 150
star_positions = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for _ in range(NUM_STARS)]

running = True
while running:
    time_delta = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Process UI events first
        ui_manager.process_events(event)

        if current_screen == "simulation":
            # Show restart hint
            hint_text = font.render("Press 'R' to restart", True, (200, 200, 200))
            window.blit(hint_text, (10, 10))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and current_screen == "simulation":
                print("🔁 Restarting simulation...")

                # Reset to configuration state
                current_screen = "config_count"
                simulation_running = True

                # Reset planet list and configs
                planets.clear()
                planet_configs.clear()
                current_planet_index = 0

                # Reset UI elements
                number_input.set_text("3")
                number_label.show()
                number_input.show()
                number_submit.show()

        # Handle UI button presses
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == proceed_button:
                current_screen = "config_count"
                welcome_label.hide()
                proceed_button.hide()
                number_label.show()
                number_input.show()
                number_submit.show()

            elif event.ui_element == next_planet_button:
                try:
                    planet_data = {
                        'name': name_input.get_text(),
                        'color': planet_color,
                        'radius': int(radius_slider.get_current_value()),
                        'mass': int(mass_slider.get_current_value()),
                        'x': float(x_input.get_text()),
                        'y': float(y_input.get_text()),
                        'vx': float(vx_input.get_text()),
                        'vy': float(vy_input.get_text())
                    }
                    planet_configs.append(planet_data)
                    print(f"✅ Planet {current_planet_index + 1} config saved: {planet_data}")

                    current_planet_index += 1

                    if current_planet_index < num_planets:
                        radius_slider.set_current_value(20)
                        mass_slider.set_current_value(10)
                        x_input.set_text("600")
                        y_input.set_text("400")
                        vx_input.set_text("0")
                        vy_input.set_text("1.5")
                        show_planet_config(current_planet_index)
                        current_screen = "config_planet"  # important to keep screen here
                    else:
                        print("🚀 All planets configured!")
                        hide_planet_config()
                        planets.clear()
                        for cfg in planet_configs:
                            planet = {
                                'name': cfg['name'],
                                'radius': cfg['radius'],
                                'mass': cfg['mass'],
                                'pos': pygame.Vector2(cfg['x'], cfg['y']),
                                'vel': pygame.Vector2(cfg['vx'], cfg['vy']),
                                'color': cfg['color'],
                                'alpha' : 255,
                                'trail': []
                            }
                            planets.append(planet)

                        number_label.hide()
                        number_input.hide()
                        number_submit.hide()
                        hide_planet_config()
                        current_screen = "simulation"

                except Exception as e:
                    print(f"⚠️ Error in input: {e}")

            elif event.ui_element == number_submit:
                try:
                    num_planets = int(number_input.get_text())
                    if 1 <= num_planets <= 10:
                        print(f"✅ Number of planets: {num_planets}")
                        current_planet_index = 0
                        planet_configs.clear()

                        number_label.hide()
                        number_input.hide()
                        number_submit.hide()

                        show_planet_config(current_planet_index)
                        current_screen = "config_planet"  # set this screen

                    else:
                        print("⚠️ Please enter a number from 1 to 10.")
                except ValueError:
                    print("⚠️ Invalid input! Enter a number.")

            elif event.ui_element == color_button:
                if color_picker_dialog is None:
                    color_picker_dialog = UIColourPickerDialog(
                    pygame.Rect((WINDOW_WIDTH - 400) // 2, (WINDOW_HEIGHT - 400) // 2, 400, 400),  # centered
                    ui_manager,
                    window_title='Pick Planet Color',
                    initial_colour=pygame.Color(*planet_color)
                )

            elif event.ui_element == randomize_button:
                randomize_planet()

        # Handle color picker picked event
        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            planet_color = event.colour
            print(f"Color picked: {planet_color}")
            color_picker_dialog = None

        # Handle color picker window close event
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == color_picker_dialog:
                color_picker_dialog = None

    ui_manager.update(time_delta)

    window.fill((0, 0, 0))

    if current_screen == "simulation" and simulation_running:
        # Draw background stars
        for pos in star_positions:
            brightness = random.randint(150, 255)  # optional: twinkle effect
            pygame.draw.circle(window, (brightness, brightness, brightness), pos, 1)

        for p in planets[:]:  # copy for safe removal
            direction = STAR_POS - p['pos']
            distance = direction.length()

            if distance <= STAR_RADIUS + p['radius']:
                # Planet collided with star, remove it
                planets.remove(p)
                continue

            if distance > 0:
                force_magnitude = G * STAR_MASS * p['mass'] / (distance ** 2)
                acceleration = direction.normalize() * (force_magnitude / p['mass'])
                p['vel'] += acceleration * time_delta * 60  # scale by frame rate

            # Move planet
            p['pos'] += p['vel'] * time_delta * 60
            p['trail'].append(p['pos'].copy())

            # Limit trail length
            if len(p['trail']) > 300:
                p['trail'].pop(0)

            # Screen wrapping
            if p['pos'].x < 0:
                p['pos'].x = WINDOW_WIDTH
            elif p['pos'].x > WINDOW_WIDTH:
                p['pos'].x = 0

            if p['pos'].y < 0:
                p['pos'].y = WINDOW_HEIGHT
            elif p['pos'].y > WINDOW_HEIGHT:
                p['pos'].y = 0

    if current_screen == "simulation":
        # Draw star
        pygame.draw.circle(window, STAR_COLOR, (int(STAR_POS.x), int(STAR_POS.y)), STAR_RADIUS)

        for p in planets:
            for i, point in enumerate(p['trail']):
                fade = int(255 * (i / len(p['trail'])))
                trail_color = (p['color'][0], p['color'][1], p['color'][2], fade)
                trail_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, trail_color, (2, 2), 2)
                window.blit(trail_surface, (int(point.x), int(point.y)))

        # Draw planets
        for p in planets:
            pygame.draw.circle(window, p['color'], (int(p['pos'].x), int(p['pos'].y)), p['radius'])
            # Draw planet name centered on planet
            text_surface = font.render(p['name'], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(int(p['pos'].x), int(p['pos'].y) - p['radius'] - 10))
            window.blit(text_surface, text_rect)

    else:
        ui_manager.draw_ui(window)

    # Draw color preview box on config screen
    if current_screen == "config_planet":
        radius_value_label.set_text(str(int(radius_slider.get_current_value())))
        mass_value_label.set_text(str(int(mass_slider.get_current_value())))
        color_button.show()
    else:
        color_button.hide()

    pygame.display.update()

pygame.quit()