from celltype_enum import celltype_e
from encoder import decode_string


class Level:
    def __init__(self):
        self.width = None
        self.height = None
        self.string = None
        self.name = None
        self.tutorial_text = None

        self.background_cells = []
        self.cells = []

    def init_dimensions(self, width, height, max_size):
        if width > max_size or height > max_size:
            return True
        self.width = width
        self.height = height

        for column in range(width):
            self.cells.append([None] * height)
            self.background_cells.append([celltype_e.BGDEFAULT] * height)
        return False

    def set_cell(self, c, i):
        # c is cell type index, i is the level position index
        if c % 2 == 1:
            self.background_cells[i % self.width][i // self.width] = celltype_e.BGPLACEABLE0
        if c >= 72:
            return
        self.cells[i % self.width][i // self.width] = (celltype_e((c // 2) % 9), [0, 3, 2, 1][c // 18])


    def load_string(self, string, max_size):
        self.string = string
        components = self.string.split(";")
        self.background_cells = []
        self.cells = []

        if components[0] == "V1":
            if self.init_dimensions(int(components[1]), int(components[2]), max_size):
                return False, "Level too big. Max: " + str(max_size) + "x" + str(max_size)

            self.tutorial_text = components[5]
            self.name = components[6]

            bg_cells = components[3].split(",")
            cells = components[4].split(",")
            if bg_cells != [""]:
                for bg_cell in bg_cells:
                    contents = [int(c) for c in bg_cell.split(".")]
                    self.background_cells[contents[0]][contents[1]] = celltype_e.BGPLACEABLE0
            if cells != [""]:
                for cell in cells:
                    contents = [int(c) for c in cell.split(".")]
                    self.cells[contents[2]][contents[3]] = (celltype_e(contents[0]), [0, 3, 2, 1][contents[1]])
            return True,

        elif components[0] == "V2":

            if self.init_dimensions(decode_string(components[1]), decode_string(components[2]), max_size):
                return False, "Level too big. Max: " + str(max_size) + "x" + str(max_size)

            self.tutorial_text = components[4]
            self.name = components[5]

            data = components[3]
            if data == "":
                return True,

            level_cells = ""
            data_index = 0
            data = components[3]
            while data_index < len(data):
                if data[data_index] == "(" or data[data_index] == ")":
                    if data[data_index] == ")":
                        level_cells += data[data_index - 1] * decode_string(data[data_index + 1])
                        data_index += 2
                    else:
                        cell = data[data_index - 1]
                        distance = ""
                        data_index += 1
                        while data[data_index] != ")":
                            distance += data[data_index]
                            data_index += 1

                        level_cells += cell * decode_string(distance)
                        data_index += 1
                else:
                    level_cells += data[data_index]
                    data_index += 1

            for i in range(len(level_cells)):
                self.set_cell(decode_string(level_cells[i]), i)

            return True,

        elif components[0] == "V3":

            if self.init_dimensions(decode_string(components[1]), decode_string(components[2]), max_size):
                return False, "Level too big. Max: " + str(max_size) + "x" + str(max_size)

            self.tutorial_text = components[4]
            self.name = components[5]

            level_cells = ""
            data_index = 0  # iterate through data optimally without re-slicing it every step
            data = components[3]
            while data_index < len(data):
                if data[data_index] == "(" or data[data_index] == ")":
                    if data[data_index] == ")":
                        offset = data[data_index + 1]
                        distance = data[data_index + 2]
                        data_index += 3

                    else:
                        offset = ""
                        data_index += 1
                        while data[data_index] != "(" and data[data_index] != ")":
                            offset += data[data_index]
                            data_index += 1
                        if data[data_index] == ")":
                            distance = data[data_index + 1]
                            data_index += 2
                        else:
                            distance = ""
                            data_index += 1
                            while data[data_index] != ")":
                                distance += data[data_index]
                                data_index += 1
                            data_index += 1


                    for d in range(decode_string(distance)):
                        level_cells += level_cells[-decode_string(offset) - 1]

                else:
                    level_cells += data[data_index]
                    data_index += 1
            for i in range(len(level_cells)):
                self.set_cell(decode_string(level_cells[i]), i)
            return True,

        else:
            return False, "Invalid level string"