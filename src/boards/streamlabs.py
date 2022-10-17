from rgbmatrix import graphics
from PIL import ImageFont, Image
from utils import center_text, get_file
import debug
import requests
import time
import math
from datetime import datetime, timedelta

class StreamLabs:
    def __init__(self, data, matrix,sleepEvent):
        self.data = data
        self.matrix = matrix
        self.sleepEvent = sleepEvent
        self.sleepEvent.clear()
        self.font = data.config.layout.font
        self.font.monofont = data.config.layout.wxalert_font
        self.font.large = data.config.layout.font_large_2
        self.font.medium = data.config.layout.font_medium
        self.font.scroll = data.config.layout.font_xmas
        self.scroll_pos = self.matrix.width

    def draw(self):
        debug.info("StreamLabs board launched")
        self.draw_streamlabs()

    def draw_streamlabs(self) :
        self.matrix.clear()
        font1 = ImageFont.truetype(get_file("assets/fonts/04B_24__.TTF"), 12)
        font2 = ImageFont.truetype(get_file("assets/fonts/04B_03B_.TTF"), 12)
        font3 = ImageFont.truetype(get_file("assets/fonts/04B_03__.TTF"), 12)
        font4 = ImageFont.truetype(get_file("assets/fonts/retro_computer.ttf"), 12)
        now = datetime.today()
        startDate = now - timedelta(days=6,hours=now.hour,minutes=now.minute,seconds=now.second,microseconds=now.microsecond)
        url = "https://api.streamlabswater.com"
        headers = {
            "Authorization" : "Bearer CbZt2qUVD0isylKyJ3cpQh6Dk94T7rq7wGtKOg5RlBjBnQ-8ralB9Q"
        }
        barMax = 32
        streamlabs_image = Image.open(get_file('assets/images/streamlabs.png')).resize((32,32))
        res = requests.get(url + "/v1/locations", headers=headers)
        locationId = res.json()['locations'][0]['locationId']
        usageUri = url + "/v1/locations/" + locationId + "/readings/water-usage?groupBy=day&startTime=" + startDate.astimezone().isoformat()
        res = requests.get(usageUri, headers=headers)
        results = res.json()['readings']
        
        # testing response of 6 elements because today is 0
        #results.pop()
       
        rCount = len(results)
        self.matrix.draw_rectangle((0,0),(128,64),(32,55,65))
        bars = []
        rVols = []
        rDates = []
        for r in results:
            rDate = datetime.fromisoformat(r['time'])
            rVol = math.ceil(r['volume'])
            rVols.append(rVol)
            rDates.append(rDate)
            debug.info(str(rDate.month) + "/" + str(rDate.day) + " : " + rDate.strftime("%a")[0:1] + " : " + str(rVol))
        maxGal = max(rVols)
        for v in rVols:
            bars.append(round((v/maxGal)*barMax))
        for x in range(rCount):
            if rVols[x] == maxGal:
                x1 = 3+3*6*x
                x2 = 15
                y1 = 64
                y2 = -bars[x]
                debug.info(str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2))
                self.matrix.draw_rectangle((x1,y1),(x2,y2),(242,33,222))
            if rVols[x] != maxGal:
                x1 = 3+3*6*x
                x2 = 15
                y1 = 64
                y2 = -bars[x]
                debug.info(str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2))
                self.matrix.draw_rectangle((x1,y1),(x2,y2), (0,180,220))
            self.matrix.draw_text((5+3*6*x,50),rDates[x].strftime("%a")[0:1],font=font4,fill=(242,242,242))
        if rCount == 6:
            self.matrix.draw_text((5+3*6*6,50),now.strftime("%a")[0:1],font=font4,fill=(242,242,242))
            self.matrix.draw_text((83,1),  "0".ljust(4),font=font4,fill=(242,242,242))
        if rCount == 7:
            self.matrix.draw_text((83,1),  str(rVols[6]).ljust(4),font=font4,fill=(242,242,242))
        self.matrix.draw_text((33,1),  "Now".ljust(4) + ":".ljust(2),font=font4,fill=(242,242,242))
        self.matrix.draw_text((33,15), "Max".ljust(4) + ":".ljust(2),font=font4,fill=(242,242,242))
        self.matrix.draw_text((83,15), str(maxGal).ljust(4),font=font4,fill=(242,33,222))
        self.matrix.draw_image((0,0), streamlabs_image)
        self.matrix.render()
        self.sleepEvent.wait(30)

