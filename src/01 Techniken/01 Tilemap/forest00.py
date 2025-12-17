import csv
from time import time

import pygame


class Settings:
    FPS = 60
    DELTATIME = 1.0 / FPS
    TILESIZE = pygame.math.Vector2(32, 32)
    TILEMAP_NOF_COLS = 16
    TILEMAP_NOF_ROWS = 12
    TILEMAP_WINDOW: pygame.rect.FRect = pygame.rect.FRect(0, 0, TILEMAP_NOF_COLS * TILESIZE.x, TILEMAP_NOF_ROWS * TILESIZE.y)
    TARGET_NOF_COLS = 16
    TARGET_NOF_ROWS = 12
    TARGET_WINDOW: pygame.rect.FRect = pygame.rect.FRect(0, 0, TARGET_NOF_COLS * TILESIZE.x, TARGET_NOF_ROWS * TILESIZE.y)
    TILENUMBER : int = 0

class WindowTilemap:

    def __init__(self, filename:str, pos:tuple[int,int]) -> None:
        self.filename = f"images/{filename}"
        self.window = pygame.Window(size=Settings.TILEMAP_WINDOW.size)
        left = pos[0] * (Settings.TARGET_WINDOW.width + 5)
        top = 70 + pos[1] * (Settings.TARGET_WINDOW.height + 30)
        self.window.position = left, top
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.image = pygame.image.load(self.filename).convert_alpha()
        self.rect = self.screen.get_frect()
        self.window.title = f"Tilemap (size={Settings.TILESIZE})"
        self.clock = pygame.time.Clock()
        self.number_font = pygame.font.Font(pygame.font.get_default_font(), 10)
        self.grid = True
        self.number = False
        self.sprites = []
        for x in range(0, int(Settings.TILEMAP_WINDOW.width), int(Settings.TILESIZE.x)):
            for y in range(0, int(Settings.TILEMAP_WINDOW.height), int(Settings.TILESIZE.y)):
                self.sprites.append(self.image.subsurface((x, y), Settings.TILESIZE))


    def draw(self) -> None:
        self.screen.fill("black")
        self.screen.blit(self.image, self.rect) 
        if self.grid:
            for x in range(0, int(Settings.TILEMAP_WINDOW.width), int(Settings.TILESIZE.x)):
                pygame.draw.line(self.screen, "red", (x, Settings.TILEMAP_WINDOW.top), (x, Settings.TILEMAP_WINDOW.bottom))
            for y in range(0, int(Settings.TILEMAP_WINDOW.height), int(Settings.TILESIZE.y)):
                pygame.draw.line(self.screen, "red", (Settings.TILEMAP_WINDOW.left, y), (Settings.TILEMAP_WINDOW.right, y))
        if self.number:
            for x in range(Settings.TILEMAP_NOF_COLS):
                for y in range(Settings.TILEMAP_NOF_ROWS):
                    bitmap = self.number_font.render(f"{self.get_number(x, y)}", True, "red")
                    left = 1 + x * Settings.TILESIZE.x
                    top = 1 + y * Settings.TILESIZE.y
                    self.screen.blit(bitmap, (left, top))
        if Settings.TILENUMBER > -1:
            tile_x = (Settings.TILENUMBER % Settings.TILEMAP_NOF_COLS) * Settings.TILESIZE.x
            tile_y = (Settings.TILENUMBER // Settings.TILEMAP_NOF_COLS) * Settings.TILESIZE.y
            tile_rect = pygame.rect.FRect((tile_x, tile_y), Settings.TILESIZE)
            pygame.draw.rect(self.screen, "yellow", tile_rect, 3)

        self.window.flip()

    def toogle_grid(self) -> None:
        self.grid = not self.grid

    def toogle_number(self) -> None:
        self.number = not self.number

    def get_number(self, col:int, row:int) -> int:
        return row * Settings.TILEMAP_NOF_COLS + col


class WindowTarget:

    def __init__(self, filename:str, level:int, pos:tuple[int,int]) -> None:
        self.window = pygame.Window(size=Settings.TILEMAP_WINDOW.size)
        left = pos[0] * (Settings.TARGET_WINDOW.width + 5)
        top = 70 + pos[1] * (Settings.TARGET_WINDOW.height + 30)
        self.window.position = left, top
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_rect()
        self.window.title = f"Target: Level {level}"
        self.grid = True
        self.filename = f"images/{filename}"
        self.spritelib = pygame.image.load(self.filename).convert_alpha()
        self.level = level
        self.level_data = [[-1 for _ in range(Settings.TARGET_NOF_COLS)]
                           for _ in range(Settings.TARGET_NOF_ROWS)]


    def draw(self):
        self.screen.fill("black")
        for row in range(Settings.TARGET_NOF_ROWS):
            for col in range(Settings.TARGET_NOF_COLS):
                if self.level_data[row][col] > -1:
                    self.tile_number = self.level_data[row][col]
                    tile_x = (self.tile_number % Settings.TILEMAP_NOF_COLS) * Settings.TILESIZE.x
                    tile_y = (self.tile_number // Settings.TILEMAP_NOF_COLS) * Settings.TILESIZE.y
                    tile_rect = pygame.rect.FRect((tile_x, tile_y), Settings.TILESIZE)
                    dest_x = col * Settings.TILESIZE.x
                    dest_y = row * Settings.TILESIZE.y
                    self.screen.blit(self.spritelib, (dest_x, dest_y), tile_rect)
        if self.grid:
            for x in range(0, int(Settings.TARGET_WINDOW.width), int(Settings.TILESIZE.x)):
                pygame.draw.line(self.screen, "red", (x, Settings.TARGET_WINDOW.top), (x, Settings.TARGET_WINDOW.bottom))
            for y in range(0, int(Settings.TARGET_WINDOW.height), int(Settings.TILESIZE.y)):
                pygame.draw.line(self.screen, "red", (Settings.TARGET_WINDOW.left, y), (Settings.TARGET_WINDOW.right, y))
        self.window.flip()

    def save(self) -> None:
        with open(f'levels/level_{self.level}.csv', 'w', newline='') as datei:
            csvWriter = csv.writer(datei, delimiter=',')
            csvWriter.writerows(self.level_data)

    def load(self) -> None:
        self.level_data = []
        with open(f'levels/level_{self.level}.csv', 'r') as datei:
            csvReader = csv.reader(datei, delimiter=',')
            for row in csvReader:
                self.level_data.append([int(tile) for tile in row])

    def set_tile(self, pos:tuple[int, int]) -> None:
        col = pos[0] // int(Settings.TILESIZE.x)
        row = pos[1] // int(Settings.TILESIZE.y)
        print(f"Set tile at col={col}, row={row} to tilenumber={Settings.TILENUMBER}")
        self.level_data[row][col] = Settings.TILENUMBER


class WindowResult:

    def __init__(self, filename:str, pos:tuple[int,int]) -> None:
        self.window = pygame.Window(size=Settings.TILEMAP_WINDOW.size)
        left = pos[0] * (Settings.TARGET_WINDOW.width + 5)
        top = 70 + pos[1] * (Settings.TARGET_WINDOW.height + 30)
        self.window.position = left, top
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_rect()
        self.window.title = "Result"
        self.filename = f"images/{filename}"
        self.spritelib = pygame.image.load(self.filename).convert_alpha()
        self.level_data = []
        self.load()


    def draw(self):
        self.screen.fill("black")
        for level in range(3):
            for row in range(Settings.TARGET_NOF_ROWS):
                for col in range(Settings.TARGET_NOF_COLS):
                    if self.level_data[level][row][col] > -1:
                        self.tile_number = self.level_data[level][row][col]
                        tile_x = (self.tile_number % Settings.TILEMAP_NOF_COLS) * Settings.TILESIZE.x
                        tile_y = (self.tile_number // Settings.TILEMAP_NOF_COLS) * Settings.TILESIZE.y
                        tile_rect = pygame.rect.FRect((tile_x, tile_y), Settings.TILESIZE)
                        dest_x = col * Settings.TILESIZE.x
                        dest_y = row * Settings.TILESIZE.y
                        self.screen.blit(self.spritelib, (dest_x, dest_y), tile_rect)
        self.window.flip()

    def load(self) -> None:
        self.level_data = []
        for level in range(3):
            self.level_data.append([])
            with open(f'levels/level_{level}.csv', 'r') as datei:
                csvReader = csv.reader(datei, delimiter=',')
                for row in csvReader:
                    self.level_data[level].append([int(tile) for tile in row])


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window_tilemap = WindowTilemap("forest_tiles.png", (0, 0))
        self.window_target = []
        for level in range(3):
            self.window_target.append(WindowTarget("forest_tiles.png", level, (level , 1)))
        self.window_result = WindowResult("forest_tiles.png", (1, 0))
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
                elif event.key == pygame.K_g:
                    self.window_tilemap.toogle_grid()
                elif event.key == pygame.K_n:
                    self.window_tilemap.toogle_number()
                elif event.key == pygame.K_s:
                    for window_target in self.window_target:
                        window_target.save()
                elif event.key == pygame.K_p:
                    self.save()
                elif event.key == pygame.K_l:
                    for window_target in self.window_target:
                        window_target.load()
                    self.window_result.load()
                elif event.key == pygame.K_a:
                    self.all_in_one()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    try:
                        print(f"Mouse button {event.button} down at {event.pos} / {event.window.id}")
                        for window_target in self.window_target:
                            if event.window.id == window_target.window.id:
                                window_target.set_tile(event.pos)
                        if event.window.id == self.window_tilemap.window.id:
                            self.set_tilenumber(event)
                    except Exception:
                        pass
                else:
                    Settings.TILENUMBER = -1

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.window_tilemap.draw()
        for window_target in self.window_target:
            window_target.draw()
        self.window_result.draw()

    def set_tilenumber(self, event) -> None:
        Settings.TILENUMBER = (event.pos[1] // int(Settings.TILESIZE.y)) * Settings.TILEMAP_NOF_COLS + (event.pos[0] // int(Settings.TILESIZE.x))

    def save(self) -> None:
        pygame.image.save(self.window_tilemap.image, "TileMap01.png")
        pygame.image.save(self.window_tilemap.screen, "TileMap02.png")
        pygame.image.save(self.window_result.screen, "result.png")
        for level in range(3):
            pygame.image.save(self.window_target[level].screen, (f"target_level_{level}.png"))

    def all_in_one(self) -> None:
        level_data = [[-1 for _ in range(Settings.TARGET_NOF_COLS)]
                        for _ in range(Settings.TARGET_NOF_ROWS)]
        for i in range(3):
            for row in range(Settings.TARGET_NOF_ROWS):
                for col in range(Settings.TARGET_NOF_COLS):
                    value = self.window_target[i].level_data[row][col]
                    if value > -1:
                        level_data[row][col] = value

        with open('levels/level_all.csv', 'w', newline='') as datei:
            csvWriter = csv.writer(datei, delimiter=',')
            csvWriter.writerows(level_data)

  

   
def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()


