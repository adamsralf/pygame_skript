import os
from math import cos, pi, sin
from random import randint, random
from time import time
from typing import Any, Dict

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT, K_h


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (400, 200))
    PATH: Dict[str, str] = {}
    PATH["file"] = os.path.dirname(os.path.abspath(__file__))
    PATH["image"] = os.path.join(PATH["file"], "images")
    FPS = 60
    DELTATIME = 1.0/FPS
    NOFBALLS = 10
    HIDDENLINES = True


class Ball(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        fullfilename = os.path.join(Settings.PATH["image"], "blue2.png")
        self.image_orig = pygame.image.load(fullfilename).convert_alpha()
        self._scale = randint(10, 50)
        self.image = pygame.transform.smoothscale(self.image_orig, (self._scale, self._scale))
        self.rect = self.image.get_rect()
        self.radius = self._scale // 2
        self.masse = self._scale * self._scale * pi
        self._winkel = random() * 2.0 * pi
        impuls = randint(50, 100)
        self.geschwindigkeit = pygame.math.Vector2()
        self.geschwindigkeit.x = impuls * sin(self._winkel)
        self.geschwindigkeit.y = impuls * -cos(self._winkel)
        self.position = pygame.math.Vector2()
        self.randomposition()
        self.position2rect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self.position += (self.geschwindigkeit * Settings.DELTATIME)
                self.position2rect()
            if self.rect.right >= Settings.WINDOW.right:
                self.rect.right = Settings.WINDOW.right - 1
                self.position2rect(True)
                self.geschwindigkeit.x *= -1
            if self.rect.left <= Settings.WINDOW.left:
                self.rect.left = Settings.WINDOW.left + 1
                self.position2rect(True)
                self.geschwindigkeit.x *= -1
            if self.rect.top <= Settings.WINDOW.top:
                self.rect.top = Settings.WINDOW.top + 1
                self.position2rect(True)
                self.geschwindigkeit.y *= -1
            if self.rect.bottom >= Settings.WINDOW.bottom:
                self.rect.bottom = Settings.WINDOW.bottom - 1
                self.position2rect(True)
                self.geschwindigkeit.y *= -1
            if -1.0 < self.geschwindigkeit.x < 1.0:
                self.geschwindigkeit.x = 2
            if -1.0 < self.geschwindigkeit.y < 1.0:
                self.geschwindigkeit.y = 2

    def draw_values(self, screen):
        pygame.draw.line(screen, "red", self.position, self.position + self.geschwindigkeit)

    def position2rect(self, reverse: bool = False):
        if not reverse:
            self.rect.centerx = round(self.position.x)
            self.rect.centery = round(self.position.y)
        else:
            self.position.x = self.rect.centerx
            self.position.y = self.rect.centery

    def randomposition(self):
        self.position.x = randint(Settings.WINDOW.left+self._scale, Settings.WINDOW.right-self._scale)
        self.position.y = randint(Settings.WINDOW.top+self._scale, Settings.WINDOW.bottom-self._scale)


def my_sign(x) -> int:
    if x < 0.0:
        return -1
    else:
        return 1


def kreiskollision(ball1: Ball, ball2: Ball) -> Dict:
    abstand = ball2.position.distance_to(ball1.position)
    return {"kollision": abstand <= ball1.radius + ball2.radius, "abstand": abstand}


def simulate_collision(ball1: Ball, ball2: Ball):
    # Calculate the distance between the balls
    normvector = ball1.position - ball2.position
    zustand = kreiskollision(ball1, ball2)
    abstand = zustand["abstand"]
    kollidiert = zustand["kollision"]

    # Check if the balls are colliding
    if kollidiert:
        # Überlappung der beiden Kugeln
        überlappung = 2.0 + (ball1.radius + ball2.radius) - abstand
        länge = normvector.length()
        ü = pygame.Vector2()
        ü.x = (überlappung/länge * normvector.x) / 2.0
        ü.y = (überlappung/länge * normvector.y) / 2.0
        ball1.position += ü
        ball2.position -= ü
        ball1.position2rect()
        ball2.position2rect()

        # Store the current velocities of the balls
        v1 = pygame.Vector2(ball1.geschwindigkeit) * Settings.DELTATIME
        v2 = pygame.Vector2(ball2.geschwindigkeit) * Settings.DELTATIME

        # Calculate the new velocities of the balls after the collision
        ball1.geschwindigkeit.x = ((v1.x * (ball1.masse - ball2.masse) + 2 * ball2.masse * v2.x) / (ball1.masse + ball2.masse)) / Settings.DELTATIME
        ball1.geschwindigkeit.y = ((v1.y * (ball1.masse - ball2.masse) + 2 * ball2.masse * v2.y) / (ball1.masse + ball2.masse)) / Settings.DELTATIME
        ball2.geschwindigkeit.x = ((v2.x * (ball2.masse - ball1.masse) + 2 * ball1.masse * v1.x) / (ball1.masse + ball2.masse)) / Settings.DELTATIME
        ball2.geschwindigkeit.y = ((v2.y * (ball2.masse - ball1.masse) + 2 * ball1.masse * v1.y) / (ball1.masse + ball2.masse)) / Settings.DELTATIME


class Game:

    def __init__(self) -> None:
        os.environ["SDL_VIDEO_WINDOW_POS"] = "650, 70"
        pygame.init()
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(Settings.WINDOW.size)
        self._background = pygame.surface.Surface(Settings.WINDOW.size)
        self._background.fill("grey")
        pygame.display.set_caption("Impuls")
        self._all_balls = pygame.sprite.Group()
        for _ in range(Settings.NOFBALLS):
            self.add_ball()
        self._running = True

    def run(self) -> None:
        time_previous = time()
        while self._running:
            self.watch_for_events()
            self.update()
            self.draw()
            self._clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
                elif event.key == K_h:
                    Settings.HIDDENLINES = not Settings.HIDDENLINES
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.add_ball()
                elif event.button == 3:
                    self.remove_ball()

    def update(self):
        self._all_balls.update(action="move")
        for i in range(len(self._all_balls)-1):
            for j in range(i+1, len(self._all_balls)):
                simulate_collision(self._all_balls.sprites()[i], self._all_balls.sprites()[j])

    def draw(self) -> None:
        self._screen.blit(self._background, (0, 0))
        self._all_balls.draw(self._screen)
        if Settings.HIDDENLINES:
            for b in self._all_balls.sprites():
                b.draw_values(self._screen)
        pygame.display.update()

    def genugplatz(self, ball1: Ball, ball2: Ball) -> bool:
        abstand = ball2.position.distance_to(ball1.position)
        return abstand > ball1.radius + ball2.radius + 5

    def add_ball(self):
        ok = True
        ball = Ball()
        for b in self._all_balls.sprites():
            if not self.genugplatz(ball, b):
                ok = False
                break
        if ok:
            self._all_balls.add(ball)

    def remove_ball(self):
        if len(self._all_balls) > 0:
            self._all_balls.sprites()[0].kill()


def main():
    Game().run()


if __name__ == "__main__":
    main()

# https://www.physikerboard.de/topic,123,-kollision-von-2-kugeln.html
# Bei mir sah es so aus:
# mx1, mx2, my1 und my2 sind die Geschwindigkeitsvektoren vorher.
# nx1, nx2, ny1 und ny2 die hinterher.
# m1 und m2 sind die Massen.
# nx1=((m1-m2)*mx1+2*m2*mx2)/(m1+m2);
# ny1=((m1-m2)*my1+2*m2*my2)/(m1+m2);
# nx2=((m2-m1)*mx2+2*m1*mx1)/(m1+m2);
# ny2=((m2-m1)*my2+2*m1*my1)/(m1+m2);
