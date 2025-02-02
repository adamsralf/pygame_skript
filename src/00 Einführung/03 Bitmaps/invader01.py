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

    defender_image = pygame.image.load("images/defender01.png")  # Bitmap laden §\label{srcInvader0101}§
    enemy_image = pygame.image.load("images/alienbig0101.png")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")
        screen.blit(enemy_image, (10, 10))          # Bitmap ausgeben §\label{srcInvader0102}§
        screen.blit(defender_image, (10, 80))
        window.flip()
        clock.tick(Settings.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
