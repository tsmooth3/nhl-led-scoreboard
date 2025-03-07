"""
A Board is simply a display object with specific parameters made to be shown on screen.
    TODO: Make the board system customizable so that all the user needs to do is paste a board file and modify the
        config file to add the custom board.
"""
import debug
from boards.scoreticker import Scoreticker
# from boards.seriesticker import Seriesticker
from boards.standings import Standings
from boards.team_summary import TeamSummary
from boards.clock import Clock
#from boards.covid_19 import Covid_19
from boards.pbdisplay import pbDisplay
from boards.wxWeather import wxWeather
from boards.wxAlert import wxAlert
from boards.christmas import Christmas
from boards.seasoncountdown import SeasonCountdown
from boards.wxForecast import wxForecast
from boards.screensaver import screenSaver
from boards.ovigoals import OviGoals
from boards.bday0115 import Bday0115
from boards.bday0201 import Bday0201
from boards.bday0306 import Bday0306
from boards.bday0330 import Bday0330
from boards.bday0403 import Bday0403
from boards.bday0503 import Bday0503
from boards.bday0727 import Bday0727
from boards.bday0803 import Bday0803
from boards.bday1001 import Bday1001
from boards.bday1112 import Bday1112
from boards.streamlabs import StreamLabs
from boards.easter import Easter
from boards.freedom import Freedom
from boards.stanley_cup_champions import StanleyCupChampions
from boards.ovigoals import OviGoals
from boards.freedom import Freedom
from boards.birthday0115 import Birthday0115
from boards.birthday0201 import Birthday0201
from boards.birthday0330 import Birthday0330
from boards.birthday0403 import Birthday0403
from boards.birthday0727 import Birthday0727
from boards.birthday1001 import Birthday1001
from boards.birthday1112 import Birthday1112
from time import sleep

import traceback

class Boards:
    def __init__(self):
        pass

    # Board handler for PushButton
    def _pb_board(self, data, matrix, sleepEvent):

        board = getattr(self, data.config.pushbutton_state_triggered1)
        board(data, matrix, sleepEvent)

    # Board handler for Weather Alert
    def _wx_alert(self, data, matrix, sleepEvent):

        board = getattr(self, "wxalert")
        board(data, matrix, sleepEvent)

    # Board handler for screensaver
    def _screensaver(self, data, matrix, sleepEvent):

        board = getattr(self, "screensaver")
        board(data, matrix, sleepEvent)

    # Board handler for Off day state
    def _off_day(self, data, matrix, sleepEvent):
        bord_index = 0
        while True:
            board = getattr(self, data.config.boards_off_day[bord_index])
            data.curr_board = data.config.boards_off_day[bord_index]

            if data.pb_trigger:
                debug.info('PushButton triggered....will display ' + data.config.pushbutton_state_triggered1 + ' board ' + "Overriding off_day -> " + data.config.boards_off_day[bord_index])
                if not data.screensaver:
                    data.pb_trigger = False
                board = getattr(self,data.config.pushbutton_state_triggered1)
                data.curr_board = data.config.pushbutton_state_triggered1
                bord_index -= 1

            # Display the Weather Alert board
            if data.wx_alert_interrupt:
                debug.info('Weather Alert triggered in off day loop....will display weather alert board')
                data.wx_alert_interrupt = False
                #Display the board from the config
                board = getattr(self,"wxalert")
                data.curr_board = "wxalert"
                bord_index -= 1

            # Display the Screensaver Board
            if data.screensaver:
                if not data.pb_trigger:
                    debug.info('Screensaver triggered in off day loop....')
                    #Display the board from the config
                    board = getattr(self,"screensaver")
                    data.curr_board = "screensaver"
                    data.prev_board = data.config.boards_off_day[bord_index]
                    bord_index -= 1
                else:
                    data.pb_trigger = False

            board(data, matrix, sleepEvent)

            if bord_index >= (len(data.config.boards_off_day) - 1):
                return
            else:
                if not data.pb_trigger or not data.wx_alert_interrupt or not data.screensaver:
                    bord_index += 1

    def _scheduled(self, data, matrix, sleepEvent):
        bord_index = 0
        while True:
            board = getattr(self, data.config.boards_scheduled[bord_index])
            data.curr_board = data.config.boards_scheduled[bord_index]
            if data.pb_trigger:
                debug.info('PushButton triggered....will display ' + data.config.pushbutton_state_triggered1 + ' board ' + "Overriding scheduled -> " + data.config.boards_scheduled[bord_index])
                if not data.screensaver:
                    data.pb_trigger = False
                board = getattr(self,data.config.pushbutton_state_triggered1)
                data.curr_board = data.config.pushbutton_state_triggered1
                bord_index -= 1

            # Display the Weather Alert board
            if data.wx_alert_interrupt:
                debug.info('Weather Alert triggered in scheduled loop....will display weather alert board')
                data.wx_alert_interrupt = False
                #Display the board from the config
                board = getattr(self,"wxalert")
                data.curr_board = "wxalert"
                bord_index -= 1

            # Display the Screensaver Board
            if data.screensaver:
                if not data.pb_trigger:
                    debug.info('Screensaver triggered in scheduled loop....')
                    #Display the board from the config
                    board = getattr(self,"screensaver")
                    data.curr_board = "screensaver"
                    data.prev_board = data.config.boards_off_day[bord_index]
                    bord_index -= 1
                else:
                    data.pb_trigger = False

            board(data, matrix, sleepEvent)

            if bord_index >= (len(data.config.boards_scheduled) - 1):
                return
            else:
                if not data.pb_trigger or not data.wx_alert_interrupt or not data.screensaver:
                    bord_index += 1

    def _intermission(self, data, matrix, sleepEvent):
        bord_index = 0
        while True:
            board = getattr(self, data.config.boards_intermission[bord_index])
            data.curr_board = data.config.boards_intermission[bord_index]

            if data.pb_trigger:
                debug.info('PushButton triggered....will display ' + data.config.pushbutton_state_triggered1 + ' board ' + "Overriding intermission -> " + data.config.boards_intermission[bord_index])
                if not data.screensaver:
                    data.pb_trigger = False
                board = getattr(self,data.config.pushbutton_state_triggered1)
                data.curr_board = data.config.pushbutton_state_triggered1
                bord_index -= 1

            # Display the Weather Alert board
            if data.wx_alert_interrupt:
                debug.info('Weather Alert triggered in intermission....will display weather alert board')
                data.wx_alert_interrupt = False
                #Display the board from the config
                board = getattr(self,"wxalert")
                data.curr_board = "wxalert"
                bord_index -= 1

            ## Don't Display the Screensaver Board in "live game mode"
            # if data.screensaver:
            #     if not data.pb_trigger:
            #         debug.info('Screensaver triggered in intermission loop....')
            #         #Display the board from the config
            #         board = getattr(self,"screensaver")
            #         data.curr_board = "screensaver"
            #         data.prev_board = data.config.boards_off_day[bord_index]
            #         bord_index -= 1
            #     else:
            #         data.pb_trigger = False
        
            board(data, matrix, sleepEvent)

            if bord_index >= (len(data.config.boards_intermission) - 1):
                return
            else:
                if not data.pb_trigger or not data.wx_alert_interrupt or not data.screensaver:
                    bord_index += 1

    def _post_game(self, data, matrix, sleepEvent):
        bord_index = 0
        while True:
            board = getattr(self, data.config.boards_post_game[bord_index])
            data.curr_board = data.config.boards_post_game[bord_index]

            if data.pb_trigger:
                debug.info('PushButton triggered....will display ' + data.config.pushbutton_state_triggered1 + ' board ' + "Overriding post_game -> " + data.config.boards_post_game[bord_index])
                if not data.screensaver:
                    data.pb_trigger = False
                board = getattr(self,data.config.pushbutton_state_triggered1)
                data.curr_board = data.config.pushbutton_state_triggered1
                bord_index -= 1

            # Display the Weather Alert board
            if data.wx_alert_interrupt:
                debug.info('Weather Alert triggered in post game loop....will display weather alert board')
                data.wx_alert_interrupt = False
                #Display the board from the config
                board = getattr(self,"wxalert")
                data.curr_board = "wxalert"
                bord_index -= 1

            # Display the Screensaver Board
            if data.screensaver:
                if not data.pb_trigger:
                    debug.info('Screensaver triggered in post game loop....')
                    #Display the board from the config
                    board = getattr(self,"screensaver")
                    data.curr_board = "screensaver"
                    data.prev_board = data.config.boards_off_day[bord_index]
                    bord_index -= 1
                else:
                    data.pb_trigger = False


            board(data, matrix, sleepEvent)

            if bord_index >= (len(data.config.boards_post_game) - 1):
                return
            else:
                if not data.pb_trigger or not data.wx_alert_interrupt or not data.screensaver:
                    bord_index += 1

    def fallback(self, data, matrix, sleepEvent):
        Clock(data, matrix, sleepEvent)

    def scoreticker(self, data, matrix, sleepEvent):
        Scoreticker(data, matrix, sleepEvent).render()

    # Since 2024, the playoff features are removed as we have not colected the new API endpoint for them. 
    def seriesticker(self, data, matrix, sleepEvent):
        debug.info("seriesticker is disabled. This feature is not available right now")
        pass
        '''
            forcing it to show since the playoff start and regular season end are in conflict for 2021
        '''
        
        #Seriesticker(data, matrix, sleepEvent).render()
        
        '''if data.status.is_playoff(data.today, data.playoffs):
            Seriesticker(data, matrix, sleepEvent).render()
        '''    
    
    # Since 2024, the playoff features are removed as we have not colected the new API endpoint for them. 
    def stanley_cup_champions(self, data, matrix, sleepEvent):
        debug.info("stanley_cup_champions is disabled. This feature is not available right now")
        pass
        #StanleyCupChampions(data, matrix, sleepEvent).render()

    def standings(self, data, matrix, sleepEvent):
        #Try making standings a thread
        Standings(data, matrix, sleepEvent).render()

    def team_summary(self, data, matrix, sleepEvent):
        TeamSummary(data, matrix, sleepEvent).render()

    def clock(self, data, matrix, sleepEvent):
        Clock(data, matrix, sleepEvent)

    def pbdisplay(self, data, matrix, sleepEvent):
        pbDisplay(data, matrix, sleepEvent)

    def weather(self, data, matrix, sleepEvent):
        wxWeather(data, matrix, sleepEvent)

    def wxalert(self, data, matrix, sleepEvent):
        wxAlert(data, matrix, sleepEvent)

    def wxforecast(self, data, matrix, sleepEvent):
        wxForecast(data, matrix, sleepEvent)

    def screensaver(self, data, matrix, sleepEvent):
        screenSaver(data, matrix, sleepEvent)

    def bday0115(self, data, matrix, sleepEvent):
        Bday0115(data, matrix, sleepEvent).draw()

    def bday0201(self, data, matrix, sleepEvent):
        Bday0201(data, matrix, sleepEvent).draw()

    def bday0306(self, data, matrix, sleepEvent):
        Bday0306(data, matrix, sleepEvent).draw()

    def bday0330(self, data, matrix, sleepEvent):
        Bday0330(data, matrix, sleepEvent).draw()

    def bday0403(self, data, matrix, sleepEvent):
        Bday0403(data, matrix, sleepEvent).draw()

    def bday0503(self, data, matrix, sleepEvent):
        Bday0503(data, matrix, sleepEvent).draw()

    def bday0727(self, data, matrix, sleepEvent):
        Bday0727(data, matrix, sleepEvent).draw()

    def bday0803(self, data, matrix, sleepEvent):
        Bday0803(data, matrix, sleepEvent).draw()

    def bday1001(self, data, matrix, sleepEvent):
        Bday1001(data, matrix, sleepEvent).draw()

    def bday1112(self, data, matrix, sleepEvent):
        Bday1112(data, matrix, sleepEvent).draw()

    def ovigoals(self, data, matrix, sleepEvent):
        OviGoals(data, matrix, sleepEvent).draw()

    def streamlabs(self, data, matrix, sleepEvent):
        StreamLabs(data, matrix, sleepEvent).draw()

    def freedom(self, data, matrix, sleepEvent):
        Freedom(data, matrix, sleepEvent).draw()

    def easter(self, data, matrix, sleepEvent):
        Easter(data, matrix, sleepEvent).draw()

    def christmas(self, data, matrix, sleepEvent):
        Christmas(data, matrix, sleepEvent).draw()

    def seasoncountdown(self, data, matrix, sleepEvent):
        SeasonCountdown(data, matrix, sleepEvent).draw()
