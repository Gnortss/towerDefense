import constants as const


class Map:

    def __init__(self, grid):
        self.grid = []
        self.width = len(grid[0])
        self.height = len(grid)
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                x = i * const.CELL_WIDTH
                y = j * const.CELL_HEIGHT
                grid.append({
                    "info": (cell, 0),
                    "coords": (x, y)
                })

    def get_cell_info(self, x, y):
        return self.grid[y * self.width + x]['info']

    def get_cell_type(self, x, y):
        return self.grid[y * self.width + x]['info'][0]

    def get_cell_coords(self, x, y):
        return self.grid[y * self.width + x]['coords']

    def set_cell(self, x, y, info, coords):
        self.grid[y * self.width + x] = {
            "info": info,
            "coords": coords
        }
