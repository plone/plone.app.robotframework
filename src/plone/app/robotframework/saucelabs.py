# -*- coding: utf-8 -*-
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


class SauceLabsLibrary:

    def report_sauce_status(self, job_id, test_status, test_tags=[]):
        """Report test status and tags to SauceLabs
        """
        username = os.environ.get('SAUCE_USERNAME')
        access_key = os.environ.get('SAUCE_ACCESS_KEY')

        if not job_id:
            return u"No Sauce job id found. Skipping..."
        elif not username or not access_key:
            return u"No Sauce environment variables found. Skipping..."

        token = base64.encodestring('%s:%s' % (username, access_key))[:-1]
        body = json.dumps({'passed': test_status == 'PASS',
                           'tags': test_tags})

        connection = httplib.HTTPConnection('saucelabs.com')
        connection.request('PUT', '/rest/v1/%s/jobs/%s' % (
            username, job_id), body,
            headers={'Authorization': 'Basic %s' % token}
        )
        return connection.getresponse().status
