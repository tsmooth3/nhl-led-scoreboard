from rgbmatrix import graphics
from PIL import ImageFont, Image
from utils import center_text
import datetime
import debug
from time import sleep
from utils import get_file

class Bears:
    def __init__(self, data, matrix,sleepEvent):
        self.data = data
        self.matrix = matrix
        self.sleepEvent = sleepEvent
        self.sleepEvent.clear()
        self.font = data.config.layout.font
        self.font.large = data.config.layout.font_large_2
        self.font.scroll = data.config.layout.font_xmas
        self.font.medium = data.config.layout.font_medium
        self.days_to_freedom = 0
        self.scroll_pos = self.matrix.width

    def draw(self):
        
        debug.info("Lets Go Bears ROAR for more board launched")
        
        self.draw_roar()

    def draw_roar(self) :
        
        self.matrix.clear()
        
        duration = 15
        i = 0
        sleep_rate = .05
        frame_nub = 0

        while not self.sleepEvent.is_set():
        
            image = Image.open(get_file('assets/images/owen_roar.gif'))

            self.matrix.clear()
            try:
                image.seek(frame_nub)
            except EOFError:
                frame_nub = 0
                image.seek(frame_nub)
            #draw gif
            self.matrix.draw_image((0, 0), image.resize((128,64)))
            
            i += sleep_rate
            frame_nub += 1
            self.matrix.render()
            self.sleepEvent.wait(sleep_rate)
            if(i > duration) : break
