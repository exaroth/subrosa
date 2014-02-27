# -*- coding: utf-8 -*-

import json, base64
import requests



class ImgurHandler(object):

	"""
	Basic class for handling imgur image upload
	accepts header containing user_id variable
	and dictionary containing connection data
	"""

	API_URL = "https://api.imgur.com/3/image.json"

	def __init__(self, client_id , config):
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

            img = config.get("image", None)
            if not img:
                raise Exception("Missing image file")

            b64 = base64.b64encode(img)

            data = dict(
                    image = b64,
                    type = 'base64',
                    name = config['name'],
                    description = config.get("description", None)
                    )

            data.update(params)

            return json.dumps(data)


	def send_image(self, params = dict(), additional = dict()):
            req = requests.post(self.get_api(),\
                                data = self.build_send_request(params),\
                                headers = add_authorization_header(additional))

            return req.json()

