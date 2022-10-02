import time

import pygame
import random
from pygame import mixer

while True:
    quit1 = None
    restart = None
    mixer.init() #initializes the music player
    mixer.music.load("Tetris.mp3") #loads the sound file into the mixer
    mixer.music.set_volume(0.0) #sets the volume of the music
    mixer.music.play() #starts playing the music
    pygame.init() #initializes pygame
    clock = pygame.time.Clock() #initializes clock object
    screenwidth = 500 #sets the width dimension of the screen
    screenheight = 700 #sets the height dimension of the screen
    screen = pygame.display.set_mode((screenwidth, screenheight)) #uses the previously initialized variables to create screen

    color = (0,0,195) #creating a color variable
    screen.fill(color) #filling the screen with the color
    pygame.display.flip() #alters whatever argument is passed; if no argument, it alters the entire screen


    fruit_img = pygame.image.load("banananana.png") #loads image in directory into variable
    background_img = pygame.image.load("pokemon bacgkround.jpg") #loads image in directory into variable



    class Player(pygame.sprite.Sprite): #creates a class for the player

        def __init__(self, scale): #base class which allows users to further add attributes
            pygame.sprite.Sprite.__init__(self) #same ^
            image = pygame.image.load("snorlaxx.png")
            width = image.get_width() #puts width of image into variable
            height = image.get_height() #puts height of image into variable
            self.image = pygame.transform.scale(image, (int(width * scale), int(height*scale))) # player takes up
            self.rect = self.image.get_rect() #hitbox
            self.rect.center = (250, 600) #starting location

        def update(self): #what happens when the game updates in 60 fps
            global quit1
            quit1 = False
            global restart
            restart = False
            keystate = pygame.key.get_pressed() #determines state of whether keys are being pressed down
            if keystate[pygame.K_UP]: #if the up key is being pressed
                self.rect.y -= 5 #move up 5, seems opposite because of the coordinate plane formatting in pygame
            elif keystate[pygame.K_DOWN]: #if down key is being pressed
                self.rect.y += 5 #move down five
            elif keystate[pygame.K_LEFT]: #if left arrow key,
                self.rect.x -= 10 #move left five
            elif keystate[pygame.K_RIGHT]: #if right arrow key,
                self.rect.x += 10 #move right five
            elif keystate[pygame.K_q]:
                quit1 = True
            elif keystate[pygame.K_SPACE]:
                restart = True


    player = Player(.13) #calls player to a variable
    player_group = pygame.sprite.Group() #creates a group named players
    player_group.add(player) #adds created player to the group

    class Enemy(pygame.sprite.Sprite): #creates enemy class

        def __init__(self, image, scale): #base class
            pygame.sprite.Sprite.__init__(self) #attribute for enemy
            width = image.get_width() #puts width of image into variable
            height = image.get_height() #puts height into variable
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))) #transforms the image to scale
            self.rect = self.image.get_rect() #hitbox
            self.rect.center = (random.randint(50, 450), random.randint(-15000,-200)) #spawn location


        def update(self): #for each frame,
            self.rect.y += 10 #moves down 10


    enemy_group = pygame.sprite.Group() #creates enemy group
    for i in range(50): #repeats 50 times
        exec(f"enemy{i}=Enemy(fruit_img, .2)") #execute, it reads the string as a normal command
        exec(f"enemy_group.add(enemy{i})") #the command adds the created enemies to a group

    points = 0 #creates variable to keep track of points
    misses = 0 #creates variable to keep track of misses

    class bar(pygame.sprite.Sprite): #creates class for bar at the bottom of the screen

        def __init__(self): #base class
            pygame.sprite.Sprite.__init__(self) #attributes =
            self.image = pygame.Surface((450, 5)) #size dimensions
            self.image.fill((255, 255, 255)) #color
            self.rect = self.image.get_rect() #draw it
            self.rect.center = (250, 650) #location

    Bar = bar() #calls bar class and sets into variable
    bar_group = pygame.sprite.Group() #creates bar group
    bar_group.add(Bar) #adds created bar to group

    class Text(): #creates text class
        def __init__(self, surface, text, size, color, x, y): #class hierarchy with no arguments in properties of the class
            font_name = pygame.font.match_font('arial') #font name, uses one of pygames fonts
            self.surface = surface #changeable size
            self.text = text #changeable content
            self.size = size #changeable size
            self.font = pygame.font.Font(font_name, self.size) #changeable font
            self.color = color #changeable color
            self.x = x #x coord
            self.y = y # y coord
        def draw(self): #defines action
            text_surface = self.font.render(self.text, True, self.color)  #if its true, renders the font in that color
            text_rect = text_surface.get_rect() #renders text
            text_rect.midtop = (self.x, self.y) #location?
            self.surface.blit(text_surface, text_rect) #blits text over screen

    rectangle = pygame.image.load("rectangle.jpg") #loads image of rectangle into pygame

    count = 0 #sets count to 0
    while True: #game loop
        font = pygame.font.SysFont(None, 24) #base detailing for font class
        for event in pygame.event.get(): #if this happens
            if event.type == quit: #if it says quit
                 pygame.quit() #quit
                 quit()

        screen.blit(background_img, (-500, 0)) #blits background image to specific location
        point_label = font.render(f"score: {points}", True, (255, 255, 255)) #keeps track of points in corner, and dictates color
        screen.blit(point_label, (20, 20)) #location of point tracker
        directions = font.render("Use the arrow keys to move the white square.", True, (255, 255, 255)) #text which states directions, color
        screen.blit(directions, (75, 660)) #location of directions
        miss_label = font.render(f"misses: {misses}", True, (255, 255, 255)) #text that counts misses
        screen.blit(miss_label, (410, 20)) #location of misses
        instructions = font.render("Press \"q\" to quit.     Press Space to restart.", True, (255, 255, 255))  # text that counts misses
        screen.blit(instructions, (85, 680))  #


        #player_group.draw(screen) #creates screen
        player_group.update() #updates the screen
        if quit1 == True:
            pygame.display.quit()
            pygame.quit()

        if restart == True:
            pygame.display.quit()
            pygame.quit()
            break

        screen.blit(player.image, player.rect)
        hit_list = pygame.sprite.spritecollide(player, enemy_group, True) #if player and enemy group collide,
        for hit in hit_list: #for each collision added to the list above
            points +=1 #add one point
            print(points) #print points in console(?)

        enemy_group.draw(screen) #draws enemies
        enemy_group.update() #updates enemy group, causes them to move down

        bar_group.draw(screen) #draws bar onto screen

        miss_list = pygame.sprite.spritecollide(Bar, enemy_group, True) #for each miss: when the enemy hits the bar,
        for miss in miss_list: #for each contact as listed above
            misses += 1 #add one to misses
            print(misses) #print into console

        if points + misses >= 50: #when points and misses = 50 (total amount of enemies)
            font = pygame.font.SysFont(None, 50) #enlargens font
            img = font.render("GAME OVER!", True, (255, 0, 0)) #sets text to GAME OVER! and the color
            screen.blit(img, (140, 20)) #blits the text over the center of the screen
            font = pygame.font.SysFont(None, 20)

            subtitle = font.render(f"Game will restart in {5-int(count/60)} seconds", True, (0, 0, 0))
            screen.blit(subtitle, (150, 60))
            #screen.blit(point_label, (205, 115)) #blits points under (on y-axis) game over
            #screen.blit(miss_label, (205, 130)) #blits misses under (on y-axis) game over
            if count >= 300: #after game over,
                #time.sleep(3) #sleep program for 5 seconds
                break
            count += 1
        pygame.display.update()  # updates everytime it changes
        pygame.display.flip()

        clock.tick(60) #fps

pygame.quit() #automatically quit the game
quit()