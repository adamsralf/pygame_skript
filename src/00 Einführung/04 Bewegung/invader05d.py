import pygame
import os


class Settings:
    window = {'width':600, 'height':100}
    fps = 5
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
    defender_speed = defender_rect.width                                      
    defender_direction_h = 1                                

    running = True
    while running:
        clock.tick(Settings.fps)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        newpos = defender_rect.move(defender_direction_h * defender_speed, 0) # Testposition §\label{srcInvader0510}§
        if newpos.right >= Settings.window['width']: 
            defender_direction_h *= -1                      
        elif newpos.left <= 0:                       
            defender_direction_h *= -1
        else:
            defender_rect = newpos              # Übernehme neue Position §\label{srcInvader0511}§
        
        # Draw
        screen.fill((255, 255, 255))
        screen.blit(defender_image, defender_rect)         
        pygame.display.flip()

    pygame.quit()
