import pygame
import random
import math

WIDTH, HEIGHT = 1200, 900
N_BOIDS = 200
FPS = 60

VISION_RADIUS = 100
VISION_ANGLE = math.radians(120)
SEPARATION_DIST = 25
K_NEIGHBORS = 6

MAX_SPEED = 4
MAX_FORCE = 0.05

COHESION_W = 0.005
ALIGNMENT_W = 0.05
SEPARATION_W = 0.15

boids = []

for _ in range(N_BOIDS):
    pos = pygame.Vector2(
        random.uniform(0, WIDTH),
        random.uniform(0, HEIGHT)
    )
    angle = random.uniform(0, 2 * math.pi)
    vel = pygame.Vector2(math.cos(angle), math.sin(angle)) # cos za oś X, sin za oś Y
    vel.scale_to_length(random.uniform(1, MAX_SPEED))
    boids.append({"pos": pos, "vel": vel})


def get_neighbors(i):
    neighbors = []
    boid = boids[i]

    for j, other in enumerate(boids):
        if i == j:
            continue

        distance = boid["pos"].distance_to(other["pos"])
        if distance < VISION_RADIUS:
            direction = (other["pos"] - boid["pos"]).normalize()
            if boid["vel"].normalize().dot(direction) > math.cos(VISION_ANGLE / 2):
                neighbors.append((other, distance))
    neighbors.sort(key=lambda x: x[1]) # Sort by distance
    return neighbors[:K_NEIGHBORS]

def cohesion(i):
    somsiad = get_neighbors(i)
    if not somsiad:
        return pygame.Vector2(0, 0)

    center = sum((b["pos"] for b, _ in somsiad), pygame.Vector2(0, 0)) / len(somsiad)
    return center - boids[i]["pos"]

def alignment(i):
    somsiad = get_neighbors(i)
    if not somsiad:
        return pygame.Vector2(0, 0)

    avg_vel = sum((b["vel"] for b, _ in somsiad), pygame.Vector2(0, 0)) / len(somsiad)
    return avg_vel - boids[i]["vel"]

def separation(i):
    force = pygame.Vector2(0, 0)
    for boid, distance in get_neighbors(i):
        if distance < SEPARATION_DIST:
            wektor_do_sasiada = boid["pos"] - boids[i]["pos"]
            kierunek_do_sasiada = wektor_do_sasiada.normalize()
            force = force - kierunek_do_sasiada
    return force

def wrap(pos):
    if pos.x < 0: pos.x = WIDTH
    if pos.x > WIDTH: pos.x = 0
    if pos.y < 0: pos.y = HEIGHT
    if pos.y > HEIGHT: pos.y = 0



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids")
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((20, 20, 30))

    for i, boid in enumerate(boids):
        accel = (
            cohesion(i) * COHESION_W +
            alignment(i) * ALIGNMENT_W +
            separation(i) * SEPARATION_W
        )

        if accel.length() > MAX_FORCE:
            accel.scale_to_length(MAX_FORCE)

        boid["vel"] += accel
        if boid["vel"].length() > MAX_SPEED:
            boid["vel"].scale_to_length(MAX_SPEED)

        boid["pos"] += boid["vel"]
        wrap(boid["pos"])

        angle = math.atan2(boid["vel"].y, boid["vel"].x)
        p1 = boid["pos"] + pygame.Vector2(12, 0).rotate_rad(angle)
        p2 = boid["pos"] + pygame.Vector2(-8, 5).rotate_rad(angle)
        p3 = boid["pos"] + pygame.Vector2(-8, -5).rotate_rad(angle)

        pygame.draw.polygon(screen, (255, 255, 255), [p1, p2, p3])

    pygame.display.flip()

pygame.quit()
