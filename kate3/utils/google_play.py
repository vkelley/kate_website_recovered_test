import urllib
from decimal import Decimal

from BeautifulSoup import BeautifulSoup

class GetAppInfo(object):
    base_url = 'https://play.google.com'
    search_url = '%s/store/search' % base_url
    raw = None

    results = {}

    def __init__(self, name=None):
        self.name = name

        self._fetch_url()
        self._get_info()

    def _fetch_url(self):
        query = {'q': self.name}
        self.url = '%s?%s' % (self.search_url, urllib.urlencode(query))
        self.raw = urllib.urlopen(self.url).read()

    def _get_info(self):
        if not self.raw:
            self._fetch_url()

        soup = BeautifulSoup(self.raw)
        result = soup('div', {'class': 'snippet snippet-tall'})[0]

        raw_name = result('a', {'class': 'title goog-inline-block'})[0].contents[0]
        raw_url = result('a', {'class': 'thumbnail'})[0]['href']
        raw_cost = result('span', {'class': 'buy-button-price'})[0].contents[0]

        self.results['name'] = raw_name
        self.results['url'] = self._convert_url(raw_url)
        self.results['cost'] = self._convert_cost(raw_cost)

    def _convert_url(self, url):
        return "%s%s" % (self.base_url, url)

    def _convert_cost(self, cost):
        if cost == 'Install':
            return Decimal('0.00')
        c = cost.split(' ')[0]
        if c.startswith('$'):
            return Decimal(str(c[1:]))
        return Decimal(str(c))

    def get_info(self):
        return self.results


