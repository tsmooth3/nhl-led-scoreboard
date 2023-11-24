from rgbmatrix import graphics
from PIL import ImageFont, Image
from utils import center_text
from datetime import datetime, date
import debug
import requests
from time import sleep
from utils import get_file

PATH = 'assets/logos'
LOGO_LINK = "https://www-league.nhlstatic.com/images/logos/league-dark/133-flat.svg"

class SeasonCountdown:
    def __init__(self, data, matrix,sleepEvent):
        
        self.data = data
        self.matrix = matrix
        self.sleepEvent = sleepEvent
        self.sleepEvent.clear()
        self.font = data.config.layout.font
        self.font.large = data.config.layout.font_large
        self.font.large2 = data.config.layout.font_large_2
        # Current season seems to not update until pre-season start so I will have to modify the Status and the nhl_api to get the coming season.
        # self.season_start = datetime(2023, 10, 7).date()
        season_uri = 'https://api.nhle.com/stats/rest/en/season?sort=%5B%7B%22property%22:%22id%22,%22direction%22:%22DESC%22%7D%5D'
        season_response = requests.get(season_uri).json()['data'][0]['startDate']
        self.season_start = datetime.strptime(season_response, '%Y-%m-%dT%H:%M:%S').date()
        #self.season_start = datetime.strptime(self.data.status.next_season_start(), '%Y-%m-%d').date()
        self.days_until_season = (self.season_start - date.today()).days
        self.scroll_pos = self.matrix.width
        
        # Set up season text
        current_year = date.today().year
        next_year = current_year + 1
    
        self.nextseason="{0}-{1}".format(current_year,next_year)
        self.nextseason_short="NHL {0}-{1}".format(str(current_year)[-2:],str(next_year)[-2:])

    def draw(self):
        
        debug.info("NHL Countdown Launched")

        #for testing purposes
        #self.days_until_season = 0

        debug.info(str(self.days_until_season) + " days to NHL Season")

        if self.days_until_season <= 0:
            debug.info("It's NHL Season Time!")
        else:
            self.season_countdown()
  
    
    def season_start_today(self) :
        #  it's just like Christmas!
        self.matrix.clear()

        nhl_logo = Image.open(get_file('assets/logos/_local/nhl_logo_64x32.png'))

        self.matrix.draw_image((15,0), nhl_logo)
        
        debug.info("{0} season has begun".format(self.nextseason))

        self.matrix.render()
        self.sleepEvent.wait(0.5)


        #draw bottom text        
        self.matrix.draw_text(
            (14,25), 
            self.nextseason, 
            font=self.font,
            fill=(0,0,0),
            backgroundColor=(155,155,155)
        )
        self.matrix.render()
        self.sleepEvent.wait(15)

    def season_countdown(self) :
        
        self.matrix.clear()

        nhl_logo = Image.open(get_file('assets/logos/_local/nhl_logo_64x32.png')).resize((62,66))
        black_gradiant = Image.open(get_file('assets/images/64x32_scoreboard_center_gradient.png')).resize((128,64))

        self.matrix.draw_image((68,0), nhl_logo)
        #self.matrix.draw_image((-5,0), black_gradiant)
        
        debug.info("Counting down to {0}".format(self.nextseason_short))

        self.matrix.render()
        self.sleepEvent.wait(0.5)

        #draw days to xmas
        self.matrix.draw_text(
            (10,10),
            str(self.days_until_season),
             font=self.font.large2,
             fill=(252,15,30)
        )
        
        self.matrix.render()
        self.sleepEvent.wait(1)

        #draw bottom text        
        self.matrix.draw_text(
            (10,30), 
            "DAYS til", 
            font=self.font.large,
            fill=(252,15,30)
        )

        self.matrix.render()
        self.sleepEvent.wait(1)

        #draw bottom text        
        self.matrix.draw_text(
            (10,45), 
            self.nextseason_short, 
            font=self.font.large,
            fill=(0,0,0),
            backgroundColor=(155,155,155)
        )

        self.matrix.render()
        self.sleepEvent.wait(15)
