import os
from statistics import fmean, median

import pygame
import pygame.time


class Settings:
    window = {'width': 120, 'height': 650}
    fps = 10                                                   # 10 30 60 120 240 300 600
    limit = 500
    deltatime = 1.0/fps

    @staticmethod
    def window_dim():
        return (Settings.window['width'], Settings.window['height'])


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode(Settings.window_dim())
    pygame.display.set_caption("Bewegung")
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_rect = defender_image.get_rect()
    result = {}
    for fps in range(10, 610, 10):
        Settings.fps = fps
        Settings.deltatime = 1.0/Settings.fps
        messures = []
        for index in range(10):
            defender_rect.centerx = Settings.window['width'] // 2
            defender_rect.bottom = Settings.window['height'] - 5
            defender_pos = pygame.Vector2(defender_rect.left, defender_rect.top)
            defender_speed = 600
            defender_direction_v = -1

            clock.tick(Settings.fps)
            start_time = pygame.time.get_ticks()  # Startzeit der Bewegung
            running = True
            while running:
                if pygame.time.get_ticks() > start_time + Settings.limit:
                    defender_speed = 0
                    break
                # Events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Update
                defender_pos[1] += defender_direction_v * defender_speed * Settings.deltatime
                defender_rect.top = round(defender_pos[1])
                if defender_rect.bottom >= Settings.window['height']:
                    defender_direction_v *= -1
                elif defender_rect.top <= 0:
                    defender_direction_v *= -1

                # Draw
                screen.fill("white")
                pygame.draw.line(screen, "red", (0, 315), (Settings.window['width'], 315), 2)
                screen.blit(defender_image, defender_rect)
                pygame.display.flip()
                Settings.deltatime = clock.tick(Settings.fps) / 1000.0
            messures.append(defender_rect.top)
            if fps in (10, 30, 60, 120, 240, 300, 600):
                pygame.image.save(screen, f"fps_05h_{Settings.fps:03d}_{index:02d}.png")
        avg = fmean(messures)       # arithmetische Mittel
        med = median(messures)      # Median
        mad = 0.0                   # Mittlerer absolute Abweichung/Fehler
        for val in messures:
            mad += abs(val - 315)
        mad /= len(messures)
        messures.append(avg)
        messures.append(med)
        messures.append(mad)
        result[Settings.fps] = messures
    with open('result_05h.txt', 'w') as f:
        for key in result.keys():
            f.write(f"{key}")
            for i in range(len(result[key])):
                f.write(f" {result[key][i]}")
            f.write("\n")
    print(result)
    pygame.quit()


if __name__ == '__main__':
    main()
