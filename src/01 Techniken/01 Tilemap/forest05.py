import csv
from time import time

import pygame


class Settings:
    FPS = 60
    DELTATIME = 1.0 / FPS
    TILESIZE = pygame.math.Vector2(32, 32)
    TILEMAP_NOF_COLS = 16
    TILEMAP_NOF_ROWS = 12
    TILEMAP_WINDOW = pygame.rect.Rect(0, 0, 
                                      TILEMAP_NOF_COLS * TILESIZE.x, 
                                      TILEMAP_NOF_ROWS * TILESIZE.y)


class Spritelib:
    def __init__(self, filename: str) -> None:
        self.image = pygame.image.load(filename).convert_alpha()

    def subsurface(self, tilenumber: int) -> pygame.surface.Surface:
        left = (tilenumber % Settings.TILEMAP_NOF_COLS) * Settings.TILESIZE.x # 
        top = (tilenumber // Settings.TILEMAP_NOF_COLS) * Settings.TILESIZE.y # 
        tile_rect = pygame.rect.Rect((left, top), Settings.TILESIZE)
        return self.image.subsurface(tile_rect)


class Map:
    def __init__(self, levels:int) -> None:
        self.level_data = []
        for level in range(levels):
            self.level_data.append([])
            with open(f'levels/level_{level}.csv', 'r') as datei:
                csvReader = csv.reader(datei, delimiter=',')
                for row in csvReader:
                    self.level_data[level].append([int(tile) for tile in row])

    def get_level_data(self, level_index: int) -> list[list[int]]:
        return self.level_data[level_index]

class WindowGame:

    def __init__(self) -> None:
        self.window = pygame.Window(size=Settings.TILEMAP_WINDOW.size)
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.window.title = "Tilemap Example"
        self.clock = pygame.time.Clock()
        self.spritelib = Spritelib("images/forest_tiles.png")
        self.map = Map(3)

    def draw(self) -> None:
        self.screen.fill("black")
        for level_index in range(3):
            tiles = self.map.get_level_data(level_index)
            for row in range(Settings.TILEMAP_NOF_ROWS):
                for col in range(Settings.TILEMAP_NOF_COLS):
                    index = tiles[row][col]                
                    if index > -1:                          # §\label{srcforest0501}§
                        image = self.spritelib.subsurface(index)
                        position = col * Settings.TILESIZE.x, row * Settings.TILESIZE.y
                        self.screen.blit(image, position)
        self.window.flip()


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = WindowGame()
        self.running = True

    def run(self) -> None:
        time_previous = time()
        while self.running:
            self.watch_for_events()
            if self.running:
                self.update()
                self.draw()
                self.clock.tick(Settings.FPS)
                time_current = time()
                Settings.DELTATIME = time_current - time_previous
                time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.WINDOWCLOSE:
                self.running = False
                event.window.destroy()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.window.draw()

        

   
def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

