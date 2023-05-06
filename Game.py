import pygame
import random
import time

screen = pygame.display.set_mode((1080, 720))

pygame.font.init()
# set up the font
font = pygame.font.SysFont(None, 64)

# create the text surface
text_surface = font.render("You Died", True, (139, 0, 0, 1))

# get the dimensions of the text surface
text_rect = text_surface.get_rect()

# center the text surface on the screen
text_rect.center = (screen.get_width() / 2, screen.get_height() / 2)
# pygame setup\npygame.init()

pygame.display.set_caption("MAZE Game")
clock = pygame.time.Clock()
running = True
dt = 0.009

player1_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player2_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Random x position and y position for the rectangle
xRand = random.randint(1, screen.get_width())
yRand = random.randint(1, screen.get_height())

#Keep track of when the game started, so wwe can see how many seconds elapsed
start = time.perf_counter()

#Time for the levels in seconds:
timeLevel1 = 30
timeLevel2 = 60
Level1 = False
Level2 = False
speed = 3
level = 0
randXArray = []
firstRUN = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    #Generates this array once
    while firstRUN == True:
        firstRUN = False
        for i in range(6):
            x = random.randint(1, screen.get_width())
            randXArray.append(x)
            print(randXArray)

    
    #This is your player
    player1 = pygame.draw.circle(screen, "green", player1_pos, 20)
    #player2 = pygame.draw.circle(screen, "blue",player2_pos, 20)

    #Timing
    current = time.perf_counter()
    time_elapsed = current - start

    rectArray = []

    #If user hasn't reached level 1, normal speed for rectangles
    if time_elapsed < timeLevel1:
        for i in range(level+3):
            rectangle_obs = pygame.draw.rect(screen,"red", (randXArray[i], yRand, 60, 120))
            rectArray.append(rectangle_obs)
        yRand += speed
        time_remaining = str(round(30 - time_elapsed,0))
        screen.blit(font.render(time_remaining, True, (255, 255, 255)),(10, 10))

    #If he has, then speed them up
    if time_elapsed >= timeLevel1 and Level2 ==False:
        level = 1
        for i in range(level+3):
            rectangle_obs = pygame.draw.rect(screen,"red", (randXArray[i], yRand, 60, 120))
            rectArray.append(rectangle_obs)
        speed = 4
        #first time around, prompt user
        if Level1 == False:
            screen.blit(font.render("Level 1", True, "white"), text_rect)
            pygame.display.update()
            pygame.time.wait(500)
            Level1 = True

        #time remaining thing
        time_remaining = str(round(30 - time_elapsed+60,0))
        screen.blit(font.render(time_remaining, True, (255, 255, 255)),(10, 10))
        yRand += speed

    #Reached level 2
    if time_elapsed >= timeLevel2:
        level = 2
        for i in range(level+3):
            rectangle_obs = pygame.draw.rect(screen,"red", (randXArray[i], yRand, 60, 120))
            rectArray.append(rectangle_obs)
        speed = 6
        if Level2 == False:
            screen.blit(font.render("Level 2", True, "white"), text_rect)
            pygame.display.update()
            pygame.time.wait(500)
            Level2 = True
        
        #time remaining thing
        yRand+= speed
        time_remaining = str(round(30 - time_elapsed+90,0))
        screen.blit(font.render(time_remaining, True, (255, 255, 255)),(10, 10))
        

    # If the rectangle goes off the screen, then give it a random x position at the top of the screen
    if yRand > screen.get_height():
        for i in range(level + 1):
            x = random.randint(1, screen.get_width())
            randXArray[i] = x
            print(randXArray)
        yRand = 0

    # determine if the space bar is held down
    slow_motion = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        slow_motion = True

    # sets delta and the yRand to slow down time
    if slow_motion:
        dt = 0.0045
        yRand-= speed*0.5
    else:
        dt = 0.009

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if player1_pos.y > 0:
            player1_pos.y -= 500 * dt
    if keys[pygame.K_s]:
        if player1_pos.y < screen.get_height():
            player1_pos.y += 500 * dt
    if keys[pygame.K_a]:
        if player1_pos.x > 0:
            player1_pos.x -= 500 * dt
    if keys[pygame.K_d]:
        if player1_pos.x < screen.get_width():
            player1_pos.x += 500 * dt

    
    for i in rectArray:
        print("rectangle:" + str(i))
        #Checks for a collions between player and enemy, user dies
        if (player1.colliderect(i)):
            screen.blit(text_surface, text_rect)
            pygame.display.update()
        
            #Reset the start time, so he has to last the full amount to get to the level
            start = time.perf_counter()

            xRand = random.randint(1, screen.get_width())

            pygame.time.wait(500)

            #reset their coordinates
            player1_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
            #player2_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    

    # flip() the display to put your work on screen
    pygame.display.flip()
    pygame.display.update()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(120) / 1000

pygame.quit()

#Solution I think:
#Just store the coordinates of the rectangle and then put that into the collision system