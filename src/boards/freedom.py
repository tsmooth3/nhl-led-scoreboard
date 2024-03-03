from rgbmatrix import graphics
from PIL import ImageFont, Image
from utils import center_text
import datetime
import debug
from time import sleep
from utils import get_file

class Freedom:
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
        
        debug.info("Freedom board launched")
        
        self.calc_days_to_freedom()

        #for testing purposes
        #self.days_to_freedom = 0

        debug.info(str(self.days_to_freedom) + " days to fourth")

        if self.days_to_freedom < 1:
            #today is fourth
            self.freedom_today()

        else:
            #today is not Fourth
            self.freedom_countdown()

    def get_partyday(self, x):
        if x.weekday() ==  0:
            return x - datetime.timedelta(days=2)
        if x.weekday() ==  1:
            return x - datetime.timedelta(days=3)
        if x.weekday() ==  2:
            return x + datetime.timedelta(days=3)
        if x.weekday() ==  3:
            return x + datetime.timedelta(days=2)
        if x.weekday() ==  4:
            return x + datetime.timedelta(days=1)
        if x.weekday() ==  5:
            return x + datetime.timedelta(days=0)
        if x.weekday() ==  6:
            return x - datetime.timedelta(days=1)
 
    def calc_days_to_freedom(self):
        #get today's date
        today = datetime.date( datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
        thefourth = datetime.date( today.year, 7, 4 )
        partyday = self.get_partyday(thefourth)
        if today > thefourth and today > partyday:
            thefourth = datetime.date( today.year + 1, 7, 4 )
            partyday = self.get_partyday(thefourth)

        #calculate days to freedom
        self.days_to_freedom = (partyday - today).days
    
    def freedom_today(self) :
        #  it's Party Time!
        
        scrollText =  "I am apt to belive\n"
        scrollText += "will be celebrated\n"
        scrollText += "by Generations\n"
        scrollText += "a great anniversary\n"
        scrollText += "commemorated day\n"
        scrollText += "of Deliverance\n"
        scrollText += "Acts of Devotion\n"
        scrollText += "to God Almighty\n"
        scrollText += "to be solemnized\n"
        scrollText += "with Pomp & Parade\n"
        scrollText += "Shews Games Sports\n"
        scrollText += "Guns Bells Bonfires\n"
        scrollText += "and Illuminations\n"
        scrollText += "forever more!!!"

        duration = 15
        i = 0
        scroll_rate = .05
        sleep_rate = .1
        debug.info("It's Freedom Time!")
        scroll_pos = 12
        frame_nub = 0
        content_height = 125
        t_now = datetime.datetime.now().minute
        while not self.sleepEvent.is_set():
            #choose one of three daily images to draw based on days to xmas and draw it
            if t_now % 3 == 0:
                if t_now % 2 == 0:
                    freedom_image = Image.open(get_file('assets/images/fireworks.gif'))
                    x_pos = 0
                    y_pos = 0
                else:
                    freedom_image = Image.open(get_file('assets/images/64flag.gif'))
                    x_pos = 8
                    y_pos = -4
                self.matrix.clear()
                try:
                    freedom_image.seek(frame_nub)
                except EOFError:
                    frame_nub = 0
                    freedom_image.seek(frame_nub)
                #draw gif
                if t_now % 2 == 0:
                    self.matrix.draw_image((x_pos, y_pos), freedom_image.resize((128,64)))
                else:
                    self.matrix.draw_image((x_pos, y_pos), freedom_image)
                    
                #draw days to freedom
                self.matrix.draw_text( (10,50), "FREEDOM !!!", font=self.font.large, fill=(150,150,150) )
                #increment counters
                i += scroll_rate
                frame_nub += 1
                self.matrix.render()
                self.sleepEvent.wait(scroll_rate)
                if(i > duration) : break
            else:
                self.matrix.clear()
                scroll_text = self.matrix.draw_text( (1,scroll_pos), scrollText, font=self.font.medium, fill=(200,200,200) )
                scroll_pos -= 1
                debug.info(f"scroll_pos: {scroll_pos}  {(0-content_height)}")
                if(scroll_pos < (0 - content_height) ): scroll_pos = 12
                self.matrix.render()
            
                i += scroll_rate
                self.sleepEvent.wait(sleep_rate)
                if(i > duration) : break

    def freedom_countdown(self) :
        
        self.matrix.clear()
        
        debug.info("Counting down to Freedom!")
        #check for three-digit countdown
        if self.days_to_freedom < 10:
            x_pos = 32
            if self.days_to_freedom < 2:
                countdown_text = f"{self.days_to_freedom} DAY!"
            else:
                countdown_text = f"{self.days_to_freedom} DAYS"
        elif self.days_to_freedom < 99:
            x_pos = 25
            countdown_text = f"{self.days_to_freedom} DAYS"
        else:
            x_pos = 19
            countdown_text = f"{self.days_to_freedom} DAYS"

        duration = 15
        i = 0
        sleep_rate = .05
        frame_nub = 0

        while not self.sleepEvent.is_set():
        
            #choose one of three daily images to draw based on days to xmas and draw it
            if self.days_to_freedom % 3 == 0:
                freedom_image = Image.open(get_file('assets/images/64flag.gif'))
            elif self.days_to_freedom % 3 == 2:
                freedom_image = Image.open(get_file('assets/images/64flag.gif'))
            else:
                freedom_image = Image.open(get_file('assets/images/64flag.gif'))

            self.matrix.clear()
            try:
                freedom_image.seek(frame_nub)
            except EOFError:
                frame_nub = 0
                freedom_image.seek(frame_nub)
            #draw gif
            self.matrix.draw_image((8, -4), freedom_image)
            
            #draw days to freedom
            self.matrix.draw_text( (x_pos,50), countdown_text, font=self.font.large, fill=(150,150,150) )
            
            #debug.info(f"duration {i}")
            i += sleep_rate
            frame_nub += 1
            self.matrix.render()
            self.sleepEvent.wait(sleep_rate)
            if(i > duration) : break
