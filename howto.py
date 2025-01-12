import pygame
import sys
pygame.init()

# Define colors
PINK = (255, 182, 193)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Button Font
BUTTON_FONT = pygame.font.SysFont('arial', 36, bold=True)

def how_to_play_screen(screen, current_screen):
    # Get the screen size
    window_width, window_height = screen.get_size()

    # Fill the screen with a pink color
    screen.fill(PINK)

    #//////////////////////////
    # Header: "HOW TO PLAY?"
    header_font = pygame.font.SysFont('arial', 48, bold=True)
    header_text = header_font.render('HOW TO PLAY?', True, BLACK)
    header_rect = header_text.get_rect(center=(window_width // 2, 100))
    screen.blit(header_text, header_rect)

    # Subtext: "That's part of the challenge! All the best figuring them out."
    subtext_font = pygame.font.SysFont('arial', 32)
    subtext_text = subtext_font.render("That's part of the challenge!", True, BLACK)
    subtext_rect = subtext_text.get_rect(center=(window_width // 2, 180))
    screen.blit(subtext_text, subtext_rect)

    subtext_text2 = subtext_font.render("All the best figuring them out.", True, BLACK)
    subtext_rect2 = subtext_text2.get_rect(center=(window_width // 2, 220))
    screen.blit(subtext_text2, subtext_rect2)

    # Divider line
    pygame.draw.line(screen, BLACK, (50, 260), (window_width - 50, 260), 2)

    # Credits: "CREDITS"
    credits_header_font = pygame.font.SysFont('arial', 36, bold=True)
    credits_header_text = credits_header_font.render("CREDITS:", True, BLACK)
    credits_header_rect = credits_header_text.get_rect(center=(window_width // 2, 300))
    screen.blit(credits_header_text, credits_header_rect)

    # Credits content: sources
    credits_font = pygame.font.SysFont('arial', 28)
    credits_lines = [
        "- song: Space Unicorn by Parry Gripp",
        "- Ufo: Ufo icons created by Freepik - Flaticon",
        "- Star: Star icons created by Freepik - Flaticon"
    ]
    line_spacing = 35
    for i, line in enumerate(credits_lines):
        line_text = credits_font.render(line, True, BLACK)
        line_rect = line_text.get_rect(topleft=(60, 350 + i * line_spacing))
        screen.blit(line_text, line_rect)

    #///////////////////
    # Create the "Home" button at the bottom right
    button_width, button_height = 200, 50
    home_button_rect = pygame.Rect(window_width - button_width - 20, window_height - button_height - 20, button_width, button_height)
    
    # Draw the "Home" button
    pygame.draw.rect(screen, BLACK, home_button_rect)
    home_button_text = BUTTON_FONT.render('Home', True, WHITE)
    screen.blit(home_button_text, home_button_text.get_rect(center=home_button_rect.center))

    # Update the display
    pygame.display.update()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if the "Home" button is clicked
            if home_button_rect.collidepoint(mouse_x, mouse_y):
                current_screen[0] = 0  # Change to START_SCREEN
                
            

    