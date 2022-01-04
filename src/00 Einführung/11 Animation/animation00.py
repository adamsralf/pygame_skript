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


class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        for i in range(6):                          # Animations-Sprites laden §\label{srcAnimation0001}§
            bitmap = pygame.image.load(Settings.imagepath(f"cat{i}.bmp")).convert()
            bitmap.set_colorkey((0,0,0))
            self.images.append(bitmap)
        self.imageindex = 0
        self.image = self.images[self.imageindex]
        self.rect = self.image.get_rect()
        self.rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2)
        self.animation_time = Timer(100)

    def update(self):
        if self.animation_time.is_next_stop_reached():
            self.imageindex += 1
            if self.imageindex >= len(self.images):
                self.imageindex = 0
            self.image = self.images[self.imageindex]
            # implement game logic here

    def change_animation_time(self, delta):
        self.animation_time.change_duration(delta)


class CatAnimation(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.dim())
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.cat = pygame.sprite.GroupSingle(Cat()) # Meine Katze §\label{srcAnimation0002}§
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
                elif event.key == K_KP_PLUS:
                    self.cat.sprite.change_animation_time(-10)
                elif event.key == K_KP_MINUS:
                    self.cat.sprite.change_animation_time(10)

    def update(self) -> None:
        self.cat.update()

    def draw(self) -> None:
        self.screen.fill((200, 200, 200))
        self.cat.draw(self.screen)
        text_image = self.font.render(f"animation time: {self.cat.sprite.animation_time.duration}", True, (255, 255, 255))
        text_rect = text_image.get_rect()
        text_rect.centerx = Settings.window['width'] // 2
        text_rect.bottom = Settings.window['height'] - 50
        self.screen.blit(text_image, text_rect)
        pygame.display.flip()



if __name__ == '__main__':
    anim = CatAnimation()
    anim.run()

