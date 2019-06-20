from level import Level
import constants as const
import pygame


class Game:

    def __init__(self):
        self.window = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
        self.levels = ["levels/level01.json", "levels/level01.json"]
        self.current_level = 0
        self.level = Level(self.levels[self.current_level])

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_p:
                        self.level.toggle_pause()

            self.update()
            self.draw()
        pygame.quit()

    def draw(self):
        self.level.draw(self.window)

        pygame.display.update()

    def update(self):
        self.level.update()


if __name__ == "__main__":
    game = Game()
    game.run()
