import urllib2

from django.conf import settings

def check_url(url):
    """
    Code pulled from the Django code to test whether a URL
    is valid or not.
    """
    try:
        headers = {
            "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
            "Accept-Language" : "en-us,en;q=0.5",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
            "Connection" : "close",
            "User-Agent": settings.URL_VALIDATOR_USER_AGENT
            }
        req = urllib2.Request(url,None, headers)
        u = urllib2.urlopen(req)
    except ValueError:
        return False
    except urllib2.HTTPError, e:
        # 401s are valid; they just mean authorization is required.
        # 301 and 302 are redirects; they just mean look somewhere else.
        if str(e.code) not in ('401','301','302'):
            return False
    except: # urllib2.URLError, httplib.InvalidURL, etc.
        return False
    return True