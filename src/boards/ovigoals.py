from rgbmatrix import graphics
from PIL import ImageFont, Image
from utils import center_text
import datetime
import debug
import requests
from time import sleep
from utils import get_file
#import nhl_api.data

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
        ovi_uri = 'https://api-web.nhle.com/v1/player/8471214/landing'
        team_uri = 'https://api-web.nhle.com/v1/club-schedule-season/WSH/now'
        odata = requests.get(ovi_uri)
        tdata = requests.get(team_uri)
        oparsed = odata.json()
        tparsed = tdata.json()
        teamSeasonGames = tparsed.get('games', [])
        teamGamesLeft = sum(1 for game in teamSeasonGames if game['gameType'] == 2 and game['gameState'] != 'OFF')
        goalcount = oparsed['careerTotals']['regularSeason']['goals']
        points = oparsed['careerTotals']['regularSeason']['points']
        try:
            seasonGoals = oparsed['featuredStats']['regularSeason']['subSeason']['goals']
            seasonGames = oparsed['featuredStats']['regularSeason']['subSeason']['gamesPlayed']
        except:
            seasonGames = 0
            seasonGoals = 0
        oviGames = teamGamesLeft + seasonGames
        goalpct = 0
        if seasonGames > 0:
            goalpct = seasonGoals / seasonGames
        expectedGoals = round(oviGames * goalpct, 1)

        #for testing
        #goalcount = 908
        debug.info(f"Ovi Goals    : {goalcount}")
        debug.info(f"Ovi Points   : {points}")
        debug.info(f"season Goals : {seasonGoals}")
        debug.info(f"Games Played : {seasonGames}")
        debug.info(f"Games Left   : {teamGamesLeft}")
        debug.info(f"goalpct      : {goalpct}")
        debug.info(f"expected Goals for Games Played + Games Left : {expectedGoals}")

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

        if self.matrix.width >= 128:
            debug.info(f"Drawing 128x64 Ovi: {self.data.config.ovigoals_alt}")
            ovi_image = Image.open(get_file('assets/images/128ovi_goals.png'))
            self.matrix.draw_image((0,0), ovi_image)
        
            #draw top text        
            self.matrix.draw_text( (50,2), "OVI GOALS", font=self.font.medium, fill=(255,255,255) )

	    #draw ovi goal count
            self.matrix.draw_text( (46,18), str(goalcount), font=self.font.large, fill=(255,0,0) )
	    #draw ovi season goals or points
            if expectedGoals > 0:
                if self.data.config.ovigoals_alt:
                    self.matrix.draw_text( (86,15), "pts:", font=self.font.medium, fill=(0,233,233) )
                    self.matrix.draw_text( (86,27), f"{points}", font=self.font.medium, fill=(0,233,233) )
                    self.data.config.ovigoals_alt = False
                    debug.info(f"Setting data.config.ovigoals_alt: {self.data.config.ovigoals_alt}")
                else:
                    self.matrix.draw_text( (86,15), f"{seasonGoals}:{teamGamesLeft}", font=self.font.medium, fill=(0,233,233) )
                    self.matrix.draw_text( (86,27), f"*{expectedGoals}", font=self.font.medium, fill=(0,233,233) )
                    self.data.config.ovigoals_alt = True
                    debug.info(f"Setting data.config.ovigoals_alt: {self.data.config.ovigoals_alt}")
            else:
                self.matrix.draw_text( (90,23), f"{points}", font=self.font.medium, fill=(0,233,233) )

        
            #draw bottom text        
            self.matrix.draw_text( (66,40), str(countdowntext), font=self.font.medium, fill=(255,255,0) )
            self.matrix.draw_text( (66,51), str(countdowntext2), font=self.font.medium, fill=(255,255,0) )
            
            # self.matrix.image.save('/home/pi/pbjelly/ovi.png')
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

