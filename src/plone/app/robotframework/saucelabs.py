# -*- coding: utf-8 -*-
import re
import os
import httplib
import base64
try:
    import json
    json  # pyflakes
except ImportError:
    import simplejson as json


# Inject keyword for getting the selenium session id
import Selenium2Library
Selenium2Library.keywords._browsermanagement.\
    _BrowserManagementKeywords.get_session_id = lambda self:\
    self._cache.current.session_id

USERNAME_ACCESS_KEY = re.compile('^(http|https):\/\/([^:]+):([^@]+)@')


class SauceLabs:

    def report_sauce_status(self, job_id, name, status, tags=[], url=''):
        """Report test status and tags to SauceLabs
        """
        if USERNAME_ACCESS_KEY.match(url):
            username, access_key = USERNAME_ACCESS_KEY.findall(url)[0][1:]
        else:
            username = os.environ.get('SAUCE_USERNAME')
            access_key = os.environ.get('SAUCE_ACCESS_KEY')

        if not job_id:
            return u"No Sauce job id found. Skipping..."
        elif not username or not access_key:
            return u"No Sauce environment variables found. Skipping..."

        token = base64.encodestring('%s:%s' % (username, access_key))[:-1]
        body = json.dumps({'name': name,
                           'passed': status == 'PASS',
                           'tags': tags})

        connection = httplib.HTTPConnection('saucelabs.com')
        connection.request('PUT', '/rest/v1/%s/jobs/%s' % (
            username, job_id), body,
            headers={'Authorization': 'Basic %s' % token}
        )
        return connection.getresponse().status
