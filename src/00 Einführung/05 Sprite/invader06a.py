import pygame
import os


class Settings:
    window = {'width': 600, 'height': 100}
    fps = 60

    @staticmethod
    def window_dim():
        return (Settings.window['width'], Settings.window['height'])



class Defender(pygame.sprite.Sprite):               # Kindklasse von Sprite §\label{srcInvader0601}§

    def __init__(self) -> None:                     # Konstruktor §\label{srcInvader0602}§
        super().__init__()
        self.image = pygame.image.load("images/defender01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = Settings.window['width'] // 2
        self.rect.bottom = Settings.window['height'] - 5
        self.speed = 2
        self.direction = 1

    def update(self) -> None:                       # Zustandsberechnung §\label{srcInvader0603}§
        newpos = self.rect.move(self.direction * self.speed, 0)
        if newpos.right >= Settings.window['width']:
            self.change_direction()
        elif newpos.left <= 0:
            self.change_direction()
        else:
            self.rect = newpos

    def draw(self, screen) -> None:                 # Malen §\label{srcInvader0604}§
        screen.blit(self.image, self.rect)

    def change_direction(self) -> None:             # OO style §\label{srcInvader0608}§
            self.direction *= -1



if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode(Settings.window_dim())
    pygame.display.set_caption("Sprite")
    clock = pygame.time.Clock()
    defender = Defender()                           # Objekt anlegen §\label{srcInvader0605}§

    running = True
    while running:
        clock.tick(Settings.fps)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender.update()                           # Aufruf §\label{srcInvader0606}§

        # Draw
        screen.fill((255, 255, 255))
        defender.draw(screen)                       # Aufruf §\label{srcInvader0607}§
        pygame.display.flip()

    pygame.quit()
