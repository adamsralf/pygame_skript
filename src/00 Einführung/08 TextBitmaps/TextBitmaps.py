import pygame
from pygame import (KEYDOWN, QUIT, K_ESCAPE)
import os


class Settings:
    window = {'width': 700, 'height': 650}
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


class Spritelib(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(Settings.imagepath(filename)).convert()
        self.rect = self.image.get_rect()
        self.nof = {'rows': 4, 'cols': 10}
        self.letter = {'width':18, 'height':18}
        self.offset = {'h':6, 'v':6}
        self.distance = {'h':14, 'v':14}


    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Letters(object):
    def __init__(self, spritelib, colornumber) -> None:
        super().__init__()
        self.spritelib = spritelib
        self.letters = {}
        self.create_letter_bitmap(colornumber)

    def create_letter_bitmap(self, colornumber):
        lettername = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-', ' ', 'copy', 'square') # §\label{srcTextbitmaps0000}§
        index = 0
        startpos = (self.spritelib.offset['h'], self.spritelib.offset['v'] + colornumber * self.spritelib.nof['rows'] * (self.spritelib.letter['height'] + self.spritelib.distance['v']))  # §\label{srcTextbitmaps0001}§      
        for row in range(self.spritelib.nof['rows']):            # Zeilen §\label{srcTextbitmaps0002}§ 
            for col in range(self.spritelib.nof['cols']):        # Spalten §\label{srcTextbitmaps0003}§ 
                left = startpos[0] + col * (self.spritelib.letter['width'] + self.spritelib.distance['h']) # §\label{srcTextbitmaps0004}§ 
                top =  startpos[1] + row * (self.spritelib.letter['height'] + self.spritelib.distance['v']) # §\label{srcTextbitmaps0005}§ 
                width, height = self.spritelib.letter.values()   # Größe §\label{srcTextbitmaps0006}§ 
                r = pygame.Rect(left, top, width, height)
                self.letters[lettername[index]] = self.spritelib.image.subsurface(r) # §\label{srcTextbitmaps0007}§ 
                index += 1

    def get_letter(self, letter):
        if letter in self.letters:
            return self.letters[letter]
        else:
            return self.letters['square']

    def get_text(self, text):
        l = len(text) * self.spritelib.letter['width']
        h = self.spritelib.letter['height']
        bitmap = pygame.Surface((l, h))
        bitmap.set_colorkey((0, 0, 0))
        for a in range(len(text)):
            bitmap.blit(self.get_letter(text[a]), (a * self.spritelib.letter['width'], 0))
        return bitmap


class TextBitmaps(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.dim())
        pygame.display.set_caption('Textausgabe mit Bitmaps')
        self.clock = pygame.time.Clock()
        self.filename = "chars.png"
        self.running = False
        self.input = ""

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_BACKSPACE:
                    self.input = self.input[:-1]        # Letztes Zeichen abschneiden§\label{srcTextbitmaps0008}§ 
                else:
                    self.input += event.unicode         # Tastaturwert als unicode-Zeichen§\label{srcTextbitmaps0009}§ 

    def run(self):
        spritelib = Spritelib(self.filename)
        letters = Letters(spritelib, 2)
        self.running = True
        while self.running:
            self.clock.tick(60)
            self.watch_for_events()
            self.screen.fill((200, 200, 200))
            self.screen.blit(letters.get_text(self.input), (400, 200))
            spritelib.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"

    demo = TextBitmaps()
    demo.run()
