from BNRCrawler.db import DB
from datetime import datetime

if __name__ == "__main__":
  db = DB()
#   db.drop_radiotheaters_table()
#   db.create_radiotheaters_table()
  db.insert_row( ('PubTitle3', datetime.now() , 'contnet') )