import pygame
import random
import scipy

from pygame.locals import *

import generateBeatmap as bmap
import bandSplit as bsplit

# Initialize Pygame
pygame.init()

# Set FPS
FPS = 60
FrameClock = pygame.time.Clock()

# Declare colors
RED = pygame.Color(255, 0, 0)
BLACK = pygame.Color(0, 0, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = pygame.Color(0, 255, 0)

# Set up the main game window
SCREEN = pygame.display.set_mode((800, 640))
SCREEN.fill(BLACK)

blocks = []

class Beatmap():

    def __init__(self, path, pos):
        self.beats = []
        self.current_beat = 0
        self.next_beat = 0
        self.position = pos
        
        inFile = open(path)
        for line in inFile:
            self.beats.append(float(line))
        inFile.close()

    def progress(self, time):
        if time >= self.current_beat:
            newBlock = Block(self.position)
            blocks.append(newBlock)
            self.current_beat = self.beats[self.next_beat]
            self.next_beat += 1

class Block(pygame.sprite.Sprite):

    color = RED
    position = 0
    
    def __init__(self, position):
        # Define a surface for the Block
        self.surf = pygame.Surface((32,32))
        if position == 0:
            self.color = RED
        if position == 1:
            self.color = GREEN
        if position == 2:
            self.color = BLUE
        column = random.randint(1, 4)
        self.rect = self.surf.get_rect(center = ((position*300)+column*40, 0))

    def move(self):
        self.rect.move_ip(0, 16)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Set music
music = "brink.wav"
#pygame.mixer.music.load(music)

# Divide into frequency bands
bsplit.bandSplit(music)

# Generate beatmaps
bmap.generateBeatmap("music_bass.wav", "hfc", "bassMap.txt")
bmap.generateBeatmap("music_mid.wav", "hfc", "midMap.txt")
bmap.generateBeatmap("music_treb.wav", "hfc", "trebMap.txt")

bassMap = Beatmap("beatmaps/bassMap.txt", 0)
midMap = Beatmap("beatmaps/midMap.txt", 1)
trebMap = Beatmap("beatmaps/trebMap.txt", 2)
beatmaps = []
beatmaps.append(bassMap)
beatmaps.append(midMap)
beatmaps.append(trebMap)

time_passed = 0

#music = "brink.wav"
pygame.mixer.music.load(music)
#pygame.mixer.music.play(-1)

music_started = 0

# Game loop
while True:
    time_passed += (1/FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    if music_started == 0:
        pygame.mixer.music.play(-1)
        music_started = 1

    for bmap in beatmaps:
        bmap.progress(time_passed)
    
    SCREEN.fill(BLACK)

    for aBlock in blocks:
        aBlock.move()
        aBlock.draw(SCREEN)

    pygame.display.update()

    # Wait for one frame-time unit to pass before continuing the game loop
    FrameClock.tick(FPS)
