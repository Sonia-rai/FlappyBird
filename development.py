
# Development of Flappy Bird Game under progess..

import random  # For generating random numbers
import sys   # We will use sys.exit to exit the program
import pygame
from pygame.locals import *   # Basic pygame imports
import time
import os

# Global variables for the game
FPS = 32        # Frames per second
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY =  SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.jpg'
PIPE = 'gallery/sprites/pipe.png'


# colours
black = (0, 0, 0)
white = (255, 255, 255)
green = (34, 139, 34)
blue = (64, 224, 208)
red = (255,0,0)
grey = (128,128,128)

def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx , playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()      #Note: Without this function screen won't blit and further game won't update 
                FPSCLOCK.tick(FPS)    
 
 
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
    
    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    
    # my List of Upper Pipes
    upperpipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']}
        ]                             
    # my List of Lower Pipes                             
    lowerpipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']}
        ]
    
    
    pipeVelX = -4
   
    playerVelY = -9 
    playerMaxVelY = 10 
    playerMinVelY = -8 
    playerAccY = 1 
    
    playerFlapAccv = -8  # velocity while flapping
    PlayerFlapped = False # It is true only when the bird is flapping
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT  or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery>0:
                    playerVelY = playerFlapAccv
                    PlayerFlapped = True
                    GAME_SOUNDS['wing'].play()
                          
        crashTest = isCollide(playerx,playery,upperpipes,lowerpipes) # This function will return true if the player is crashed
        
        if crashTest: 
            show_score(score)
            High_score(score)
            msg_surface('Game Over')
            
            return   
        
        
        #Check for score
        PlayerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<=PlayerMidPos<pipeMidPos+4:
                score+=1 
                GAME_SOUNDS['point'].play()   
        if playerVelY <playerMaxVelY and not PlayerFlapped: # when PlayerFlapped is True(not False)
            playerVelY += playerAccY
        
        if PlayerFlapped:
            PlayerFlapped = False  
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight) # selects minimum among both
        
        
        # move pipes too the left
        for upperpipe ,lowerPipe  in zip(upperpipes,lowerpipes):
            upperpipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
             
        # Add a new pipe when the first pipe is about to cross the leftmost part of the screen
        if 0<upperpipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])
                             
        #if the pipe is out of the screen, remove it    
        if lowerpipes[0]['x'] <-GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)            
         
    
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        
        for upperPipe, lowerPipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex ,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH-width)/2
        
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset,SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)    
                
def isCollide(playerx,playery,upperpipes,lowerpipes):
    if playery> GROUNDY - 25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerpipes:
        if(playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False   
     
        
def getRandomPipe():
    """
    Generating positions of two pipes (One bottom straight and one top rotated) for blitting on the screen  
    """
    pipeHeight =  GAME_SPRITES['pipe'][1].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - offset * 1.2))
    pipex = SCREENWIDTH + 10   # difference of distance between 4 (2-upperpipe and 2-lowerpipe) pipe with 4 other pipes
    y1 = pipeHeight - y2 + offset
    pipe=[
        {'x' : pipex , 'y' : -y1},  # Upper pipe[0] Pipe will be generated on screenwidth + 10 units 
        {'x' : pipex , 'y' :  y2}   # Lower pipe[1]
    ]
    return pipe

def makeTextObjs(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def show_score(current_score):
    textx = int(SCREENWIDTH/2)-70
    texty = int(SCREENHEIGHT/2)-20
    font = pygame.font.Font('freesansbold.ttf', 22)
    text = font.render('Your Score:' + str(current_score), True, black)
    SCREEN.blit(text, (textx, texty))

    pygame.display.update()
    return current_score
    
                   
def High_score(scores):

    highx = int(SCREENWIDTH/2)-70  # Highscore width i.e. x coordinate
    highy = int(SCREENHEIGHT/2)+20   # y coordinate
    highnx = int(SCREENWIDTH/2)-130                    # New Highscore width i.e. x coordinate
    highny = int (SCREENHEIGHT/2)+20                   # New Highscore height i.e. y coordinate
    font = pygame.font.Font('freesansbold.ttf', 22)
    font1 = pygame.font.Font('freesansbold.ttf', 22)
     
    # Creating a static file for saving the Highscores! 
    with open('Highscore.txt','r+') as f:
      try:
          highscore = int(f.read()) 
      except Exception as e:
          highscore = 0
          
    # Conditions for having Highscore      
    if highscore < scores:    
        highscore = scores
        with open('Highscore.txt','w') as f:
            f.write(str(scores))
        HIGHSCOREN = font1.render('Congras!NewHighscore:'+ str(scores), True, black)  
        SCREEN.blit(HIGHSCOREN, (highnx, highny))  
    else:
        highscore = highscore
        HIGHSCORE = font.render('High Score:'+ str(highscore), True, black) 
        SCREEN.blit(HIGHSCORE, (highx, highy))
   
    pygame.display.update()  
    
def msg_surface(text):
    '''
    This functions displays/blit the message to the screen
    '''
    
    smallText = pygame.font.Font('freesansbold.ttf',20)
    largeText = pygame.font.Font('freesansbold.ttf', 50)

    titletextSurf, titleTextRect = makeTextObjs(text, largeText)
    titleTextRect.center = (SCREENWIDTH / 2), (SCREENHEIGHT / 2)-80
    SCREEN.blit(titletextSurf, titleTextRect)

    #typtextSurf, typTextRect = makeTextObjs('Press any key to continue', smallText)
    #typTextRect.center = SCREENWIDTH / 2, ((SCREENHEIGHT/ 2) + 100)
    #SCREEN.blit(typtextSurf, typTextRect) 

    pygame.display.update()
    time.sleep(1)

    #while replay_or_quit() is None:
     #   FPSCLOCK.tick(FPS)
    welcomeScreen()
    mainGame()
    
    

if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init()  # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by SoniaRai')
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )
    
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    
    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame()  # This is the main game function 


      
