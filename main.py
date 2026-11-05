import math
import random

import pygame
import sys

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 1080, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)

pygame.display.set_caption("breathing")

# Define the font and track the score variable
# Passing None uses the default Pygame system font; 36 is the font size
score_font = pygame.font.Font(None, 36)
score_value = 0

# Game Over Stuff
end_font = pygame.font.Font(None, 72)
game_ove_ind = False

# Circle settings
circle_color = (0, 150, 255)
circle_pos = (WIDTH // 2, HEIGHT // 2)
circle_pox = WIDTH // 2
circle_poy = HEIGHT // 2
player_x_vec = 0
player_y_vec = 0
radius = 50
min_radius = 10
max_radius = 300
radius_step = 2

# Player input settings
flagMouseLeftClick = False
flagMouseRightClick = False
flagMouseClick = False

# Enemy settings
enemy_color = (75, 200, 130)
enemy_pox = WIDTH
enemy_poy = HEIGHT
enemy_pos = (enemy_pox, enemy_poy)
enemy_radius = 10
enemy_x_vec = 0
enemy_y_vec = 0

#timer to increase difficulty over time
timer = 0
timer_divide = 100



clock = pygame.time.Clock()

class Button:
    def __init__(self, text, x, y, width, height, normal_color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.normal_color = normal_color
        self.hover_color = hover_color

        # Initialize the font and render the text
        self.font = pygame.font.SysFont("Arial", 24)
        self.text_surf = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        # 1. Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # 2. Change color if hovering
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.normal_color

        # 3. Draw the button rectangle and text
        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, event):
        # 4. Check if the mouse clicked within the button area
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


def main():
    global radius
    running = True
    score_value = 0
    flagMouseLeftClick = False
    flagMouseRightClick = False
    circle_pox = WIDTH // 2
    circle_poy = HEIGHT // 2
    enemy_x_vec = random.randint(-5, 0)
    enemy_y_vec = random.randint(-5, 0)
    player_x_vec = 0
    player_y_vec = 0
    enemy_pox = WIDTH
    enemy_poy = HEIGHT
    game_ove_ind = False
    timer = 1
    backgroundTimer = 1

    while running:
        clock.tick(60)  # Limit to 60 FPS
        timer += 100/(timer +1)
        print (timer/timer_divide)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    flagMouseLeftClick = True
                elif event.button == 3:
                    flagMouseRightClick = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    flagMouseLeftClick = False
                elif event.button == 3:
                    flagMouseRightClick = False

            keys = pygame.key.get_pressed()
            if not keys[pygame.K_a]:
                player_x_vec = 0
            if not keys[pygame.K_d]:
                player_x_vec = 0
            if not keys[pygame.K_w]:
                player_y_vec = 0
            if not keys[pygame.K_s]:
                player_y_vec = 0

            if keys[pygame.K_w]:
                player_y_vec = -3
            if keys[pygame.K_a]:
                player_x_vec = -3
            if keys[pygame.K_s]:
                player_y_vec = 3
            if keys[pygame.K_d]:
                player_x_vec = 3




        if flagMouseLeftClick or flagMouseRightClick:
            # Left click (1) - expand
            if flagMouseLeftClick:
                radius = min(radius + radius_step, max_radius)
            # Right click (3) - shrink
            elif flagMouseRightClick:
                radius = max(radius - radius_step, min_radius)
        # Shrink slowly if nothing is clicked
        else:
            radius = max(radius - radius_step/4, min_radius)

        score_value += (math.sqrt(radius) + 1)/40

        # Enemy Movement
        enemy_pox += enemy_x_vec
        enemy_poy += enemy_y_vec

        # Checks if out of bounds
        if enemy_pox >= WIDTH:
            enemy_pox = WIDTH
            enemy_x_vec = random.randint(-int(timer/timer_divide), 0)
            enemy_y_vec = random.randint(-int(timer/timer_divide), int(timer/timer_divide))
        elif enemy_pox <= 0:
            enemy_pox = 0
            enemy_x_vec = random.randint(0, int(timer/timer_divide))
            enemy_y_vec = random.randint(-int(timer/timer_divide), int(timer/timer_divide))
        if enemy_poy >= HEIGHT:
            enemy_poy = HEIGHT
            enemy_y_vec = random.randint(-int(timer/timer_divide), 0)
            enemy_x_vec = random.randint(-int(timer/timer_divide), int(timer/timer_divide))
        elif enemy_poy <= 0:
            enemy_poy = 0
            enemy_y_vec = random.randint(0, int(timer/timer_divide))
            enemy_x_vec = random.randint(-int(timer/timer_divide), int(timer/timer_divide))

        if enemy_x_vec in {1, 2, 3}:
            enemy_x_vec = 4
        if enemy_x_vec in {-1, -2, -3}:
            enemy_x_vec = -4
        if enemy_y_vec in {1, 2, 3}:
            enemy_y_vec = 4
        if enemy_y_vec in {-1, -2, -3}:
            enemy_y_vec = -4


        # Player Movement
        circle_pox += player_x_vec
        circle_poy += player_y_vec
        # Checks if out of bounds
        if circle_pox > WIDTH:
            circle_pox = WIDTH
        elif circle_pox < 0:
            circle_pox = 0
        if circle_poy > HEIGHT:
            circle_poy = HEIGHT
        elif circle_poy < 0:
            circle_poy = 0

        # Set enemy and player position
        enemy_pos = (enemy_pox, enemy_poy)
        circle_pos = (circle_pox, circle_poy)

        # Check for collision
        center_distance = math.dist(circle_pos, enemy_pos)
        edge_distance = center_distance - (radius + enemy_radius)
        if edge_distance <= 0:
            game_ove_ind = True
            running = True

        while game_ove_ind:
            clock.tick(60)  # Limit to 60 FPS
            my_button = Button("PLAY AGAIN", WIDTH - 200, HEIGHT  -100, 160, 60, (50, 120, 200), (70, 150, 240))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_ove_ind = False
                    running = False


                # Trigger an action if the button is clicked
                if my_button.is_clicked(event):
                    running = True
                    score_value = 0
                    flagMouseLeftClick = False
                    flagMouseRightClick = False
                    circle_pox = WIDTH // 2
                    circle_poy = HEIGHT // 2
                    enemy_x_vec = random.randint(-5, 0)
                    enemy_y_vec = random.randint(-5, 0)
                    player_x_vec = 0
                    player_y_vec = 0
                    enemy_pox = WIDTH
                    enemy_poy = HEIGHT
                    radius = 50
                    timer = 1
                    game_ove_ind = False


            # Drawing
            SCREEN.fill((30, 30, 30))  # Background color
            score_text = score_font.render(f"Score: {int(score_value)}", True, (255, 255, 255))
            SCREEN.blit(score_text, (20, 20))
            end_text = score_font.render(f"GAME OVER", True, (255, 255, 255))
            SCREEN.blit(end_text, (WIDTH - 500, 20))
            # Draw the button to the screen
            my_button.draw(SCREEN)
            pygame.display.flip()


        # Drawing
        SCREEN.fill((30, 30, 30))  # Background color
        # Render the score text
        # Arguments: text string, antialiasing (True), RGB text color (White)
        score_text = score_font.render(f"Score: {int(score_value)}", True, (255, 255, 255))
        # Draw (blit) the rendered text surface onto the screen at (x, y) coordinates
        SCREEN.blit(score_text, (20, 20))
        # Draw Player
        pygame.draw.circle(SCREEN, circle_color, circle_pos, radius)
        # Draw Enemy
        pygame.draw.circle(SCREEN, enemy_color, enemy_pos, enemy_radius)


        pygame.display.flip()



    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


