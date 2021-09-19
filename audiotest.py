import pygame
import random
import demo_bpm_extract
import aubio

from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set FPS
FPS = 60
FrameClock = pygame.time.Clock()

# Declare colors
#RED = pygame.Color(255, 0, 0)
#GREEN = pygame.Color(0, 255, 0)
#BLUE = pygame.Color(0, 0, 255)
#BLACK = pygame.Color(0, 0, 0)
#WHITE = pygame.Color(255, 255, 255)
#CORNFLOWER = pygame.Color(100, 149, 237)

# Set up the main game window
DISPLAYSURF = pygame.display.set_mode((640, 512))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Audiosurf 3")

class Block(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((32, 32))
        self.rect = self.surf.get_rect(center = (random.randint(0, 640), 0))

    def move(self):
        self.rect.move_ip(0, 8)
        #if (self.rect.top > 670):
        #    self.rect.center = (random.randint(0, 640), 0)

    def draw(self, surface):
        afterglow = self.rect.move(0, -96)
        pygame.draw.rect(surface, (10, 0, 0), afterglow)
        afterglow = self.rect.move(0, -80)
        pygame.draw.rect(surface, (20, 0, 0), afterglow)
        afterglow = self.rect.move(0, -64)
        pygame.draw.rect(surface, (40, 0, 0), afterglow)
        afterglow = self.rect.move(0, -48)
        pygame.draw.rect(surface, (60, 0, 0), afterglow)
        afterglow = self.rect.move(0, -32)
        pygame.draw.rect(surface, (80, 0, 0), afterglow)
        afterglow = self.rect.move(0, -16)
        pygame.draw.rect(surface, (100, 0, 0), afterglow)
        
        pygame.draw.rect(surface, RED, self.rect)

class Enemy(pygame.sprite.Sprite):

    row = 0
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("asprite.bmp")
        self.surf = pygame.Surface((32, 32))
        self.rect = self.surf.get_rect(center = (16, 16))

    def move(self):
        self.rect.move_ip(32,0)
        if (self.rect.right > 640):
            self.rect.right = 32
            self.row += 1
            self.rect.top = 32*self.row
            if(self.rect.bottom > 512):
                self.rect.top = 0
                self.row = 0
        #self.rect.move_ip(0,10)
        #if (self.rect.bottom > 600):
        #    self.rect.top = 0
        #    self.rect.center = (random.randint(30, 370), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        #pygame.draw.rect(DISPLAYSURF, RED, self.rect)

#E1 = Enemy()
B1 = Block()

# Set up music and detect BPM

music = "85_bpm.wav"
bpm = demo_bpm_extract.get_file_bpm(music)

# onset testing

win_s = 512
hop_s = win_s // 2
samplerate = 0

s = aubio.source(music, samplerate, hop_s)
samplerate = s.samplerate

ons = aubio.onset("default", win_s, hop_s, samplerate)

onsets = []

total_frames = 0
while True:
    samples, read = s()
    if ons(samples):
        #print("beat")
        onsets.append(ons.get_last())
    total_frames += read
    if read < hop_s: break

print(len(onsets))
print(onsets[0])
print(onsets[1])
print(onsets[2])
# Attempt to filter


#source = aubio.source(music)
#samplerate = source.samplerate
#print(source.samplerate)
#samplerate = 16000 #industrial mode

#filtr = aubio.digital_filter(3)
#filtr.set_biquad(1.00232158, -1.92154676, 0.92253521, -1.92172674, 0.92467681)
#filtr.set_a_weighting(96000)

# Create output file
#out = aubio.sink("music5.wav", samplerate)

#total_frames = 0
#while True:
#    # read from source
#    samples, read = source()
#    filtered_samples = filtr(samples)
#    # write
#    out(filtered_samples, read)
#    # count frames
#    total_frames += read
#    # end of file
#    if read < source.hop_size:
#        break

#out.close()

#music = "music5.wav"
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)

print("The BPM is " + str(bpm))

bps = bpm / 60
cycle_time = FPS / bps
cycle = 0

waiting_for = onsets[0]
samples_passed = 0
current_beat = 0

fallingBlocks = []

while True: # Game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            #exit()

    if samples_passed >= waiting_for:
        newBlock = Block()
        fallingBlocks.append(newBlock)
        current_beat += 1
        if(current_beat >= len(onsets)):
           current_beat = 0
           samples_passed = 0
        waiting_for = onsets[current_beat]

    samples_passed += samplerate / FPS

    #B1.move()

    #cycle += 1
    #if(cycle >= cycle_time):
    #    E1.move()
    #    cycle = 0

    

    DISPLAYSURF.fill(BLACK)

    for obj in fallingBlocks:
        obj.move()
        obj.draw(DISPLAYSURF)
    
    #E1.draw(DISPLAYSURF)
    #B1.draw(DISPLAYSURF)

    pygame.display.update()
    FrameClock.tick(FPS)
