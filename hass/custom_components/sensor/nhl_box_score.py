import voluptuous as vol
import datetime
import logging
import json

from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor.rest import RestData
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.util.dt as hassdt
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_TEAM = "team"
CONF_CALENDAR = "calendar"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_TEAM): cv.string,
    vol.Required(CONF_CALENDAR): cv.string
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    add_devices([NHLBoxScoreSensor(hass, config.get(CONF_TEAM), config.get(CONF_CALENDAR))])

class NHLBoxScoreSensor(Entity):

    SCHEDULE_ENDPOINT = 'http://statsapi.web.nhl.com/api/v1/schedule/?date={}'
    FEED_ENDPOINT = 'http://statsapi.web.nhl.com/api/v1/game/{}/feed/live'

    def __init__(self, hass, team, calendar):
        self.hass = hass
        self.game_id = None
        self.is_gameday = False
        self.last_checked = datetime.datetime.fromtimestamp(0)
        self.schedule_rest = None
        self.feed_rest = None
        self.scoring_plays = []
        self.penalties = []
        self.players = {}
        self.period = 1
        self.is_intermission = False
        self.team = team
        self.calendar = calendar
        self.schedule_query = NHLBoxScoreSensor.SCHEDULE_ENDPOINT.format(hassdt.now().strftime("%Y-%m-%d"))

    @property
    def state_attributes(self):
        """Return the state attributes."""
        return {
            "gameday": self.is_gameday,
            "last_checked": self.last_checked,
            "period": self.period,
            "intermission": self.is_intermission,
            "query": self.schedule_query
        }

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'NHL Box Score Sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return "Game ID: {}".format(self.game_id) if self.game_id is not None else "No Game"

    def init_game_data(self):
        self.period = 1
        del self.scoring_plays[:]
        del self.penalties[:]
        self.players.clear()
        self.is_intermission = True

    def setup_rest(self, endpoint, variables=None):
        payload = auth = headers = None
        verify_ssl = False
        method = 'GET'

        return RestData(method, endpoint.format(variables), auth, headers, payload, verify_ssl)

    def fetch_game_id(self):
        if self.is_gameday:
            self.schedule_query = NHLBoxScoreSensor.SCHEDULE_ENDPOINT.format(hassdt.now().strftime("%Y-%m-%d"))
            self.schedule_rest = self.setup_rest(self.schedule_query)
            self.schedule_rest.update()
            json_data = None
            try:
                json_data = json.loads(self.schedule_rest.data)
            except ValueError as e:
                _LOGGER.error("Schedule data could not be parsed as JSON")

            if json_data is not None:
                games = json_data['dates'][0]['games']
                my_game = [game['gamePk'] for game in games if game['teams']['away']['team']['name'] == self.team or
                                                               game['teams']['home']['team']['name'] == self.team]
                if len(my_game) == 1:
                    self.game_id = my_game[0]
                    self.init_game_data()
                    self.feed_rest = self.setup_rest(NHLBoxScoreSensor.FEED_ENDPOINT, self.game_id)
            else:
                _LOGGER.error("Unable to fetch today's schedule from API")
        else:
            self.game_id = None

    def get_player_info(self, playerId):
        player_detail = self.players.get(playerId)
        if player_detail:
            return (player_detail['fullName'], player_detail['primaryNumber'])
        else:
            return None

    def get_scoring_info(self, event):
        scoring_info = {}
        scoring_info['team'] = event['team']['name']
        scoring_info['assists'] = []
        players = event['players']
        for player in players:
            player_details = self.get_player_info('ID{}'.format(player['player']['id']))
            if player_details is not None:
                if player['playerType'] == 'Scorer':
                    scoring_info['scorer'] = {'name': player_details[0], 'number': player_details[1]}
                if player['playerType'] == 'Assist':
                    scoring_info['assists'].append({'name': player_details[0], 'number': player_details[1]})
        return scoring_info

    def get_penalty_info(self, event):
        penalty_info = {}
        penalty_info['team'] = event['team']['name']
        penalty_info['description'] = "{} minute {} for {}".format(event['result']['penaltyMinutes'], event['result']['penaltySeverity'], event['result']['secondaryType'])
        players = event['players']
        for player in players:
            player_details = self.get_player_info('ID{}'.format(player['player']['id']))
            if player_details is not None:
                if player['playerType'] == 'PenaltyOn':
                    penalty_info['player'] = {'name': player_details[0], 'number': player_details[1]}
        return penalty_info

    def poll_game_feed(self, team_calendar):
        game_active = (team_calendar.state == "on") or self.period > 1

        if self.is_gameday and game_active and self.game_id is not None:
            self.feed_rest.update()
            json_data = None
            try:
                json_data = json.loads(self.feed_rest.data)
            except ValueError as e:
                _LOGGER.error("Feed data could not be parsed as JSON")

            if json_data is not None:
                plays = json_data['liveData']['plays']['allPlays']

                # Store the lineups
                if not self.players:
                    self.players = json_data['gameData']['players'].copy()

                # Look for period events
                for event in plays:
                    eventId = event['about']['eventId']

                    if event['result']['event'] == "Goal" and eventId not in self.scoring_plays:
                        self.hass.bus.fire('nhl_scoring', self.get_scoring_info(event))
                        self.scoring_plays.append(eventId)
                    elif event['result']['event'] == "Penalty" and eventId not in self.penalties:
                        self.hass.bus.fire('nhl_penalty', self.get_penalty_info(event))
                        self.penalties.append(eventId)
                    elif self.is_intermission and event['result']['event'] == "Period Start" and event['about']['period'] == self.period:
                        self.hass.bus.fire('nhl_period_start', {"period": self.period})
                        self.is_intermission = False
                    elif event['result']['event'] == "Period End" and event['about']['period'] == self.period:
                        self.hass.bus.fire('nhl_period_end', {"period": self.period})
                        self.is_intermission = True
                        self.period += 1
                    elif event['result']['event'] == "Game End":
                        self.hass.bus.fire('nhl_game_end', {})
                        self.init_game_data()
                        self.game_id = None
            else:
                _LOGGER.error("Unable to fetch live feed data from game")

    def update(self):
        today_date = hassdt.now()
        team_calendar = self.hass.states.get(self.calendar)

        # Check once a day to see if there's a game today
        if self.last_checked.date() < today_date.date() and today_date.hour > 8:
            self.last_checked = today_date
            next_scheduled_game = team_calendar.attributes.get('start_time')
            next_scheduled_game = datetime.datetime.strptime(next_scheduled_game, '%Y-%m-%d %H:%M:%S')
            self.is_gameday = (next_scheduled_game.date() == today_date.date())
            self.fetch_game_id()

        self.poll_game_feed(team_calendar)

