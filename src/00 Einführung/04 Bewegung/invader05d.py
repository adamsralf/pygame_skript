import os

import pygame


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (600, 100))
    FPS = 5


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode(Settings.WINDOW.size)
    pygame.display.set_caption("Bewegung")
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_rect = defender_image.get_rect()
    defender_rect.centerx = Settings.WINDOW.centerx
    defender_rect.bottom = Settings.WINDOW.height - 5
    defender_speed = defender_rect.width
    defender_direction_h = 1

    running = True
    while running:
        clock.tick(Settings.FPS)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        newpos = defender_rect.move(defender_direction_h * defender_speed, 0)  # Testposition §\label{srcInvader0510}§
        if newpos.right >= Settings.WINDOW.right:
            defender_direction_h *= -1
        elif newpos.left <= Settings.WINDOW.left:
            defender_direction_h *= -1
        else:
            defender_rect = newpos              # Übernehme neue Position §\label{srcInvader0511}§

        # Draw
        screen.fill("white")
        screen.blit(defender_image, defender_rect)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
