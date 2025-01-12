# screens.py
#Handles the rendering of game screen
# screens.py

import pygame
import random
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
import os
import sys
from startscreen import *
pygame.init()


# Define colors
PINK = (255, 182, 193)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Button Font
BUTTON_FONT = pygame.font.SysFont('arial', 36, bold=True)

def game_screen(screen, current_screen):
    os.chdir(r"D:\asus\OneDrive\Documents\book\year4sem1\Machine_Vision\ProjectGame")

    width, height = 1280, 720
    # Images and sounds for the Balloon Pop game
    imgBalloon = pygame.image.load(r'./Resources/star.png').convert_alpha()
    # Resize the image to a smaller size, e.g., 40x40 pixels
    imgBalloon = pygame.transform.scale(imgBalloon, (40, 40))
    spaceship_img = pygame.image.load(r'./Resources/ufo.png').convert_alpha()
    spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))  # Resize spaceship image as needed


    imgJumpscare = pygame.image.load(r'./Resources/HD-wallpaper-cute-puppy-lovely-adorable-sweet-dog-face-cute-graphy-paws-puppies-face-eyes-animals-dogs-puppy-dog.jpg').convert_alpha()
    imgJumpscare = pygame.transform.scale(imgJumpscare, (width, height))

    bgMusic = pygame.mixer.Sound(r'./Resources/Elevator Music (Kevin MacLeod) - Background Music (HD).mp3')
    jumpscareSound = pygame.mixer.Sound(r'./Resources/Sad Trombone - Sound Effect (HD).mp3')
    font = pygame.font.Font('./Resources/Marcellus-Regular.ttf', 50)

    #--------------------------------------------

   
    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        exit()
    cap.set(3, 640)  # Set fixed width (e.g., 640)
    cap.set(4, 480)  # Set fixed height (e.g., 480)

    # hand detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)  #ori 0.8

    # music
    bgMusic.play(-1, 0, 5000)

    # Get the window size
    window_width, window_height = screen.get_size()

    #------------------------------------------------------------
    
    #-----------------------------------------------

    # Balloon Reset Function
    def resetBalloon():
        rectBalloon.x = random.randint(100, 640 - 100)
        rectBalloon.y = height + 50

    score = 0
    level = 1
    speed = 10
    targetScore = 10
    startTime = time.time()
    totalTime = 60
    timeRemain = totalTime
    balloonPopped = False

    rectBalloon = imgBalloon.get_rect()
    resetBalloon()

    

    # Main game loop for the second page (Balloon Pop)
    is_paused = False  # Track the pause state
    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    cap.release()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Toggle pause with the spacebar
                        is_paused = not is_paused
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Check if "Home" button is clicked
                    if home_button_rect.collidepoint(mouse_x, mouse_y):
                        running = False  # Exit the game screen to go back to the previous page
                        current_screen[0] = 0
                        
            

            timeRemain = int(totalTime - (time.time() - startTime))

            if timeRemain <= 0:
                if score < targetScore:
                    screen.fill((0, 0, 0))
                    screen.blit(imgJumpscare, (0, 0))
                    pygame.display.update()
                    bgMusic.stop()
                    jumpscareSound.play()
                    pygame.time.wait(3000)
                    level = 1
                    score = 0
                    speed = 10
                    targetScore = 10
                    startTime = time.time()
                    totalTime = 60
                    balloonPopped = False
                    bgMusic.play(-1, 0, 5000)

                else:
                    screen.fill((255, 255, 255))
                    textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
                    textLevel = font.render(f'Level {level} Complete!', True, (50, 50, 255))
                    screen.blit(textScore, (450, 350))
                    screen.blit(textLevel, (450, 275))
                    pygame.display.update()
                    pygame.time.wait(2000)
                    level += 1
                    score = 0
                    speed += 5
                    targetScore += 5
                    startTime = time.time()
                    totalTime = 60
                    balloonPopped = False

            else:
                success, img = cap.read()
                if not success:
                    print("Warning: No frame received from the webcam.")
                    continue

                img = cv2.flip(img, 1)

                # Convert the frame to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Apply edge detection (Canny algorithm)
                edges = cv2.Canny(gray, 100, 200)
                # Convert the edges image to a format compatible with Pygame
                edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)


                # Add purple lines to a black background where edges are detected
                black_background = np.zeros_like(edges_rgb)  # Create a black RGB image
                # Add random stars
                #for _ in range(100):  # Number of stars
                #    x = random.randint(0, black_background.shape[1] - 1)
                #    y = random.randint(0, black_background.shape[0] - 1)
                #    black_background[y, x] = [255, 255, 255]  # White star

                black_background[np.where(edges > 0)] = [138, 43, 226]  # Set color for edge pixels



                hands, img = detector.findHands(img, flipType=False)




                rectBalloon.y -= speed
                if rectBalloon.y < 0:
                    resetBalloon()
                    balloonPopped = False

                # Initialize spaceship_rect to a default position (or any other safe value)
                spaceship_rect = spaceship_img.get_rect(center=(window_width // 2, window_height // 2))

                # Define a proximity threshold (radius) for balloon popping
                PROXIMITY_THRESHOLD = 30

                if hands:
                    hand = hands[0]
                    x, y = hand['lmList'][8][0:2]

                    # Get the spaceship rect based on the finger position
                    spaceship_rect = spaceship_img.get_rect(center=(x, y))  # Position spaceship at finger tip

                    
                    # Calculate the distance between the fingertip and the balloon's center
                    balloon_center_x, balloon_center_y = rectBalloon.center
                    distance = ((x - balloon_center_x) ** 2 + (y - balloon_center_y) ** 2) ** 0.5

                    # this code is for, if the distance between finger and star in range, then balloon pop
                    cv2.circle(black_background, (x, y), PROXIMITY_THRESHOLD, (0, 140, 255), -1)  # orange circle of proximity
                    if distance <= PROXIMITY_THRESHOLD and not balloonPopped:
                    #if rectBalloon.collidepoint(x, y) and not balloonPopped:
                        resetBalloon()
                        score += 1
                        balloonPopped = True

                imgRGB = cv2.cvtColor(black_background, cv2.COLOR_BGR2RGB)
                imgRGB = np.rot90(imgRGB)
                frame = pygame.surfarray.make_surface(imgRGB).convert()
                frame = pygame.transform.flip(frame, True, False)

                #additional-------------------------------
                # Get the window size
                window_width, window_height = screen.get_size()

                # Calculate the camera feed's size and position
                feed_width, feed_height = frame.get_size()
                x_pos = (window_width - feed_width) // 2
                y_pos = (window_height - feed_height) // 2

                # Fill the background with orange
                #screen.fill((255, 165, 0))  # Orange background
                draw_gradient_background(screen, (0, 4, 40), (0, 78, 146))  # Dark blue to blue gradient

               
                # Create a surface to combine the webcam feed and the balloon
                combined_surface = pygame.Surface((feed_width, feed_height))

                # Blit the OpenCV frame (camera feed) onto the combined surface
                combined_surface.blit(frame, (0, 0))

                # Blit the balloon image on top of the webcam feed (combined surface)
                combined_surface.blit(imgBalloon, rectBalloon)  

                # Draw a glowing effect around the spaceship
                pygame.draw.circle(combined_surface, (0, 255, 255), spaceship_rect.center, 40, 4)  # Cyan glow
                combined_surface.blit(spaceship_img, spaceship_rect.topleft)

                # Now blit the combined surface onto the screen
                screen.blit(combined_surface, (x_pos, y_pos))

                textScore = font.render(f'Score: {score}', True, (255, 215, 0))
                textTime = font.render(f'Time: {timeRemain}', True, (0, 255, 255))
                textTargetScore = font.render(f'Goal: {targetScore}', True, (255, 69, 0))
                
                
                # Place the text outside the camera feed area
                screen.blit(textScore, (feed_width + 10 +  x_pos , 35))
                screen.blit(textTime, (feed_width + 10 +  x_pos , 100))
                screen.blit(textTargetScore, (feed_width + 10 +  x_pos , 165))



            # Draw the "Home" button
            button_width, button_height = 200, 50
            home_button_rect = pygame.Rect(window_width - button_width - 20, window_height - button_height - 20, button_width, button_height)
            pygame.draw.rect(screen, (47, 79, 79), home_button_rect)
            home_button_text = BUTTON_FONT.render('Home', True, (255, 255, 255))
            screen.blit(home_button_text, home_button_text.get_rect(center=home_button_rect.center))


            pygame.display.update()
            clock.tick(fps)

    except KeyboardInterrupt:
        print("Game interrupted. Exiting...")

    finally:
        cap.release()
        bgMusic.stop()



def draw_gradient_background(screen, top_color, bottom_color):
    width, height = screen.get_size()
    for y in range(height):
        color = [
            top_color[i] + (bottom_color[i] - top_color[i]) * y // height
            for i in range(3)
        ]
        pygame.draw.line(screen, color, (0, y), (width, y))
