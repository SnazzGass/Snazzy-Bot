from PIL import Image
import os

from level import Level
from celltype_enum import celltype_e


texture_path = "./textures"


textures = {}

for file in os.listdir(texture_path):
    if os.path.splitext(file)[0].upper() in celltype_e.__members__:
        textures[celltype_e[os.path.splitext(file)[0].upper()]] = Image.open("/".join((texture_path, file)))


class Preview:
    def __init__(self, max_level_size):
        self.max_level_size = max_level_size
        self.level = Level()
        self.width = None
        self.height = None
        self.tex_size = None
        self.preview_image = None

    def preview(self, level_string, default_color=(42, 42, 42, 255), texture_size=16):
        self.tex_size = texture_size
        try:
            load_result = self.level.load_string(level_string, self.max_level_size)
            if load_result[0] is False:
                return False, load_result[1]
        except:
            return False, "Invalid level string"

        if self.level.width <= 0 and self.level.height <= 0:
            return False, "Invalid level size"

        self.width = self.level.width * texture_size
        self.height = self.level.height * texture_size

        self.preview_image = Image.new("RGBA", (self.width, self.height), default_color)

        for x_index in range(self.level.width):
            for y_index in range(self.level.height):
                self.paste_cell_image(x_index, y_index, textures[self.level.background_cells[x_index][y_index]])
                if self.level.cells[x_index][y_index] is not None:
                    self.paste_cell_image(x_index, y_index,
                                          textures[self.level.cells[x_index][y_index][0]],
                                          self.level.cells[x_index][y_index][1])

        return True, self.level.name, self.level.tutorial_text

    def paste_cell_image(self, x, y, cell_image, rotation=0):
        cell_image_r = cell_image.rotate(rotation * 90)
        self.preview_image.paste(cell_image_r, (x * self.tex_size, self.height - (y + 1) * self.tex_size), cell_image_r)

    def save_image(self, max_width=1024, max_height=1024):
        scale_factor = 1
        sample_mode = Image.BILINEAR
        if self.width * self.height != 0:
            scale_factor = min(max_width / self.width, max_height / self.height)
            if scale_factor > 1:
                sample_mode = Image.NEAREST

        img = self.preview_image.resize((int(self.width * scale_factor), int(self.height * scale_factor)), sample_mode)
        img.save("preview.png", "PNG")
