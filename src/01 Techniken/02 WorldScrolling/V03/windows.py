
import pygame
from globals import Settings


class WindowPlain:

    def __init__(self, tiles:pygame.sprite.Group, mobs:pygame.sprite.Group) -> None:
        self.tiles = tiles
        self.mobs = mobs
        self.window = pygame.Window(size=Settings.WINDOW.size)
        self.window.position = (0 * (Settings.WINDOW.width + 60), 
                                0 * (Settings.WINDOW.height) + 30)
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.window.title = f"Plain Window (size={self.rect.size})"
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill("Black")
        a = [r for r in self.tiles.sprites() if Settings.WINDOW.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, sprite.rect) 
        #self.tiles.draw(self.screen_plain)
        a = [r for r in self.mobs.sprites() if Settings.WINDOW.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, sprite.rect) 
        #self.mobs.draw(self.screen_plain)
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "plain_image.png")


class WindowBirdEyeView:

    def __init__(self, world_screen:pygame.surface.Surface) -> None:
        self.world_screen = world_screen
        zx = Settings.WINDOW.width / Settings.WORLD.width
        zy = Settings.WINDOW.height / Settings.WORLD.height
        self.zoom = pygame.Vector2(zx, zy)
        self.window = pygame.Window(size=Settings.WINDOW.size)
        self.window.position = (1 * (Settings.WINDOW.width + 60), 
                                0 * (Settings.WINDOW.height) + 30)
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.window.title = f"Birdeye (zoom=({self.zoom.x:0.2f}, {self.zoom.y:0.2f})"

    def draw(self):
        image = pygame.transform.scale_by(self.world_screen, self.zoom) #§\label{windowsv0301}§
        self.screen.blit(image)
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "birdeye_image.png")
