import requests

class Crawler:
	def __init__(self, url) -> None:
		self.url = url

	def save_html(self):
		filename = './data/result.html'
		with open(filename, 'w') as f:
			f.write(self.html)

	def get_html(self)-> str:
		r = requests.get(self.url)

		if r.ok:
			self.html = r.text
			return self.html



