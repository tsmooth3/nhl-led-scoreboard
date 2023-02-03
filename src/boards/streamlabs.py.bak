from rgbmatrix import graphics
from PIL import ImageFont, Image
from utils import center_text, get_file
import json
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
        font1 = ImageFont.truetype(get_file("assets/fonts/04B_24__.TTF"), 14)
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
        
        with open('../pbjelly/filter.json', 'r') as openfile:
            filterObj = json.load(openfile)
        with open('../pbjelly/softener.json', 'r') as openfile:
            softenerObj = json.load(openfile)
        sinceReset1 = url + "/v1/locations/" + locationId + "/readings/water-usage?groupBy=day&startTime=" + filterObj['resetDate']
        sinceReset2 = url + "/v1/locations/" + locationId + "/readings/water-usage?groupBy=day&startTime=" + softenerObj['resetDate']
        res1 = requests.get(sinceReset1, headers=headers)
        res2 = requests.get(sinceReset2, headers=headers)
        usage1 = sum(map(lambda x: float(x['volume']), res1.json()['readings']))
        usage2 = sum(map(lambda x: float(x['volume']), res2.json()['readings']))
        print(f"{filterObj['capacity']} - {usage1}")
        print(f"{softenerObj['capacity']} - {usage2}")
        fRemaining = int(filterObj['capacity'] - (usage1*.72))
        sRemaining = int(softenerObj['capacity'] - (usage2*.72))
        print(res1.json())
        print(res2.json())
        
        # testing response of 6 elements because today is 0
        #results.pop()
        
        pushToken = 'o.eNBIagc4Wx1imQuOehnI3RClOYdMMneP'
        pushHeaders = {'Access-Token':f'{pushToken}','Content-Type':'application/json'}
        pushUrl = 'https://api.pushbullet.com/v2/pushes'
        
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
            nowGal = 0
        if rCount == 7:
            nowGal = rVols[6]
        
        # send pushBullet
        pushPayload = json.dumps({
            "title":"StreamLabs",
            "body": f"Current Usage: {nowGal}",
            "type":"note"
        })
        # pushResponse = requests.request("POST", pushUrl, headers=pushHeaders, data=pushPayload) 
        
        # draw the stuff
        self.matrix.draw_text((32,1),  "Now".ljust(3) + ":".ljust(2),font=font1,fill=(242,242,242))
        self.matrix.draw_text((59,1),  str(nowGal).ljust(4),font=font1,fill=(242,242,242))
        
        self.matrix.draw_text((83,1),  "F*".ljust(2) + ":".ljust(2),font=font1,fill=(242,242,242))
        if fRemaining < 100:
            self.matrix.draw_text((100,1),  str(fRemaining).ljust(4),font=font1,fill=(255,255,0))
        else:
            self.matrix.draw_text((100,1),  str(fRemaining).ljust(4),font=font1,fill=(242,242,242))
        debug.info("f* " + str(fRemaining))
        
        self.matrix.draw_text((32,15), "Max".ljust(3) + ":".ljust(2),font=font1,fill=(242,242,242))
        self.matrix.draw_text((59,15), str(maxGal).ljust(4),font=font1,fill=(242,33,222))
        
        self.matrix.draw_text((83,15), "S*".ljust(2) + ":".ljust(2),font=font1,fill=(242,242,242))
        if sRemaining < 100:
            self.matrix.draw_text((100,15),  str(sRemaining).ljust(4),font=font1,fill=(255,255,0))
        else:
            self.matrix.draw_text((100,15),  str(sRemaining).ljust(4),font=font1,fill=(242,242,242))
        debug.info("s* " + str(sRemaining))
        
        self.matrix.draw_image((0,0), streamlabs_image)
        self.matrix.render()
        self.sleepEvent.wait(30)

