from http.client import HTTPConnection
from robot.libraries.BuiltIn import BuiltIn

import base64
import json
import os
import re


USERNAME_ACCESS_KEY = re.compile(r"^(http|https)://([^:]+):([^@]+)@")


class SauceLabs:
    def report_sauce_status(self, name, status, tags=[], remote_url=""):
        """Report test status and tags to SauceLabs"""
        job_id = (
            BuiltIn()
            .get_library_instance("Selenium2Library")
            .driver
            .session_id
        )

        if USERNAME_ACCESS_KEY.match(remote_url):
            username, access_key = USERNAME_ACCESS_KEY.findall(remote_url)[0][1:]
        else:
            username = os.environ.get("SAUCE_USERNAME")
            access_key = os.environ.get("SAUCE_ACCESS_KEY")

        if not job_id:
            return "No Sauce job id found. Skipping..."
        elif not username or not access_key:
            return "No Sauce environment variables found. Skipping..."

        token = base64.encodestring(f"{username}:{access_key}")[:-1]
        body = json.dumps({"name": name, "passed": status == "PASS", "tags": tags})

        connection = HTTPConnection("saucelabs.com")
        connection.request(
            "PUT",
            f"/rest/v1/{username}/jobs/{job_id}",
            body,
            headers={"Authorization": "Basic %s" % token},
        )
        return connection.getresponse().status
