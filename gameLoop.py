import pygame
import random

from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set FPS
FPS = 60
FrameClock = pygame.time.Clock()

# Declare colors
RED = pygame.Color(255, 0, 0)
BLACK = pygame.Color(0, 0, 0)

# Set up the main game window
SCREEN = pygame.display.set_mode((800, 640))
SCREEN.fill(BLACK)

class Block(pygame.sprite.Sprite):
    def __init__(self):
        # Define a surface for the Block
        self.surf = pygame.Surface((32,32))
        column = random.randint(1, 4)
        self.rect = self.surf.get_rect(center = (300+column*40, 100))

    def move(self):
        self.rect.move_ip(0, 16)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)
        

block1 = Block()
blocks = []
beatmap = []

# Read textfile
inFile = open("beatmaps/beatmap_complex.txt")
for line in inFile:
    #print(line)
    beatmap.append(float(line))

#for line in beatmap:
#    print(line)

time_passed = 0
next_onset = beatmap[0]
current_beat = 0

music = "crab_rave.wav"
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)

# Game loop
while True:
    time_passed += (1/FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    if time_passed >= next_onset:
        newBlock = Block()
        blocks.append(newBlock)
        current_beat += 1
        next_onset = beatmap[current_beat]
        
    
    SCREEN.fill(BLACK)

    

    for aBlock in blocks:
        aBlock.move()
        aBlock.draw(SCREEN)
    
    #block1.move()
    #block1.draw(SCREEN)
    

    pygame.display.update()

    # Wait for one frame-time unit to pass before continuing the game loop
    FrameClock.tick(FPS)
