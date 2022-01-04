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
        # Vereinfacht §\label{srcInvader0609}§
        self.rect.move_ip(self.direction * self.speed, 0)

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

    def change_direction(self) -> None:
        self.direction *= -1


class Border(pygame.sprite.Sprite):

    def __init__(self, leftright) -> None:
        super().__init__()
        self.image = pygame.image.load("images/brick01.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (35, Settings.window['height']))
        self.rect = self.image.get_rect()
        if leftright == 'right':
            self.rect.left = Settings.window['width'] - self.rect.width

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