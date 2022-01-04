import pygame
import os


class Settings:
    window = {'width': 600, 'height': 100}
    fps = 60

    @staticmethod
    def window_dim():
        return (Settings.window['width'], Settings.window['height'])


class Defender(pygame.sprite.Sprite):

    def __init__(self) -> None:      
        super().__init__()
        self.image = pygame.image.load("images/defender01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = Settings.window['width'] // 2
        self.rect.bottom = Settings.window['height'] - 5
        self.speed = 2
        self.direction = 1

    def update(self) -> None:           
        self.rect.move_ip(self.direction * self.speed, 0)  # Vereinfacht §\label{srcInvader0609}§

    def draw(self, screen) -> None:     
        screen.blit(self.image, self.rect)

    def change_direction(self) -> None: 
            self.direction *= -1



class Border(pygame.sprite.Sprite):

    def __init__(self, leftright) -> None:
        super().__init__()
        self.image = pygame.image.load("images/brick01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, Settings.window['height']))
        self.rect = self.image.get_rect()
        if leftright == 'right':
            self.rect.left = Settings.window['width'] - self.rect.width
 
    def update(self) -> None:
        pass




if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode(Settings.window_dim())
    pygame.display.set_caption("Sprite")
    clock = pygame.time.Clock()
    defender = pygame.sprite.GroupSingle(Defender())
    all_border = pygame.sprite.Group()
    all_border.add(Border('left'))
    all_border.add(Border('right'))

    running = True
    while running:
        clock.tick(Settings.fps)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        if pygame.sprite.spritecollide(defender.sprite, all_border, False): # ! §\label{srcInvader0611}§
            defender.sprite.change_direction()
        defender.update()    

        # Draw
        screen.fill((255, 255, 255))
        defender.draw(screen)                      
        all_border.draw(screen)                 # Mit einem Rutsch §\label{srcInvader0610}§
        pygame.display.flip()

    pygame.quit()
