# -*- coding: utf-8 -*-
"""

    subrosa.imgur
    ============


    Implements class that allows
    integration with imgur API

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.

"""

import base64
import json
from six.moves import urllib



class ImgurHandler(object):

    """
    Basic class for handling Imgur image upload,
    Accepts header containing user_id variable
    and dictionary containing request configuration
    """

    API_URL = "https://api.imgur.com/3/image"

    def __init__(self, client_id , config = dict()):

        self.client_id = client_id
        self.config = config
        if 'api' in self.config:
            self.API_URL = self.config['api']


    def get_api(self):
        return self.API_URL


    def add_authorization_header(self, additional = dict()):

        """
        Builds authorization headers for anonymous users
        """

        headers = dict(
            Authorization = "Client-ID " + self.client_id
        )
        headers.update(additional)
        return headers


    def build_send_request(self, params = dict()):

        """
        Build request for sending an image
        """

        img = self.config.get("image", None)
        if not img:
            raise Exception("Missing image file")

        b64 = base64.b64encode(img.read())

        data = dict(
                image = b64,
                type = 'base64',
                name = self.config.get("name", None),
                description = self.config.get("description", None)
                )

        data.update(params)
        return urllib.parse.urlencode(data).encode("utf-8")


    def send_image(self, params = dict(), additional = dict()):
        req = urllib.request.Request(url = self.get_api(),
                              data = self.build_send_request(params),
                              headers = self.add_authorization_header()
                             )
        data = urllib.request.urlopen(req)
        return json.loads(data.read().decode("utf-8"))

    def delete_image(self, delete_hash):
        opener = urllib.request.build_opener(urllib.request.HTTPHandler)
        req = urllib.request.Request(url = self.get_api() + "/" + delete_hash,
                              headers = self.add_authorization_header())
        req.get_method = lambda: "DELETE"
        data = urllib.request.urlopen(req)
        return json.loads(data.read())

