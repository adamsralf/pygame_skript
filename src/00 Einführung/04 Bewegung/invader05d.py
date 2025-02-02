import pygame


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (600, 100))
    FPS = 5


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
    defender_speed = defender_rect.width
    defender_direction_h = 1

    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        newpos = defender_rect.move(defender_direction_h * defender_speed, 0)  # Testposition §\label{srcInvader0510}§
        if newpos.right >= Settings.WINDOW.right:
            defender_direction_h *= -1
            newpos.right = Settings.WINDOW.right  # Ausrichten am rechten Rand
        elif newpos.left <= Settings.WINDOW.left:
            defender_direction_h *= -1
            newpos.left = Settings.WINDOW.left  # Ausrichten am linken Rand
        defender_rect = newpos  # Übernehme neue Position §\label{srcInvader0511}§

        # Draw
        screen.fill("white")
        screen.blit(defender_image, defender_rect)
        window.flip()
        clock.tick(Settings.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
