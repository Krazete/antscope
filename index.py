import webapp2
import json
import urllib
import traceback
import antndb
from scrape import scrape

MAPURL = 'https://www.myatlascms.com/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5'
# https://map.uci.edu/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5
# https://www.myatlascms.com/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5
# http://map.concept3d.com/?id=463
# https://www.reg.uci.edu/perl/WebSoc?YearTerm=1990-03&CourseCodes=0-99999&Submit=Text

class Index(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        database = {}
        for schedule in antndb.Schedule.query().fetch():
            building = schedule.building
            room = schedule.room
            database.setdefault(building, {})
            database[building].setdefault(room, {
                'schedule': schedule.schedule,
                'datestamp': schedule.datestamp.isoformat()
            })
        template = open('index.html').read()
        datajson = json.dumps(database)
        mapjson = urllib.urlopen(MAPURL).read()
        content = template.replace('{WEBSOC_DATA}', datajson).replace('{MAP_DATA}', mapjson)
        self.response.write(content)

class Scrape_YearTerm(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = open('scrape_yearterm.html').read()
        content = template.replace('{YEAR_VALUE}', '1990').replace('{INPUT_INDEX}', '1')
        self.response.write(content)
    def post(self):
        year = int(self.request.get('year', 1990))
        term = int(self.request.get('term', 92))
        template = open('scrape_yearterm.html').read()
        try:
            scrape([year], [term])
            self.response.write('YearTerm {:04d}-{:02d} has successfully been added to the database.<br><br>'.format(year, term))
            year_value = str(year + 1 if term == 92 else year) # iterate year
            input_index = str([0, 92, 03, 14, 25, 39, 76].index(term)) # iterate term
        except Exception as e:
            traceback.print_exc() # only visible in terminal
            self.response.write('ERROR: {}<br><br>'.format(e))
            year_value = str(year) # preserve year
            input_index = str([0, 03, 14, 25, 39, 76, 92].index(term)) # preserve term
        content = template.replace('{YEAR_VALUE}', year_value).replace('{INPUT_INDEX}', input_index)
        self.response.write(content)

sitemap = [
    ('/', Index),
    ('/scrape_yearterm', Scrape_YearTerm)
]

app = webapp2.WSGIApplication(sitemap, debug=True)
