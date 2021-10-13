from PIL import Image
from images.image_helper import ImageHelper

PATH = "assets/loading/loading.png"

class Loading:
    def __init__(self, matrix):
        self.matrix = matrix
        if self.matrix.width == 128:
            self.image = Image.open(PATH).resize((128,64))
        else:
            self.image = Image.open(PATH)
    def render(self):
        print('Loading...')
        self.matrix.draw_image(
            (0,0),
            self.image
        )
        self.matrix.render()
