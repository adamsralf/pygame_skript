import sys  # Wegen max int
from random import randint
from time import time
from typing import Any

import pygame

from continent_polygons import continent_polygons


class Settings:
    WINDOW = pygame.rect.Rect(0, 0, 600, 800)
    FPS = 60
    DELTATIME = 1.0 / FPS 
    HORIZONT = 50
    # Physikalische Konstanten (Mondbedingungen)
    MOON_GRAVITY = 1.62                         # m/s²
    EARTH_GRAVITY = 9.81                        # m/s²
    PIXELS_PER_METER = 10                       # Skalierung 1m = 10px
    GRAVITY = MOON_GRAVITY * PIXELS_PER_METER   # = 16.2 px/s²
    THRUST = -3 * PIXELS_PER_METER              # = 30.0 px/s²
    LEVEL = {"easy":sys.maxsize, "fair":500, "hard":450, "ai":380} # 

class Sky:
    def __init__(self, screen:pygame.surface.Surface, star_count: int=200) -> None:
        top = 0 
        left = 0
        width = Settings.WINDOW.width
        height = Settings.WINDOW.height - Settings.HORIZONT
        self.rect = pygame.rect.Rect(top, left, width, height)
        self.screen = screen
        
        self.stars = []                    # Sternenliste
        for _ in range(star_count):
            self.stars.append({"pos":(randint(2, self.rect.right-1), 
                                       randint(2, self.rect.right-1)),
                          "size":randint(1, 3),
                          "duration": randint(200, 600), # Zeit in frames
                          "counter":0,
                          "color":randint(10, 255)})
    
    def update(self) -> None:
        for star in self.stars:
            star["counter"] = (star["counter"] + 1) % (star["duration"] + 1) # Zähler 
            if star["counter"] == 0:          
                star["color"] = (star["color"] + randint(0, 70)) % 256
                star["size"] = (star["size"] + 1) % 4

    def draw(self) -> None:
        pygame.draw.rect(self.screen, "black", self.rect)
        for star in self.stars:
            pygame.draw.circle(self.screen, (255,255,star["color"]), star["pos"], star["size"])

class Moon:
    def __init__(self, screen: pygame.surface.Surface, layer_count:int=5, peaks: int=35):
        self.screen = screen
        self.surface = pygame.surface.Surface((Settings.WINDOW.width, 
                                                Settings.HORIZONT + layer_count*30),
                                                pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.left = Settings.WINDOW.left
        self.rect.bottom = Settings.WINDOW.bottom
        landingarea = pygame.rect.Rect(0, self.rect.height - Settings.HORIZONT, 
                                     Settings.WINDOW.width, Settings.HORIZONT) # Landeplatz

        layers = []
        for layer_index in range(layer_count): # Aufbau Gebirge
            mypeaks = randint(peaks//2, peaks) # Anzahl variiert
            dist = landingarea.width // mypeaks # Abstand zwischen Höhenunterschieden
            mycolor = 180 - layer_index * 20   # Vordergrund dunkler, Hintergrund heller
            y = landingarea.top - 10 - randint(5, 10)*layer_index # Zufällige Starthöhe
            x = landingarea.left                # Erster Peak startet ganz links
            lofPeaks = [(x, landingarea.top)]   # Der erste Peak als Punkt
            for i in range(mypeaks):           # Die anderen Peaks werden erzeugt.
                lofPeaks.append((x, y + randint(-5, 20))) # Zufälliger Höheunterschied
                x += dist                      # Der nächste Peak ist weiter rechts
            lofPeaks.append((landingarea.right, y))   # Letzter Peak ist ganz rechts
            lofPeaks.append((landingarea.right, landingarea.top)) # Basis des Gebirgszuges 

            poly = []                          # Ein Polygonzug
            for index in range(len(lofPeaks)-1):
                p1 = lofPeaks[index]
                p2 = lofPeaks[index+1]
                p3 = (lofPeaks[index+1][0], landingarea.top)
                p4 = (lofPeaks[index][0], landingarea.top)
                r = randint(-5,5)
                c =  [mc +  r for mc in (mycolor, mycolor, mycolor)]
                poly.append({"points":(p1, p2, p3, p4), "color":c})
            layers.append(poly)

        # Landefläche
        pygame.draw.rect(self.surface, (230, 230, 230), landingarea)

        # Für jeden Gebirgszug von hinten nach vorne zeichnen -> Tiefeneffekt
        for layer in reversed(layers):
            for poly in layer:
                pygame.draw.polygon(
                    self.surface,
                    poly["color"],
                    poly["points"])

    def draw(self):
        self.screen.blit(self.surface, self.rect.topleft)
 
class Earth:
    def __init__(self, screen:pygame.surface.Surface) -> None:
        self.radius = 80
        self.surface = pygame.surface.Surface(
            (2*self.radius, 2*self.radius), 
            pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.left = Settings.WINDOW.right - 200
        self.rect.top = Settings.WINDOW.top + 50
        self.screen = screen

        for a in range(20, 1, -1):
            pygame.draw.circle(self.surface, 
                               (135, 206, 250, 210-a*10),       # Steigende Transparanz
                               (self.radius, self.radius), 
                               self.radius-20+a)               # Wachsender Radius
        pygame.draw.circle(self.surface, 
                           (30, 144, 255), 
                           (self.radius, self.radius), 
                           self.radius-20)
        
        for landmasse in continent_polygons:
            poly = [(self.radius + (0.5*x), self.radius + (0.5*y)) for (x, y) in landmasse]
            pygame.draw.polygon(self.surface, (181, 150, 116), poly)


    def draw(self) -> None:
        self.screen.blit(self.surface, self.rect.topleft)

class Lander:
    def __init__(self, window: pygame.window.Window) -> None: # §\label{moonlander0701}§
        self.screen = window.get_surface()
        self.surface = pygame.surface.Surface((90,81), pygame.SRCALPHA)
        self.surface_thrusting = pygame.surface.Surface((90,81), pygame.SRCALPHA)
        self.rect = self.surface.get_frect()
        self.rect.centerx = Settings.WINDOW.centerx # horizontale Startposition
        self.rect.top = self.rect.height            # vertikale Startposition
        self.create_lander()                        # Zeichnen wird ausgelagert
        self.thrusting = False                      # Flag, ob beschleunigt wird
        self.velocity = 0                           # Horizontale Geschwindigkeit
        self.fuel_initial = Settings.LEVEL["fair"]  # Starttreibstoff 
        self.fuel = self.fuel_initial               # Aktueller Treibstoff
        self.fuel_consumption = 20                  # Treibstoffverbrauch pro Sekunde
        self.create_status_window(window)

    def create_lander(self) -> None:
        # Ein paar Abkürzungen
        cx = self.rect.width // 2
        cy = self.rect.height //2
        s = self.rect.width // 2
        sur = self.surface

        # Antenne
        pygame.draw.line(sur, (220, 220, 220), (cx, cy - s//2), (cx, cy - s//1.2), 2)
        pygame.draw.circle(sur, (255, 255, 255), (cx, cy - s//1.2), 3)

        # Oberes Crewmodul (schmaler)
        pygame.draw.polygon(
            sur, (160, 160, 160),
            [(cx - s//4, cy - s//2),
             (cx - s//6, cy - s//3),
             (cx + s//6, cy - s//3),
             (cx + s//4, cy - s//2)]
        )

        # Verbinder zwischen Basis und Crewmodul
        conn_color = (160, 160, 160)
        pygame.draw.line(sur, conn_color, (cx - s//3, cy), (cx - s//6, cy - s//3), 2)
        pygame.draw.line(sur, conn_color, (cx, cy), (cx, cy - s//3), 2)
        pygame.draw.line(sur, conn_color, (cx + s//3, cy), (cx + s//6, cy - s//3), 2)

        # Modulbasis (zentrale Kapsel, hellgrau)
        pygame.draw.polygon(
            sur, (200, 200, 200),
            [(cx - s//3, cy),
             (cx - s//2, cy + s//2),
             (cx + s//2, cy + s//2),
             (cx + s//3, cy)]
        )

        # Fenster im Modul
        r = 5
        window_color = (50, 50, 50)
        pygame.draw.circle(sur, window_color, (cx, cy+(s//4)), r)
        pygame.draw.circle(sur, window_color, (cx-(s//4), cy+(s//4)), r)
        pygame.draw.circle(sur, window_color, (cx+(s//4), cy+(s//4)), r)

        # Landebeine
        leg_color = (100, 100, 100)
        pygame.draw.line(sur, leg_color, (cx - s//2, cy + s//2), (cx - s, cy + s), 3)
        pygame.draw.line(sur, leg_color, (cx + s//2, cy + s//2), (cx + s, cy + s), 3)
        pygame.draw.line(sur, leg_color, (cx - s//4, cy + s//2), (cx - s//3, cy + s), 3)
        pygame.draw.line(sur, leg_color, (cx + s//4, cy + s//2), (cx + s//3, cy + s), 3)

        # Füße
        feet_color = (150, 150, 150)
        pygame.draw.circle(sur, feet_color, (cx - s + (r+2), cy + s - (r+2)), r-1)
        pygame.draw.circle(sur, feet_color, (cx + s - (r+2), cy + s - (r+2)), r-1)
        pygame.draw.circle(sur, feet_color, (cx - s//3 + (r-4), cy + s - (r+2)), r-1)
        pygame.draw.circle(sur, feet_color, (cx + s//3 - (r-4), cy + s - (r+2)), r-1)

        # Ausstoß
        self.surface_thrusting.blit(sur, (0,0))
        pygame.draw.polygon(self.surface_thrusting, (255, 140, 0), [
            (cx - 5, cy + s//2),
            (cx + 5, cy + s//2),
            (cx, cy + s//2 + 20)
        ])

    def create_status_window(self, window: pygame.window.Window) -> None:
        self.status_window = pygame.Window(size=(300, 100), title="Status")
        self.status_screen = self.status_window.get_surface()
        top = window.position[1]
        left = window.position[0] + Settings.WINDOW.width + 10
        self.status_window.position = (left, top)

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "thrust":
                self.thrust(True)
            elif kwargs["action"] == "unthrust":
                self.thrust(False)
            elif kwargs["action"] == "move":
                self.move()

    def thrust(self, thrusting:bool) -> None:
        if thrusting and self.fuel > 0:
            self.thrusting = True
        else:
            self.thrusting = False

    def draw(self) -> None:
        if self.thrusting:
            self.screen.blit(self.surface_thrusting, self.rect.topleft)
        else:
            self.screen.blit(self.surface, self.rect.topleft)
        self.draw_status()

    def draw_status(self) -> None:
        self.status_screen.fill("black")

        # Textausgabe §\label{moonlander0705}§
        font = pygame.font.SysFont("Consolas", 14)
        labels = f"Geschwindigkeit (px/s):"
        labels += "\nHöhe (px):"
        values = f"{self.velocity:>7.0f}"
        values += f"\n{-1*(self.rect.bottom - (Settings.WINDOW.bottom - Settings.HORIZONT)):>7.0f}"
        text_labels = font.render(labels, True, "white")
        text_values = font.render(values, True, "white")
        self.status_screen.blit(text_labels, (5, 10))
        self.status_screen.blit(text_values, (230, 10))

        # Balkenanzeige §\label{moonlander0706}§
        if self.thrusting:
            pygame.draw.rect(self.status_screen, (255, 140, 0), (5, 46, 290, 20))
        pygame.draw.rect(self.status_screen, "grey", (5, 70, 290, 20))
        ratio = int(290 * self.fuel / self.fuel_initial)
        pygame.draw.rect(self.status_screen, "green", (5, 70, ratio, 20))

        self.status_window.flip()
        
    def move(self) -> None:
        if self.thrusting and self.fuel > 0:                          # Treibstoff übrig?
            self.velocity += Settings.THRUST * Settings.DELTATIME
            self.fuel -= self.fuel_consumption * Settings.DELTATIME   # Treibstoffverbrauch
            if self.fuel < 0:
                self.thrusting = False
                self.fuel = 0
        self.velocity += Settings.GRAVITY * Settings.DELTATIME
        self.rect.top += self.velocity * Settings.DELTATIME
        if self.rect.bottom >= Settings.WINDOW.bottom - Settings.HORIZONT:
            self.rect.bottom = Settings.WINDOW.bottom -Settings.HORIZONT
            self.velocity = 0      # Aufsetzen -> Geschwindigkeit 0§\label{moonlander0702}§         

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
            if self.running:
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
            elif event.type == pygame.WINDOWCLOSE:  # Neu wegen 2 Fenster! §\label{moonlander0703}§ 
                self.running = False
                event.window.destroy()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.restart()
                elif event.key == pygame.K_SPACE:
                    self._lander.update(action="thrust")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self._lander.update(action="unthrust")

    def update(self) -> None:
        self.background.update()
        self._lander.update(action="move")      # Soll sich bewegen!

    def draw(self) -> None:
        self.background.draw()
        self.moon.draw()
        self.earth.draw()
        self._lander.draw()
        self.window.flip()

    def restart(self) -> None:
        self.background = Sky(self.screen)
        self.moon = Moon(self.screen)
        self.earth = Earth(self.screen)
        self._lander = Lander(self.window)     # wegen Statusfenster§\label{moonlander0704}§  
        self.running = True

def main():
    Game().run()

if __name__ == "__main__":
    main()





