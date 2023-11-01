from BNRCrawler.db import DB
from BNRCrawler.crawler import Crawler
from datetime import datetime


BASE_URL = 'https://bnr.bg/hristobotev/radioteatre/list'

if __name__ == "__main__":

	crawler = Crawler(BASE_URL)
	html = crawler.get_html()
	crawler.save_html()


