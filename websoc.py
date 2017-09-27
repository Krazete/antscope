from google.appengine.api import urlfetch
from datetime import datetime
from bs4 import BeautifulSoup

URL = 'https://www.reg.uci.edu/perl/WebSoc'

def get():
    'Returns content from WebSoc.'
    return urlfetch.fetch(URL).content

def post(yearterm, coursecodes=None):
    'Posts a request to WebSoc and returns the response content.'
    params = '?YearTerm=' + yearterm
    if coursecodes:
        params += '&Submit=TextResults&CourseCodes=' + coursecodes
    return urlfetch.fetch(URL + params).content

def detect_yearterms(year=None):
    'Detects current yearterms or gets yearterms specified by year.'
    if not year:
        year = datetime.now().year
    content = get()
    html = BeautifulSoup(content, 'html.parser')
    yearterms_html = html.find('select').find_all('option')
    yearterms = map(lambda e: e['value'], yearterms_html)
    return filter(lambda e: int(e.split('-')[0]) == year, yearterms)

def generate_yearterms(year=None):
    'Generates current yearterms or yearterms specified by year.'
    yearterms = detect_yearterms(year)
    for yearterm in yearterms:
        if year:
            yield yearterm
        else:
            content = post(yearterm)
            if 'Currently in week' in content:
                yield yearterm

def generate_coursecodes(n):
    'Generates coursecodes from 0 to 99999 in blocks of size n.'
    blocks = 100000 / n
    remainder = 100000 % n
    for i in range(blocks):
        a = i * n
        b = a + n - 1
        yield str(a) + '-' + str(b)
    if remainder:
        a = b + 1
        b = a + remainder - 1
        yield str(a) + '-' + str(b)

def get_data(year=None):
    'Returns raw data of course schedules from WebSoc.'
    data = []
    yearterms = generate_yearterms(year)
    for yearterm in yearterms:
        coursecodes = generate_coursecodes(800)
        for coursecode in coursecodes:
            content = post(yearterm, coursecode)
            if 'No courses matched' not in content:
                data.append(content)
    return data
