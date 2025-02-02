import pygame


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (600, 100))
    FPS = 60


def main():
    pygame.init()
    window = pygame.Window(size=Settings.WINDOW.size, title="Bewegung", position=(10, 50))
    screen = window.get_surface()
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_rect = defender_image.get_rect()
    defender_rect.centerx = Settings.WINDOW.centerx
    defender_rect.bottom = Settings.WINDOW.height - 5
    defender_speed = 2
    defender_direction_h = 1

    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender_rect.left += defender_direction_h * defender_speed
        if defender_rect.right >= Settings.WINDOW.right:  # Rechter Rand erreicht§\label{srcInvader0508}§
            defender_direction_h *= -1  # Richtungswechsel§\label{srcInvader0509}§
        elif defender_rect.left <= Settings.WINDOW.left:  # Linker Rand erreicht
            defender_direction_h *= -1

        # Draw
        screen.fill("white")
        screen.blit(defender_image, defender_rect)
        window.flip()
        clock.tick(Settings.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
