from rgbmatrix import graphics
from PIL import ImageFont, Image
from utils import center_text
import datetime
import debug
from time import sleep
from utils import get_file

class Bday1001:
    def __init__(self, data, matrix,sleepEvent):
        self.data = data
        self.matrix = matrix
        self.sleepEvent = sleepEvent
        self.sleepEvent.clear()
        self.font = data.config.layout.font
        self.font.large = data.config.layout.font_large_2
        self.font.scroll = data.config.layout.font_xmas
        self.font.medium = data.config.layout.font_medium
        self.days_to_next_birthday = 0
        self.days_old = 0
        self.age = 0
        self.who = "Chloe"
        self.birthday = datetime.date( 2009, 10, 1 )
        self.bday_image = Image.open(get_file('assets/images/bday1001.jpg')).resize((64,64))
        self.scroll_pos = self.matrix.width

    def draw(self):
        debug.info(f"{self.who} {self.birthday} Birthday countdown board launched")
        self.calc_days_to_birthday()
        #for testing purposes
        #self.days_to_birthday = 0

        debug.info(str(self.days_to_birthday) + " days")

        if self.days_to_birthday < 1 or self.days_to_birthday > 363:
            #today is Birthday
            self.birthday_today()
        else:
            #today is not birthday
            if self.days_to_birthday < 102:
                self.birthday_countdown()

    def calc_days_to_birthday(self):
        #get todays date
        today = datetime.date( datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
        this_year_bday = datetime.date ( today.year, self.birthday.month, self.birthday.day)
        next_year_bday = datetime.date ( today.year + 1, self.birthday.month, self.birthday.day)
        if today > this_year_bday:
            thebday = next_year_bday
        else:
            thebday = this_year_bday

        self.age = round((thebday - self.birthday).days / 365.2425)
        #calculate days to bday
        self.days_to_birthday = (thebday - today).days
        self.days_old = (today - this_year_bday).days
        if self.days_to_birthday > 363:
            self.age = self.age - 1
    
    def birthday_today(self) :
        #  it's Party Time!
        duration = 15
        i = 0
        sleep_rate = .1
        debug.info("It's Birthday Time!")
        while not self.sleepEvent.is_set():
            self.matrix.clear()
            self.matrix.draw_image((0,0), self.bday_image)
            self.matrix.draw_text( (67,2), "Happy", font=self.font.medium, fill=(150,150,150) ) 
            self.matrix.draw_text( (67,17), "Birthday", font=self.font.medium, fill=(150,150,150) ) 
            self.matrix.draw_text( (67,32), f"{self.who}!", font=self.font.medium, fill=(150,150,150) ) 
            self.matrix.draw_text( (67,47), f"You're {self.age}", font=self.font.medium, fill=(150,150,150) ) 
            i += sleep_rate
            self.matrix.render()
            self.sleepEvent.wait(sleep_rate)
            if(i > duration) : break

    def birthday_countdown(self) :
        self.matrix.clear()
        debug.info("Counting down to Birthday!")
        #check for three-digit countdown
        if self.days_to_birthday < 10:
            if self.days_to_birthday < 2:
                countdown_text = f"in {self.days_to_birthday} DAY"
            else:
                countdown_text = f"{self.days_to_birthday} DAYS"
        else:
            countdown_text = f"{self.days_to_birthday} DAYS"  

        duration = 7
        i = 0
        sleep_rate = .05

        while not self.sleepEvent.is_set():
            self.matrix.clear()
            self.matrix.draw_image((0,0), self.bday_image)
            self.matrix.draw_text( (67,2), countdown_text, font=self.font.medium, fill=(150,150,150) ) 
            self.matrix.draw_text( (67,17), f"{self.who}", font=self.font.medium, fill=(150,150,150) ) 
            self.matrix.draw_text( (67,32), f"Turns {self.age}", font=self.font.medium, fill=(150,150,150) ) 
            i += sleep_rate
            self.matrix.render()
            self.sleepEvent.wait(sleep_rate)
            if(i > duration) : break
