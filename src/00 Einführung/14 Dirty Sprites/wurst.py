from time import time

import pygame


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (600, 600))
    FPS = 60
    DELTATIME = 1.0 / FPS


class Ball(pygame.sprite.DirtySprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.surface.Surface((30, 30)).convert()
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, "blue", (15, 15), 15)
        pygame.draw.rect(self.image, "red", (0, 0, 30, 30), 1)

        # Für Dirty-Rects lieber int-Rect (stabiler als FRect)
        self.rect = self.image.get_rect(topleft=(100, 100))

        # Pixel pro Sekunde
        self.speed = pygame.Vector2(-200, 120)

        self.dirty = 1

    def update(self) -> None:
        # dt-basierte Bewegung
        self.rect.x += int(self.speed.x * Settings.DELTATIME)
        self.rect.y += int(self.speed.y * Settings.DELTATIME)

        if self.rect.left < 0 or self.rect.right > Settings.WINDOW.width:
            self.speed.x *= -1
        if self.rect.top < 0 or self.rect.bottom > Settings.WINDOW.height:
            self.speed.y *= -1

        self.dirty = 1


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("Ball mit DirtySprite (fixed)")

        self.clock = pygame.time.Clock()

        # Hintergrund (Surface) vorbereiten
        self.background = pygame.Surface(Settings.WINDOW.size).convert()
        self.background.fill("white")

        # Hintergrund einmal initial zeichnen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        # LayeredDirty-Gruppe
        self.group = pygame.sprite.LayeredDirty()
        self.group.add(Ball())

        # Optional: hilft LayeredDirty beim Timing
        self.group.set_timing_threshold(1000.0 / Settings.FPS)

        self.running = True

    def run(self) -> None:
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

    def update(self) -> None:
        self.group.update()

    def draw(self) -> None:
        # WICHTIG: alte Sprite-Positionen mit Hintergrund löschen
        self.group.clear(self.screen, self.background)

        # Neu zeichnen -> liefert dirty rects
        rects = self.group.draw(self.screen)

        # Nur die betroffenen Bereiche updaten
        pygame.display.update(rects)


if __name__ == "__main__":
    Game().run()
