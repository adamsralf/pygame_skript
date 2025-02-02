from random import randint

import pygame


class Circle:
    def __init__(self, pos) -> None:
        self.posx = pos[0] + randint(-2, 2)
        self.posy = pos[1] + randint(-2, 2)
        self.radius = 2
        self.color = [randint(100, 255), randint(50, 255), 0]

    def draw(self, screen: pygame.surface.Surface) -> None:
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)


def main():
    size = (300, 600)
    pygame.init()
    window = pygame.Window( size=size, title = "Partikelschwarm", position = (10, 50))         
    screen = window.get_surface()                   
    clock = pygame.time.Clock()
    circles = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.mouse.get_pressed()[0]:           # Linke Maustaste?§\label{srcCircles0105}§
            circles.append(Circle(pygame.mouse.get_pos()))

        screen.fill("white")
        for p in circles:
            p.draw(screen)

        window.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
