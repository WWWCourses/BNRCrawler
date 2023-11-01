from BNRCrawler.config.read_config import read_db_config

import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

class DB:
	def __init__(self):
		try:
			db_config = read_db_config('config.ini', 'mysql')
			# print(db_config)
			self.conn = mysql.connector.connect(**db_config)
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)

	def create_radiotheaters_table(self):
		sql = """
			CREATE TABLE IF NOT EXISTS radiotheaters(
				id INT AUTO_INCREMENT PRIMARY KEY,
				title VARCHAR(100) NOT NULL,
				pub_date DATE NOT NULL,
				content TEXT,
				created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
				updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

				CONSTRAINT title_date UNIQUE (title, pub_date)
			);
		"""
		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			self.conn.commit()

	def drop_radiotheaters_table(self):
		sql = "DROP TABLE IF EXISTS radiotheaters";

		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			self.conn.commit()

	def insert_row(self, data):
		print(data)
		q = """
			INSERT INTO radiotheaters
				(title, pub_date, content)
				VALUES ( %s, %s, %s)
		"""

		with self.conn.cursor(prepared=True) as cursor:
			cursor.execute(q, data)
			self.conn.commit()

	def truncate_table(self):
				pass


	def close_connection(self):
		self.conn.close()
