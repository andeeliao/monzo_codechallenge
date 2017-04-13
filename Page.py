class Page():
	def __init__(self, url):
		self.url = url
		self.static_assets = []
		self.links_to = []

	def set_static_assets(self, assets):
		self.static_assets = assets

	def add_static_asset(self, asset):
		self.static_assets.append(asset)

	def add_links_to(self, url):
		self.links_to.append(url)

	def set_links_to(self, urls):
		self.links_to = urls

		