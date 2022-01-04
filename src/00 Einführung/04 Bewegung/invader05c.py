import pygame
import os


class Settings:
    window = {'width':600, 'height':100}
    fps = 60
    @staticmethod
    def window_dim():
        return (Settings.window['width'], Settings.window['height'])


if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode(Settings.window_dim())
    pygame.display.set_caption("Bewegung")
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_rect = defender_image.get_rect()              
    defender_rect.centerx = Settings.window['width'] // 2  
    defender_rect.bottom = Settings.window['height'] - 5   
    defender_speed = 2                                      
    defender_direction_h = 1                                

    running = True
    while running:
        clock.tick(Settings.fps)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender_rect.left += defender_direction_h * defender_speed 
        if defender_rect.right >= Settings.window['width']: # Rechter Rand erreicht§\label{srcInvader0508}§
            defender_direction_h *= -1                      # Richtungswechsel§\label{srcInvader0509}§
        elif defender_rect.left <= 0:                       # Linker Rand erreicht
            defender_direction_h *= -1
        
        # Draw
        screen.fill((255, 255, 255))
        screen.blit(defender_image, defender_rect)         
        pygame.display.flip()

    pygame.quit()
