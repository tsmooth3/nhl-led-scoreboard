from rgbmatrix import graphics
from PIL import ImageFont, Image
from utils import center_text
import datetime
import debug
from time import sleep
from utils import get_file

class Easter:
    def __init__(self, data, matrix,sleepEvent):
        self.data = data
        self.matrix = matrix
        self.sleepEvent = sleepEvent
        self.sleepEvent.clear()
        self.font = data.config.layout.font
        self.font.large = data.config.layout.font_large_2
        self.font.scroll = data.config.layout.font_xmas
        self.font.medium = data.config.layout.font_medium
        self.days_to_easter = 0
        self.scroll_pos = self.matrix.width

    def draw(self):
        
        debug.info("Easter board launched")
        
        self.calc_days_to_easter()

        #for testing purposes
        #self.days_to_easter = 0

        debug.info(str(self.days_to_easter) + " days to Easter")

        if self.days_to_easter == 0:
            #today is Easter
            self.easter_today()

        else:
            #today is not Easter
            if self.days_to_easter < 50: 
                self.easter_countdown()

    def calc_easter(self, year):
        #find easter for 'year'
        y = year
        a = y // 100
        b = y % 100
        c = (3 * (a + 25)) // 4
        d = (3 * (a + 25)) % 4
        e = (8 * (a + 11)) // 25
        f = (5 * a + b) % 19
        g = (19 * f + c - e) % 30
        h = (f + 11 * g) // 319
        j = (60 * (5 - d) + b) // 4
        k = (60 * (5 - d) + b) % 4
        m = (2 * j - k - g + h) % 7
        n = (g - h + m + 114) // 31
        p = (g - h + m + 114) % 31
        dy = p + 1
        mth = n
        easter = datetime.date(y, mth, dy)
        return easter
 
    def calc_days_to_easter(self):
        #get today's date
        today = datetime.date(
            datetime.datetime.now().year,
            datetime.datetime.now().month,            
            datetime.datetime.now().day
            )
        
        next_easter = self.calc_easter(today.year)

        if today > next_easter:
            next_easter = self.calc_easter(today.year + 1) 

        #calculate days to easter
        self.days_to_easter = (next_easter - today).days
    
    def easter_today(self) :
        #  it's Easter!

        duration = 7
        i = 0
        scroll_rate = .0001
            
        debug.info("It's Easter!")

        while not self.sleepEvent.is_set():

            self.matrix.clear()

            easter_scroll_text = self.matrix.draw_text(
                (self.scroll_pos,12),
                "Christ is Risen! Alleluia! Happy Easter!",
                font=self.font.scroll,
                fill=(240,240,240)
                )
            
            easter_scroll_text_width = easter_scroll_text["size"][0] + 3
            
            easter_image = Image.open(get_file('assets/images/easter.jpg')).resize((64,64))
            self.matrix.draw_image((self.scroll_pos + easter_scroll_text_width,4), easter_image)

            easter_content_width = easter_scroll_text_width + 48

            if(self.scroll_pos < (0 - easter_content_width) ): self.scroll_pos = self.matrix.width

            i += scroll_rate
            self.scroll_pos -= 1

            self.matrix.render()
            #sleep(scroll_rate)
            self.sleepEvent.wait(scroll_rate)

            if(i > duration) : break

    def easter_countdown(self) :
        
        self.matrix.clear()
        
        debug.info("Counting down to Easter!")

        easter_image = Image.open(get_file('assets/images/lent.jpg')).resize((128,64))
        self.matrix.draw_image((0,0), easter_image)
        
        #draw days to easter
        self.matrix.draw_text(
            (10,33),
            str(self.days_to_easter),
             font=self.font.large,
             fill=(240,240,240)
        )
        
           
        #draw bottom text        
        self.matrix.draw_text(
            (10,52), 
            "DAYS TO EASTER", 
            font=self.font.medium,
            fill=(240,240,240)
        )

        self.matrix.render()
        self.sleepEvent.wait(15)
