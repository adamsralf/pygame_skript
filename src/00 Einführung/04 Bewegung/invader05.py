import pygame


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (600, 100))           # Rect-Objekt §\label{srcInvader0504a}§
    FPS = 60


def main():
    pygame.init()
    window = pygame.Window(
        size=Settings.WINDOW.size,                          # Zugriff auf ein Rect-Attribut §\label{srcInvader0504b}§
        title="Bewegung", 
        position=(10, 50))
    screen = window.get_surface()
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_rect = defender_image.get_rect()               # Rect-Objekt §\label{srcInvader0501}§
    defender_rect.centerx = Settings.WINDOW.centerx         # Nicht nur left §\label{srcInvader0502}§
    defender_rect.bottom = Settings.WINDOW.height - 5       # Nicht nur top §\label{srcInvader0503}§

    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update

        # Draw
        screen.fill("white")
        screen.blit(defender_image, defender_rect)          # blit kann auch rect §\label{srcInvader0504}§
        window.flip()
        clock.tick(Settings.FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
