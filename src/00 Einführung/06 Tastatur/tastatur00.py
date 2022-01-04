import pygame
import os


class Settings:
    window = {'width': 150, 'height': 150}
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
        self.rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2) # Zentrum §\label{srcTastatur0001}§
        self.direction = (0, 0)                         # 2 Dimensionen §\label{srcTastatur0002}§
        self.start()
        self.move_right()

    def update(self) -> None:
        self.rect.move_ip(self.direction[0] * self.speed, self.direction[1] * self.speed)

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

    def move_right(self) -> None:
        self.direction = (1, 0)

    def move_left(self) -> None:
        self.direction = (-1, 0)

    def move_up(self) -> None:
        self.direction = (0, -1)

    def move_down(self) -> None:
        self.direction = (0, 1)

    def stop(self) -> None:
        self.speed = 0

    def start(self) -> None:
        self.speed = 2

    def change_direction(self) -> None:
        self.direction = (self.direction[0] * -1, self.direction[1] * -1)




class Border(pygame.sprite.Sprite):

    def __init__(self, whichone) -> None:
        super().__init__()
        self.image = pygame.image.load("images/brick01.png").convert_alpha()
        if whichone == 'right':
            self.image = pygame.transform.scale(self.image, (10, Settings.window['height']))
            self.rect = self.image.get_rect()
            self.rect.left = Settings.window['width'] - self.rect.width
        elif whichone == 'left':
            self.image = pygame.transform.scale(self.image, (10, Settings.window['height']))
            self.rect = self.image.get_rect()
            self.rect.left = 0
        elif whichone == 'top':
            self.image = pygame.transform.scale(self.image, (Settings.window['width'], 10))
            self.rect = self.image.get_rect()
            self.rect.top = 0
        elif whichone == 'down':
            self.image = pygame.transform.scale(self.image, (Settings.window['width'], 10))
            self.rect = self.image.get_rect()
            self.rect.bottom = Settings.window['height']

    def update(self) -> None:
        pass


class Game(object):

    def __init__(self) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.window_dim())
        pygame.display.set_caption("Sprite")
        self.clock = pygame.time.Clock()
        self.defender = pygame.sprite.GroupSingle(Defender())
        self.all_border = pygame.sprite.Group()
        self.all_border.add(Border('left'))
        self.all_border.add(Border('right'))
        self.all_border.add(Border('top'))
        self.all_border.add(Border('down'))
        self.running = False

    def run(self) -> None:
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:          # Taste drücken §\label{srcTastatur0003}§
                if event.key == pygame.K_ESCAPE:        # Boss-Taste §\label{srcTastatur0004}§
                    self.running = False
                elif event.key == pygame.K_RIGHT:       # Pfeiltasten §\label{srcTastatur0005}§
                    self.defender.sprite.move_right()
                elif event.key == pygame.K_LEFT:
                    self.defender.sprite.move_left()
                elif event.key == pygame.K_UP:
                    self.defender.sprite.move_up()
                elif event.key == pygame.K_DOWN:
                    self.defender.sprite.move_down()
                elif event.key == pygame.K_SPACE:       # Leerzeichen-Taste §\label{srcTastatur0006}§
                    self.defender.sprite.stop()
                elif event.key == pygame.K_r:
                    if event.mod & pygame.KMOD_LSHIFT:  # Shift-Taste §\label{srcTastatur0007}§
                        self.defender.sprite.stop()
                    else: 
                        self.defender.sprite.start()


    def update(self) -> None:
        if pygame.sprite.spritecollide(self.defender.sprite, self.all_border, False):
            self.defender.sprite.change_direction()
        self.defender.update()

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        self.defender.draw(self.screen)
        self.all_border.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()