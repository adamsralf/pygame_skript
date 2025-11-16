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
