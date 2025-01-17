import pygame
import sys
from howto import *
from screens import game_screen 
from startscreen import *

import os


#---------------------------------------------------
# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Rocket Adventure')
#---------------------------------------------------

# Define screen states
START_SCREEN = 0
GAME_SCREEN = 1
HOW_TO_PLAY_SCREEN = 2

# Initial screen state (mutable reference)
current_screen = [START_SCREEN]  # Use a list to allow modification in functions

# Load and start background music for long tracks
pygame.mixer.music.load('Resources/space_unicorn.mp3')

# Play the music indefinitely
pygame.mixer.music.set_volume(0.1)  # Set music volume (optional)

def start_music():
    """Start music for Start Screen and How to Play Screen"""
    pygame.mixer.music.play(-1, 0.0)  # Play music indefinitely starting from 0 seconds

def stop_music():
    """Stop music for Game Screen"""
    pygame.mixer.music.stop()

#---------------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Check the current screen state and control music accordingly
    if current_screen[0] == START_SCREEN:
        if not pygame.mixer.music.get_busy():  # Start music if not already playing
            start_music()
        start_screen(screen, current_screen)  # Pass current_screen as a mutable argument
    elif current_screen[0] == GAME_SCREEN:
        stop_music()  # Stop music when switching to the game screen
        game_screen(screen, current_screen)
    elif current_screen[0] == HOW_TO_PLAY_SCREEN:
        if not pygame.mixer.music.get_busy():  # Start music if not already playing
            start_music()
        how_to_play_screen(screen, current_screen)
