from time import time

import pygame
import pygame.time


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (120, 650))
    FPS = 300  # 10 30 60 120 240 300 600
    LIMIT = 500
    DELTATIME = 1.0 / FPS


def main():
    pygame.init()
    window = pygame.Window(size=Settings.WINDOW.size, title="Bewegung", position=(10, 50))
    screen = window.get_surface()
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_rect = pygame.rect.FRect(defender_image.get_rect())
    defender_rect.centerx = Settings.WINDOW.centerx
    defender_rect.bottom = Settings.WINDOW.height - 5
    defender_speed = 600
    defender_direction_v = -1

    start_time = pygame.time.get_ticks()
    time_previous = time()  # Startzeit festhalten§\label{srcInvader05i01}§
    running = True
    while running:
        if pygame.time.get_ticks() > start_time + Settings.LIMIT:
            defender_speed = 0
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender_rect.top += defender_direction_v * defender_speed * Settings.DELTATIME
        if defender_rect.bottom >= Settings.WINDOW.height:
            defender_direction_v *= -1
        elif defender_rect.top <= 0:
            defender_direction_v *= -1

        # Draw
        screen.fill("white")
        pygame.draw.line(screen, "red", (0, 315), (Settings.WINDOW.width, 315), 2)
        screen.blit(defender_image, defender_rect)
        window.flip()
        clock.tick(Settings.FPS)
        time_current = time()  # Aktuelle Zeit festhalten§\label{srcInvader05i02}§
        Settings.DELTATIME = time_current - time_previous  # Zeitverbrauche§\label{srcInvader05i03}§
        time_previous = time_current  # Neue Startzeit§\label{srcInvader05i04}§
    pygame.quit()


if __name__ == "__main__":
    main()
