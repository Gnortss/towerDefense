import constants as const


class Defense:
    img = None

    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.level = 0
        self.range = 30  # In pixels
        self.upgrade_cost = []
        self.sell_cost = []
        self.placed = False

    def draw(self, window):
        cx = self.x - int(self.width/2)
        cy = self.y - int(self.height/2)
        window.blit(self.img, (cx * const.CELL_WIDTH, cy * const.CELL_HEIGHT))

    def move_to(self, x, y):
        """
        Clips the tower to the cell which is covering given x and y
        :param x: x coordinate
        :param y: y coordinate
        :return: None
        """
        self.x = x // const.CELL_WIDTH
        self.y = y // const.CELL_HEIGHT

    def place(self):
        self.placed = True

    def upgrade(self):
        pass

    def sell(self):
        pass
