import pygame
from pygame.constants import (QUIT, K_KP_PLUS, K_KP_MINUS, K_ESCAPE, KEYDOWN)
import os



class Settings(object):
    window = {'width':300, 'height':200}
    fps = 60
    title = "Animation"
    path = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "images")
    directions = {'stop':(0, 0), 'down':(0,  1), 'up':(0, -1), 'left':(-1, 0), 'right':(1, 0)}

    @staticmethod
    def dim():
        return (Settings.window['width'], Settings.window['height'])

    @staticmethod
    def filepath(name):
        return os.path.join(Settings.path['file'], name)

    @staticmethod
    def imagepath(name):
        return os.path.join(Settings.path['image'], name)


class Timer(object):
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

    def change_duration(self, delta=10):
        self.duration += delta
        if self.duration < 0:
            self.duration = 0


class Animation(object):
    def __init__(self, namelist, endless, animationtime, colorkey=None):
        self.images = []
        self.endless = endless
        self.timer = Timer(animationtime)
        for filename in namelist:
            if colorkey == None:
                bitmap = pygame.image.load(Settings.imagepath(filename)).convert_alpha()
            else:
                bitmap = pygame.image.load(Settings.imagepath(filename)).convert()
                bitmap.set_colorkey(colorkey)           # Transparenz herstellen §\label{srcAnimation0101}§
            self.images.append(bitmap)
        self.imageindex = -1

    def next(self):
        if self.timer.is_next_stop_reached():
            self.imageindex += 1
            if self.imageindex >= len(self.images):
                if self.endless:
                    self.imageindex = 0
                else:
                    self.imageindex = len(self.images) - 1
        return self.images[self.imageindex]

    def is_ended(self):
        if self.endless:
            return False
        elif self.imageindex >= len(self.images) - 1:
            return True
        else:
            return False
        



class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation=Animation([f"cat{i}.bmp" for i in range(6)], True, 100, (0,0,0)) # §\label{srcAnimation0102}§
        self.image = self.animation.next()
        self.rect = self.image.get_rect()
        self.rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2)

    def update(self):
        self.image = self.animation.next()



class CatAnimation(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.dim())
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.cat = pygame.sprite.GroupSingle(Cat())
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
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False


    def update(self) -> None:
        self.cat.update()

    def draw(self) -> None:
        self.screen.fill((200, 200, 200))
        self.cat.draw(self.screen)
        pygame.display.flip()



if __name__ == '__main__':
    anim = CatAnimation()
    anim.run()

