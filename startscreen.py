
import pygame
import cv2
import os
import sys



pygame.init()

# design
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Fonts
TITLE_FONT_PATH = 'Resources/Marcellus-Regular.ttf'
TITLE_FONT = pygame.font.Font(TITLE_FONT_PATH, 72)
BUTTON_FONT = pygame.font.SysFont('arial', 36, bold=True)

#---------------------------------------------------

cap = cv2.VideoCapture("Resources/space.mp4")



# Function to display the start screen
def start_screen(screen, current_screen):

    screen_width, screen_height = screen.get_size()


    # Capture and display the video
    ret, frame = cap.read()
    if not ret:
        # If video ends, reset the capture to the start
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()  # Read the first frame again

    

    # Convert the frame from BGR (OpenCV format) to RGB (Pygame format)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.scale(frame, (screen_width, screen_height))
    screen.blit(frame, (0, 0))
    

    # Title
    title_text = TITLE_FONT.render('Rocket Adventure', True, WHITE)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(title_text, title_rect)

    # Buttons
    button_width, button_height = 200, 50
    start_button_rect = pygame.Rect((screen_width - button_width) // 2, (3 * screen_height) // 4, button_width, button_height)
    how_to_play_button_rect = pygame.Rect((screen_width - button_width) // 2, (3 * screen_height) // 4 + 60, button_width, button_height)

    # Draw buttons
    pygame.draw.rect(screen, BLACK, start_button_rect)
    pygame.draw.rect(screen, BLACK, how_to_play_button_rect)

    # Button text
    start_button_text = BUTTON_FONT.render('Start', True, WHITE)
    how_to_play_button_text = BUTTON_FONT.render('How to Play', True, WHITE)
    screen.blit(start_button_text, start_button_text.get_rect(center=start_button_rect.center))
    screen.blit(how_to_play_button_text, how_to_play_button_text.get_rect(center=how_to_play_button_rect.center))

    pygame.display.update()

    # Event handling for button clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(mouse_x, mouse_y):
                current_screen[0] = 1  # Switch to GAME_SCREEN
            elif how_to_play_button_rect.collidepoint(mouse_x, mouse_y):
                current_screen[0] = 2  # Switch to HOW_TO_PLAY_SCREEN
    
    
    