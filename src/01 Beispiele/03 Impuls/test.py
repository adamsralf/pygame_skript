import math

import pygame

# Fenstergröße
WIDTH, HEIGHT = 800, 600

# Farben
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 50, 50)


# Ball-Klasse
class Ball:
    def __init__(self, x, y, vx, vy, radius, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.mass = radius  # Masse proportional zur Größe

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Wände prüfen
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx *= -1
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


def check_collision(b1, b2):
    dx = b2.x - b1.x
    dy = b2.y - b1.y
    distance = math.hypot(dx, dy)

    if distance < b1.radius + b2.radius:
        # Richtung normalisieren
        nx = dx / distance
        ny = dy / distance

        # Relative Geschwindigkeit
        dvx = b1.vx - b2.vx
        dvy = b1.vy - b2.vy

        # Geschwindigkeit entlang der Kollisionsachse
        dot = dvx * nx + dvy * ny
        if dot > 0:
            return  # Keine Kollision (sie entfernen sich)

        # Impulsübertragung (elastisch)
        impulse = (2 * dot) / (b1.mass + b2.mass)
        b1.vx -= impulse * b2.mass * nx
        b1.vy -= impulse * b2.mass * ny
        b2.vx += impulse * b1.mass * nx
        b2.vy += impulse * b1.mass * ny

        # Überlappung auflösen
        overlap = 0.5 * (b1.radius + b2.radius - distance + 1)
        b1.x -= overlap * nx
        b1.y -= overlap * ny
        b2.x += overlap * nx
        b2.y += overlap * ny


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kollision zweier Bälle")
    clock = pygame.time.Clock()

    # Zwei Bälle initialisieren
    ball1 = Ball(200, 300, 2, 1, 40, BLUE)
    ball2 = Ball(500, 300, -2, -1, 60, RED)

    running = True
    while running:
        clock.tick(60)  # 60 FPS
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ball1.move()
        ball2.move()
        check_collision(ball1, ball2)

        ball1.draw(screen)
        ball2.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
