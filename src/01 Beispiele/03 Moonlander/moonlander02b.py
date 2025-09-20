from random import randint
from time import time

import pygame


class Settings:
    WINDOW = pygame.rect.Rect(0, 0, 600, 800)
    FPS = 60
    DELTATIME = 1.0 / FPS 
    HORIZONT = 50

class Sky:
    def __init__(self, screen:pygame.surface.Surface) -> None:
        top = 0 
        left = 0
        width = Settings.WINDOW.width
        height = Settings.WINDOW.height - Settings.HORIZONT
        self.rect = pygame.rect.Rect(top, left, width, height)
        self.screen = screen

    def draw(self) -> None:
        pygame.draw.rect(self.screen, "black", self.rect)

class Moon:
    def __init__(self, screen: pygame.surface.Surface, layer_count:int=5, peaks: int=35):
        self.screen = screen
        top = Settings.WINDOW.height - Settings.HORIZONT
        self.rect = pygame.rect.Rect(0, top, 
                                     Settings.WINDOW.width, Settings.HORIZONT) # Landeplatz

        self._layers = []
        dist = self.rect.width // peaks       # Abstand zwischen Höhenunterschieden§\label{moonlander02b01}§ 
        for layer_index in range(layer_count): # Aufbau Gebirge
            mycolor = 180 - layer_index * 20   # Vordergrund dunkler, Hintergrund heller
            y = self.rect.top - 10 - randint(5, 30)*layer_index # Zufällige Starthöhe§\label{moonlander02b02}§ 
            x = self.rect.left          # Erster Peak startet ganz links§\label{moonlander02b03}§ 
            lofPeaks = [(x, top)]        # Der erste Peak als Punkt§\label{moonlander02b04}§ 
            for i in range(peaks):       # Die anderen Peaks des layers werden erzeugt.§\label{moonlander02b05}§ 
                lofPeaks.append((x, y + randint(-5, 10))) # Zufälliger Höheunterschied§\label{moonlander02b06}§ 
                x += dist                # Der nächste Peak ist weiter rechts§\label{moonlander02b07}§ 
            lofPeaks.append((self.rect.right, y))   # Letzter Peak ist ganz rechts
            lofPeaks.append((self.rect.right, top)) # Basis des Gebirgszuges §\label{moonlander02b08}§ 
            self._layers.append({"color":(mycolor, mycolor, mycolor),
                                "peaks":lofPeaks})

    def draw(self):
        # Landefläche
        pygame.draw.rect(self.screen, (230, 230, 230), self.rect)

        # Für jeden Gebirgszug von hinten nach vorne zeichnen -> Tiefeneffekt
        for layer in reversed(self._layers):
            pygame.draw.polygon(
                self.screen,
                layer["color"],
                layer["peaks"]
            )

class Earth:
    def __init__(self, screen:pygame.surface.Surface) -> None:
        self.radius = 80
        left = Settings.WINDOW.right - 2*self.radius - 30
        top = Settings.WINDOW.top + 15
        width = 2*self.radius
        height = 2*self.radius
        self.rect = pygame.rect.Rect(left, top, width, height)
        self.screen = screen


    def draw(self) -> None:
        pygame.draw.circle(self.screen, "blue", self.rect.center, self.radius)

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=Settings.WINDOW.size, title="MyMoonlander", position=pygame.WINDOWPOS_CENTERED)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()


    def run(self) -> None:
        self.restart()
        time_previous = time()
        while self.running:
            self.watch_for_events()
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.restart()

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.background.draw()
        self.moon.draw()
        self.earth.draw()
        self.window.flip()

    def restart(self) -> None:
        self.background = Sky(self.screen)
        self.moon = Moon(self.screen)
        self.earth = Earth(self.screen)
        self.running = True

def main():
    Game().run()

if __name__ == "__main__":
    main()




