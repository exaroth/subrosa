# -*- coding: utf-8 -*-

import urllib.request
from main import app
import json, base64



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


	def add_authorization_header(self, request):

		return request.add_header('Authorization', 'Client-ID ' + self.client_id)

	def build_request(self, data):

		url = self.API_URL

		req = urlib.request.Request(url)

		if data is not None:
			req.add_data(urllib.parse.urlencode(data).encode('utf-8'))
		return req

	def build_send_request(self, params = dict()):
		b64 = base64.b64encode(config['image'])

		data = dict(
			image = b64,
			type = 'base64',
			name = config['name'],
			description = config['description']
			)

		data.update(params)

		return self.build_request(data)

	def send_image(self):


