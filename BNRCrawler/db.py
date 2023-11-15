try:
	from BNRCrawler.config.read_config import read_db_config
except:
	from config.read_config import read_db_config


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

	def insert_rows(self, rows_data):
		sql = """
			INSERT IGNORE INTO radiotheaters
			(title, pub_date, content)
			VALUES ( %s, %s, %s)
		"""

		with self.conn.cursor() as cursor:
			cursor.executemany(sql, rows_data)
			self.conn.commit()

	def insert_row(self, row_data):
		sql = """
			INSERT IGNORE INTO radiotheaters
				(title, pub_date, content)
				VALUES ( %s, %s, %s)
		"""

		with self.conn.cursor(prepared=True) as cursor:
			cursor.execute(sql, tuple(row_data.values()))
			self.conn.commit()

	def select_all_data(self):
		sql = "SELECT id, title, pub_date, content FROM  radiotheaters"

		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			result = cursor.fetchall()

		return result

	def get_last_updated_date(self):
		sql = 'SELECT MAX(updated_at) AS "Max Date" FROM radiotheaters;'
		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			result = cursor.fetchone()

		if result:
			return result[0]
		else:
			raise ValueError('No data in table')

	def get_column_names(self):
		sql = "SELECT id, title, pub_date, content FROM  radiotheaters LIMIT 1;"

		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			result = cursor.fetchone()

		return cursor.column_names

	def truncate_table(self):
		pass

	def close_connection(self):
		self.conn.close()
