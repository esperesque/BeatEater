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

    beats = []
    current_beat = 0
    next_beat = 0
    #path = "nothing.txt"

    def __init__(self, path):
        inFile = open(path)
        for line in inFile:
            self.beats.append(float(line))

    def progress(self, time):
        if time >= self.current_beat:
            newBlock = Block(0)
            blocks.append(newBlock)
            self.current_beat = self.beats[self.next_beat]
            self.next_beat += 1

class Block(pygame.sprite.Sprite):

    color = RED
    position = 0
    
    def __init__(self, position):
        # Define a surface for the Block
        self.surf = pygame.Surface((64,256))
        if position == 0:
            self.color = RED
        if position == 1:
            self.color = GREEN
        if position == 2:
            self.color = BLUE
        column = random.randint(1, 3)
        self.rect = self.surf.get_rect(center = ((position*300)+column*40, 0))

    def move(self):
        self.rect.move_ip(0, 64)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        

#block1 = Block()

#beatmap_bass = []
#beatmap_mid = []
#beatmap_treb = []

# Set music
music = "brink.wav"
#pygame.mixer.music.load(music)

# Divide into frequency bands
bsplit.bandSplit(music)

# Generate beatmaps
bmap.generateBeatmap("music_bass.wav", "hfc", "bassMap.txt")
bmap.generateBeatmap("music_mid.wav", "hfc", "midMap.txt")
bmap.generateBeatmap("music_treb.wav", "hfc", "trebMap.txt")

bassMap = Beatmap("beatmaps/trebMap.txt")
beatmaps = []
beatmaps.append(bassMap)

# Read textfile
#inFile = open("beatmaps/bassMap.txt")
#for line in inFile:
    #print(line)
#    beatmap_bass.append(float(line))

#inFile2 = open("beatmaps/midMap.txt")
#for line in inFile2:
#    beatmap_mid.append(float(line))

#inFile3 = open("beatmaps/trebMap.txt")
#for line in inFile3:
#    beatmap_treb.append(float(line))

time_passed = 0
#next_onset_bass = beatmap_bass[0]
#next_onset_mid = beatmap_mid[0]
#next_onset_treb = beatmap_treb[0]
#current_beat_bass = 0
#current_beat_mid = 0
#current_beat_treb = 0

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
        

    #if time_passed >= next_onset_bass:
    #    newBlock = Block(0)
    #    blocks.append(newBlock)
    #    current_beat_bass += 1
    #    next_onset_bass = beatmap_bass[current_beat_bass]

    #if time_passed >= next_onset_mid:
    #    newBlock = Block(1)
    #    blocks.append(newBlock)
    #    current_beat_mid += 1
    #    next_onset_mid = beatmap_mid[current_beat_mid]    

    #if time_passed >= next_onset_treb:
    #    newBlock = Block(2)
    #    blocks.append(newBlock)
    #    current_beat_treb += 1
    #    next_onset_treb = beatmap_treb[current_beat_treb]    
    
    SCREEN.fill(BLACK)

    

    for aBlock in blocks:
        aBlock.move()
        aBlock.draw(SCREEN)
    
    #block1.move()
    #block1.draw(SCREEN)
    

    pygame.display.update()

    # Wait for one frame-time unit to pass before continuing the game loop
    FrameClock.tick(FPS)
