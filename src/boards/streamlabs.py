from rgbmatrix import graphics
from PIL import ImageFont, Image
from utils import center_text, get_file
from statistics import mean
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
        self.SL_TOKEN = ''

    def draw(self):
        debug.info("StreamLabs board launched")
        self.draw_streamlabs()

    def draw_streamlabs(self) :
        self.matrix.clear()
        font1 = ImageFont.truetype(get_file("assets/fonts/04B_24__.TTF"), 14)
        font2 = ImageFont.truetype(get_file("assets/fonts/04B_03B_.TTF"), 12)
        font3 = ImageFont.truetype(get_file("assets/fonts/04B_03__.TTF"), 12)
        font4 = ImageFont.truetype(get_file("assets/fonts/retro_computer.ttf"), 12)
        streamlabs_image = Image.open(get_file('assets/images/streamlabs.png')).resize((32,32))
        
        page = 1
        barMax = 32
        index = 0
        segment = 0
        segmentVol = 0
        dayTotal = 0
        rVols = [] 
        results = []
        bars = []
        barMax = 96+16
        chartMax = 260
        morn = (168,246,252)
        day = (55,117,176)
        evening = (99,177,213) 
        maxColor = (242,33,222)
        avgColor = (228,228,0)
        avgyColor = (245,135,0)
       
        now = datetime.today()
        startDate = now - timedelta(days=2,hours=now.hour,minutes=now.minute,seconds=now.second,microseconds=now.microsecond)
        thirtyStartDate = now - timedelta(days=30,hours=now.hour,minutes=now.minute,seconds=now.second,microseconds=now.microsecond)
        url = "https://api.streamlabswater.com"
        if self.SL_TOKEN == '':
            with open("config/streamlabs_token.txt") as f:
                self.SL_TOKEN = f.read().strip() 
        headers = {
            "Authorization" : f"Bearer {self.SL_TOKEN}"
        }
       
        locationId = requests.get(url + "/v1/locations", headers=headers).json()['locations'][0]['locationId']
        hourlyUsageUri = url + "/v1/locations/" + locationId + f"/readings/water-usage?page={page}&groupBy=hour&startTime=" + startDate.astimezone().isoformat()
        res = requests.get(hourlyUsageUri, headers=headers)
        
        thirtydayUsageUri = url + "/v1/locations/" + locationId + f"/readings/water-usage?page={page}&groupBy=day&startTime=" + thirtyStartDate.astimezone().isoformat()
        thirtydayresults = requests.get(thirtydayUsageUri, headers=headers).json()['readings']
        
        summaryUri = url + "/v1/locations/" + locationId + "/readings/water-usage/summary"
        summary = requests.get(summaryUri, headers=headers).json()

        results += res.json()['readings']
        while(page < res.json()['pageCount']):
            page += 1
            hourlyUsageUri = url + "/v1/locations/" + locationId + f"/readings/water-usage?page={page}&groupBy=hour&startTime=" + startDate.astimezone().isoformat()
            res = requests.get(hourlyUsageUri, headers=headers)
            results += res.json()['readings']

        # with open('config/softener.json', 'r') as openfile:
        #    softenerObj = json.load(openfile)
        #sinceReset2 = url + "/v1/locations/" + locationId + "/readings/water-usage?groupBy=day&startTime=" + softenerObj['resetDate']
        #res2 = requests.get(sinceReset2, headers=headers)
        #usage2 = sum(map(lambda x: float(x['volume']), res2.json()['readings']))
        #print(f"{softenerObj['capacity']} - {usage2}")
        #sRemaining = int(softenerObj['capacity'] - (usage2*.72))
        
        self.matrix.draw_rectangle((0,0),(128,64),(32,55,65))
        self.matrix.draw_image((0,-1), streamlabs_image)
        
        for r in results:
            # get the stuff
            rDate = datetime.fromisoformat(r['time'])
            rVol = math.ceil(r['volume'])

            #rDate.hour % 8 = 0
            if rDate.hour % 8 == 0:
                if len(rVols) > 0:
                    segment += 1
                    segmentVol = 0
                    index += 1
                    if segment == 3:
                        segment = 0
                        dayTotal = 0
            rVols.append({'date':rDate,'seg':segment,'vol':0,'dayTotal':0})

            # add the volume to current segment
            segmentVol += rVol
            dayTotal += rVol
            rVols[index]['date']=rDate
            rVols[index]['seg']=segment
            rVols[index]['vol']=segmentVol
            rVols[index]['dayTotal']=dayTotal
    
        # avgGal = mean(list(map(lambda x: (x['volume']), thirtydayresults)))
        avgGaly = summary['thisYear'] / 365 
        avgGal = summary['thisMonth'] / int(datetime.now().day) 
        avgBar = round((avgGal/chartMax)*barMax)
        avgyBar = round((avgGaly/chartMax)*barMax)
        maxGal = max(list(map(lambda x: (math.ceil(x['volume'])), thirtydayresults)))
        maxBar = round((maxGal/chartMax)*barMax)
        #print(f"average: {avgGal} - maxGal: {maxGal} - chartMax: {chartMax}")
        debug.info(f"average: {round(avgGal,2)} - yearAverage: {round(avgGaly,2)} - maxGal: {maxGal} - chartMax: {chartMax}")

        for v in rVols:
            bars.append(round((v['vol']/chartMax)*barMax))

        self.matrix.draw_rectangle((16+maxBar+2,28),(1,36), (242,33,222))
        for i in range(0, len(bars), 3):
            try:
                x1 = bars[i]
            except:
                x1 = 0
    
            try:
                x2 = bars[i+1]
            except:
                x2 = 0
    
            try:
                x3 = bars[i+2]
            except:
                x3 = 0

            self.matrix.draw_text((3,30+(i*4)),rVols[i]['date'].strftime("%a")[0:1],font=font4,fill=(242,242,242))
            self.matrix.draw_rectangle((16,30+(i*4)),(x1,8),morn)
            self.matrix.draw_rectangle((16+x1+1,30+(i*4)),(x2,8),day)
            self.matrix.draw_rectangle((16+x1+x2+2,30+(i*4)),(x3,8),evening)
 
        # draw the stuff
        # nowVol = math.ceil(thirtydayresults[-1]['volume'])
        nowVol = math.ceil(summary['today'])
        self.matrix.draw_text((27,1),  "Now".ljust(3) + ":".ljust(2),font=font1,fill=(242,242,242))
        self.matrix.draw_text((54,1),  str(nowVol).ljust(4),font=font1,fill=(242,242,242))
        
        #max 
        self.matrix.draw_rectangle((16+maxBar+2,28),(1,36), maxColor)
        self.matrix.draw_text((27,15), "Max".ljust(3) + ":".ljust(2),font=font1,fill=(242,242,242))
        self.matrix.draw_text((54,15), str(maxGal).ljust(4),font=font1,fill=(242,33,222))
       
        #avg 
        self.matrix.draw_rectangle((16+avgBar+2,28),(0,36), avgColor)
        self.matrix.draw_rectangle((16+avgyBar+2,28),(0,36), avgyColor)
        self.matrix.draw_text((76,1), f"{now.strftime('%b')}:",font=font1,fill=(242,242,242))
        self.matrix.draw_text((104,1), str(round(avgGal)).ljust(3),font=font1,fill=avgColor)
        self.matrix.draw_text((76,15), "A.YR:",font=font1,fill=(242,242,242))
        self.matrix.draw_text((104,15),  str(round(avgGaly)).ljust(4),font=font1,fill=avgyColor)
        
        self.matrix.render()
        self.sleepEvent.wait(30)

