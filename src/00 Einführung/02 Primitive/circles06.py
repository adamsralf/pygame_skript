import os
from random import randint

import pygame


class Circle:
    gravity = 0.3
    radius_inc = -0.1                                       # Radiusinkrement§\label{srcCircles0600}§

    def __init__(self, pos) -> None:
        self.posx = pos[0] + randint(-4, 4)                 # Veränderte Streuung§\label{srcCircles0601}§
        self.posy = pos[1] + randint(-4, 4)
        self.radius = 8
        self.color = [randint(100, 255), randint(50, 255), 0]
        self.speedx = randint(-15, 15) / 10.01              # Fontaine breiter§\label{srcCircles0602}§
        self.speedy = randint(-100, 0) / 10.01
        self.todelete = False

    def update(self):
        self.speedy -= Circle.gravity
        self.posx += self.speedx
        self.posy += self.speedy
        self.radius += Circle.radius_inc
        if self.posx - self.radius < 0:
            self.todelete = True
        elif self.posx + self.radius > pygame.display.get_window_size()[0]:
            self.todelete = True
        elif self.posy - self.radius > pygame.display.get_window_size()[1]:
            self.todelete = True
        elif self.radius <= 0.0:                            # Können raus§\label{srcCircles0603}§
            self.todelete = True

    def draw(self):
        screen = pygame.display.get_surface()
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)


def main():
    size = (300, 600)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()
    pygame.display.set_caption('Partikelschwarm')
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    circles = []

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.mouse.get_pressed()[0]:
            for i in range(5):
                circles.append(Circle(pygame.mouse.get_pos()))

        todelete = []
        for p in circles:
            p.update()
            if p.todelete:
                todelete.append(p)
        for p in todelete:
            circles.remove(p)

        screen.fill("white")
        for p in circles:
            p.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
