import pygame


class Settings:
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 400
    FPS = 60


def main():
    pygame.init()
    window = pygame.Window(
        size=(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT), 
        title="Bitmaps laden und ausgeben", 
        position=(10, 50))
    screen = window.get_surface()
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()  # §\label{srcInvader0301}§
    defender_image = pygame.transform.scale(defender_image, (30, 30))

    enemy_image = pygame.image.load("images/alienbig0101.png").convert()
    enemy_image.set_colorkey("black")               # Transparenzfarbe setzen§\label{srcInvader0302}§
    enemy_image = pygame.transform.scale(enemy_image, (50, 45))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")
        screen.blit(enemy_image, (10, 10))
        screen.blit(defender_image, (10, 80))
        window.flip()
        clock.tick(Settings.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
