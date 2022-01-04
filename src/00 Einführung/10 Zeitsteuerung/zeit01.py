import pygame
import os


class Settings(object):
    window = {'width':700, 'height':200}
    fps = 60
    title = "Zeitsteuerung"
    path = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "images")
    directions = {'stop':(0, 0), 'down':(0,  1), 'up':(0, -1), 'left':(-1, 0), 'right':(1, 0)} # §\label{srcZeit0001}§

    @staticmethod
    def dim():
        return (Settings.window['width'], Settings.window['height'])

    @staticmethod
    def filepath(name):
        return os.path.join(Settings.path['file'], name)

    @staticmethod
    def imagepath(name):
        return os.path.join(Settings.path['image'], name)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(Settings.imagepath(filename)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)
        self.direction = Settings.directions['right']
        self.speed = 1

    def update(self):
        self.rect.move_ip([self.speed*x for x in self.direction])
        if self.rect.left < 10:
            self.direction = Settings.directions['right']
        elif self.rect.right >= Settings.window['width'] - 10:
            self.direction = Settings.directions['left']


class Bullet(pygame.sprite.Sprite):
    def __init__(self, picturefile) -> None:
        super().__init__()
        self.image = pygame.image.load(Settings.imagepath(picturefile)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (10, 10)
        self.direction = Settings.directions['down']
        self.speed = 2

    def update(self):
        self.rect.move_ip([self.speed*x for x in self.direction])
        if self.rect.top > Settings.window['height'] - 30:
            self.kill()



class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        pygame.display.set_caption(Settings.title)
        self.screen = pygame.display.set_mode(Settings.dim())
        self.clock = pygame.time.Clock()
        self.enemy = pygame.sprite.GroupSingle(Enemy("alienbig1.png"))
        self.all_bullets = pygame.sprite.Group()
        self.time_counter = 0                           # Zähler§\label{srcZeit0101}§
        self.time_range = 30                            # Obergrenze§\label{srcZeit0102}§ 
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)                         
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw(self):
        self.screen.fill((200, 200, 200))
        self.all_bullets.draw(self.screen)
        self.enemy.draw(self.screen)
        pygame.display.flip()

    def update(self):
        self.new_bullet()
        self.all_bullets.update()
        self.enemy.update()

    def new_bullet(self):
        self.time_counter += 1                          # Erhöhe pro Takt um 1 §\label{srcZeit0103}§ 
        if self.time_counter >= self.time_range:        # Wenn Obergrenze erreicht§\label{srcZeit0104}§ 
            b = Bullet("shoot.png")
            b.rect.centerx = self.enemy.sprite.rect.centerx
            b.rect.centery = self.enemy.sprite.rect.centery + 20
            self.all_bullets.add(b)
            self.time_counter = 0                       # Setze Zähler wieder zurück §\label{srcZeit0105}§ 



if __name__ == '__main__':

    game = Game()
    game.run()
