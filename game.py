from level import Level
from level_selector import LevelSelector
import constants as const
import pygame


class Game:

    def __init__(self):
        pygame.font.init()
        self.window = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
        self.placing = False
        self.level = None

        # init and show levels
        self.ls = LevelSelector(const.LEVEL_DIR, self.window)
        pygame.display.update()

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
                    if self.level is not None:
                        if event.key == pygame.K_p:
                            self.level.toggle_pause()
                        if event.key == pygame.K_1:
                            self.create_defense(1)
                        if event.key == pygame.K_2:
                            self.create_defense(2)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.level is None:
                        self.level = self.ls.get_level(*pygame.mouse.get_pos())  # Return Level or None
                    if self.placing and self.level is not None:  # 1 is left click
                        # print("Confirming placement")
                        self.confirm_placing()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if self.placing and self.level is not None:  # 3 is right click
                        # print("Canceling placement")
                        self.cancel_placing()

            self.update()
        pygame.quit()

    def update(self):
        if self.level is not None:
            message = self.level.update(self.window)
            if message is not None:  # Level has ended
                # show end message
                print(message)
                # reset back to level selector
                self.placing = False
                self.level = None

                self.ls.draw(self.window)

        pygame.display.update()

    def create_defense(self, defense_id):
        if not self.placing:
            self.placing = self.level.create_defense(defense_id)
            # print("Trying to place defense: ", self.placing)

    def confirm_placing(self):
        if self.level.confirm_placing():
            self.placing = False
            # print("CONFIRMED")
        # else:
            # print("CAN'T CONFIRM")

    def cancel_placing(self):
        if self.level.cancel_placing():
            self.placing = False
        #     print("CANCELED")
        # else:
        #     print("CAN'T CANCEL")


if __name__ == "__main__":
    game = Game()
    game.run()
