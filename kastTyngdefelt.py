import pygame, sys, math

pygame.init()

FPS = 60 # bilder per sekund
fpsClock = pygame.time.Clock()

# setter opp vinduet
screen = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Kast i tyngdefelt')

farge_svart = (0, 0, 0)
farge_hvit = (255, 255, 255)

#variabler
dt = 0.05
m = 1
g = 9.8
k = 0.2

x = 0
y = 300

vinkel = 45
theta = math.radians(vinkel)

v = 100
vx = v * math.cos(theta)
vy = -v * math.sin(theta)

while True:
    screen.fill(farge_svart)

    fx = -k*vx
    fy = m*g - k*vy

    vx = vx + (fx / m) * dt
    vy = vy + (fy / m) * dt

    x = x + vx * dt
    y = y + vy * dt

    pygame.draw.circle(screen, farge_hvit, (int(x), int(y)), 5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)

