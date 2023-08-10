from rgbmatrix import graphics
from PIL import ImageFont, Image
from utils import center_text
import datetime
import debug
from time import sleep
from utils import get_file
import nhl_api.data

class OviGoals:
    def __init__(self, data, matrix,sleepEvent):
        self.data = data
        self.matrix = matrix
        self.sleepEvent = sleepEvent
        self.sleepEvent.clear()
        self.font = data.config.layout.font
        self.font.large = data.config.layout.font_large_2
        self.font.medium = data.config.layout.font_medium
        self.font.scroll = data.config.layout.font_xmas
        self.scroll_pos = self.matrix.width

    def draw(self):
        
        debug.info("OviGoals board launched")

        self.draw_ovi_goals()
  
    def draw_ovi_goals(self) :
        
        self.matrix.clear()
        odata = nhl_api.data.get_ovi_goals()
        oparsed = odata.json()
        goalcount = oparsed["stats"][0]["splits"][0]["stat"]['goals']
        #for testing
        #goalcount = 908
        debug.info(str(goalcount) + " Ovi Goals")
        jagr = 767
        howe = 802
        gretzky = 895

        goalsTo3rd = jagr - goalcount
        goalsTo2nd = howe - goalcount
        goalsTo1st = gretzky - goalcount
        countdowntext = "3rd:-" + str(goalsTo3rd) 
        countdowntext2 = "2nd:-" + str(goalsTo2nd)
     
        if goalsTo3rd < 1:
            #3rd place
            countdowntext = "2nd:-" + str(goalsTo2nd) 
            countdowntext2 = "1st:-" + str(goalsTo1st)
        if goalsTo2nd < 1:
            #2nd place
            countdowntext = str(goalsTo1st) + " to go"
            countdowntext2 = "for 1st"
        if goalsTo1st < 1:
            #1st place
            countdowntext = "BEST )))" 
            countdowntext2 = "+" + str(goalsTo1st * -1 + 1)

        if self.matrix.width == 128:
            debug.info("Drawing 128x64 Ovi")
            ovi_image = Image.open(get_file('assets/images/128ovi_goals.png'))
            self.matrix.draw_image((0,0), ovi_image)
        
            #draw top text        
            self.matrix.draw_text(
                (56,2), 
                "OVI GOALS", 
                font=self.font.medium,
                fill=(255,255,255)
            )

	    #draw ovi goal count
            self.matrix.draw_text(
                (68,18),
                str(goalcount),
                font=self.font.large,
                fill=(255,0,0)
            )
        
            #draw bottom text        
            self.matrix.draw_text(
                (66,38), 
                str(countdowntext), 
                font=self.font.medium,
                fill=(255,255,0)
            )
            #draw bottom text        
            self.matrix.draw_text(
                (66,50), 
                str(countdowntext2), 
                font=self.font.medium,
                fill=(255,255,0)
            )
            self.matrix.image.save('/home/pi/pbjelly/ovi.png')
        else: 
            debug.info("Drawing 64x32 Ovi")
            ovi_image = Image.open(get_file('assets/images/ovi_goals.png'))
            self.matrix.draw_image((0,0), ovi_image)
        
            #draw top text        
            self.matrix.draw_text(
                (34,1), 
                "OVECHKIN", 
                font=self.font,
                fill=(255,255,255)
            )

	    #draw ovi goal count
            self.matrix.draw_text(
                (39,11),
                str(goalcount),
                font=self.font.medium,
                fill=(255,0,0)
            )
        
            #draw bottom text        
            self.matrix.draw_text(
                (39,26), 
                "GOALS", 
                font=self.font,
                fill=(255,255,255)
            )

        self.matrix.render()
        self.sleepEvent.wait(15)
