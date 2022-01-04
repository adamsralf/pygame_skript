import pygame
import os


class Settings(object):
    window = {'width':700, 'height':200}
    fps = 60
    title = "Kollisionsarten"
    path = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "images")

    @staticmethod
    def dim():
        return (Settings.window['width'], Settings.window['height'])

    @staticmethod
    def filepath(name):
        return os.path.join(Settings.path['file'], name)

    @staticmethod
    def imagepath(name):
        return os.path.join(Settings.path['image'], name)
    modus = "rect"


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, filename1, filename2) -> None:
        super().__init__()
        self.image_normal = pygame.image.load(Settings.imagepath(filename1)).convert_alpha()
        self.image_hit = pygame.image.load(Settings.imagepath(filename2)).convert_alpha()
        self.image = self.image_normal
        self.rect = self.image.get_rect()                   # Rechteck §\label{srcKollision01}§
        self.mask = pygame.mask.from_surface(self.image)    # Maske §\label{srcKollision02}§
        self.radius = self.rect.width // 2                  # Innenkreis §\label{srcKollision03}§
        self.rect.centery = Settings.window['height'] // 2
        self.hit = False

    def update(self):
        self.image = self.image_hit if (self.hit) else self.image_normal


class Bullet(pygame.sprite.Sprite):
    def __init__(self, picturefile) -> None:
        super().__init__()
        self.image = pygame.image.load(Settings.imagepath(picturefile)).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (10, 10)
        self.directions = {'stop':(0, 0), 'down':(0,  1), 'up':(0, -1), 'left':(-1, 0), 'right':(1, 0)}
        self.set_direction('stop')

    def update(self):
        self.rect.move_ip(self.speed)

    def set_direction(self, direction):
        self.speed = self.directions[direction]


class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        pygame.display.set_caption(Settings.title)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.screen = pygame.display.set_mode(Settings.dim())
        self.clock = pygame.time.Clock()
        self.bullet = pygame.sprite.GroupSingle(Bullet("shoot.png"))
        self.all_obstacles = pygame.sprite.Group()
        self.all_obstacles.add(Obstacle("brick1.png", "brick2.png"))
        self.all_obstacles.add(Obstacle("raumschiff1.png", "raumschiff2.png"))
        self.all_obstacles.add(Obstacle("alienbig1.png", "alienbig2.png"))
        self.running = False

    def run(self):
        self.resize()

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
                elif event.key == pygame.K_DOWN:
                    self.bullet.sprite.set_direction('down')
                elif event.key == pygame.K_UP:
                    self.bullet.sprite.set_direction('up')
                elif event.key == pygame.K_LEFT:
                    self.bullet.sprite.set_direction('left')
                elif event.key == pygame.K_RIGHT:
                    self.bullet.sprite.set_direction('right')
                elif event.key == pygame.K_r:
                    Settings.modus = "rect"
                elif event.key == pygame.K_c:
                    Settings.modus = "circle"
                elif event.key == pygame.K_m:
                    Settings.modus = "mask"
            elif event.type == pygame.KEYUP:
                    self.bullet.sprite.set_direction('stop')

    def update(self):
        self.check_for_collision()
        self.bullet.update()
        self.all_obstacles.update()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.all_obstacles.draw(self.screen)
        self.bullet.draw(self.screen)
        text_surface_modus = self.font.render("Modus: {0}".format(Settings.modus), True, (0, 0, 255))
        self.screen.blit(text_surface_modus, dest=(10, Settings.window['height']-30))
        pygame.display.flip()

    def resize(self):
        total_width = 0 
        for s in self.all_obstacles:
            total_width += s.rect.width
        padding = (Settings.window['width'] - total_width) // 4     # Abstand §\label{srcKollision04}§
        for i in range(len(self.all_obstacles)):
            if i == 0:
                self.all_obstacles.sprites()[i].rect.left = padding 
            else:
                self.all_obstacles.sprites()[i].rect.left = self.all_obstacles.sprites()[i-1].rect.right + padding 

    def check_for_collision(self):
        if Settings.modus == "circle":
            for s in self.all_obstacles:
               s.hit = pygame.sprite.collide_circle(self.bullet.sprite, s)
        elif Settings.modus == "mask":
            for s in self.all_obstacles:
               s.hit = pygame.sprite.collide_mask(self.bullet.sprite, s)
        else:
            for s in self.all_obstacles:
               s.hit = pygame.sprite.collide_rect(self.bullet.sprite, s)


if __name__ == '__main__':

    game = Game()
    game.run()
