import pygame


class Settings:
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 400
    FPS = 60
    ALIENS_NOF = 7


def main():
    pygame.init()
    window = pygame.Window(
        size=(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT), 
        title="Load and Draw of Bitmaps", 
        position=(10, 50))
    screen = window.get_surface()
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_pos_left = (Settings.WINDOW_WIDTH - 30) // 2   # Left coordinate§\label{srcInvader0401}§
    defender_pos_top = Settings.WINDOW_HEIGHT - 30 - 5      # Top coordinate§\label{srcInvader0402}§
    defender_pos = (defender_pos_left, defender_pos_top)    # Create a 2-tuple§\label{srcInvader0403}§

    alien_image = pygame.image.load("images/alienbig0101.png").convert_alpha()
    alien_image = pygame.transform.scale(alien_image, (50, 45))
    space_for_aliens = Settings.ALIENS_NOF * 50             # Space occupied by aliens§\label{srcInvader0405}§
    space_availible = Settings.WINDOW_WIDTH - space_for_aliens  # Remaining available space§\label{srcInvader0406}§
    space_nof = Settings.ALIENS_NOF + 1                     # Number of gaps§\label{srcInvader0407}§
    space_between_aliens = space_availible // space_nof     # Space per gap §\label{srcInvader0408}§

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")
        alien_top = 10                                      # Distance from top§\label{srcInvader0409}§
        for i in range(Settings.ALIENS_NOF):                # Compute and draw positions§\label{srcInvader0410}§
            alien_left = (i + 1) * space_between_aliens + i * 50
            alien_pos = (alien_left, alien_top)
            screen.blit(alien_image, alien_pos)
        screen.blit(defender_image, defender_pos)           # Draw defender at its position§\label{srcInvader0404}§
        window.flip()
        clock.tick(Settings.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
