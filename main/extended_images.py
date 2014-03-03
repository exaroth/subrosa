"""

Replace <img src='..'> tags with <img src='new' data-src='..'> 
Used for preloading images in article view

Accepts new path to src attribute in config

	:author Konrad Wasowicz <exaroth@gmail.com>

"""



import markdown
from markdown.inlinepatterns import IMAGE_LINK_RE, IMAGE_REFERENCE_RE
from markdown.treeprocessors import Treeprocessor
import logging

logger = logging.getLogger("MARKDOWN")

class ExtendedImagesExtension(markdown.Extension):

	def __init__(self, config):
		self.config = {
			# set default path
			'replacement': [ '#', 'Replacement for src tag' ]
		}

		for k, v in config:
			self.setConfig(k, v)

	def extendMarkdown(self, md, md_globals):
		md.registerExtension(self)
		self.processor = ExtendedImagesTreeprocessor()
		self.processor.md = md
		self.processor.config = self.getConfigs()
		if 'att_list' in md.treeprocessors.keys():
			md.treeprocessores.add('extended_img', self.processor, '>attr_list')
		else:
			md.treeprocessors.add('extended_img', self.processor, '>prettify')




class ExtendedImagesTreeprocessor(Treeprocessor):

	
	"""
	Replace <img src='...'> tags
	with <img data-src='...'>
	"""


	def run(self, text):

		replacement = self.config['replacement']

		for elem in text.getiterator():
			if elem.tag == 'img':
				# if 'title' in elem.attrib:
				# 	title = elem.get('title')
				# if 'alt' in elem.attrib:
				# 	alt = elem.get('alt')

				base_src = elem.get('src')

				elem.set('src', replacement)
				elem.set('data-src', base_src)

def makeExtension(config = None):
	return ExtendedImagesExtension(config = config)


