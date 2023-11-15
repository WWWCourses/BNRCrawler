import sys

from BNRCrawler.crawler import Crawler
from BNRCrawler.ui import TableView, TableViewWidget

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel



import datetime

BASE_URL = 'https://bnr.bg/hristobotev/radioteatre/list'

class MainWindow(qtw.QMainWindow):
	def __init__(self , *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.crawler = Crawler(BASE_URL)

		self.setWindowTitle('BNR Crawler')

		layout = qtw.QVBoxLayout()
		lblTableCaption = qtw.QLabel('Radiotheaters Data')
		lblTableCaption.setObjectName('lblTableCaption')
		lblTableCaption.setAlignment(qtc.Qt.AlignCenter)
		layout.addWidget(lblTableCaption)

		btnsLayout = qtw.QHBoxLayout()
		btnCrawlerRun = qtw.QPushButton('Run Crawler')
		self.btnShowData = qtw.QPushButton('Show Data')
		# self.btnShowData.setEnabled(False)

		btnsLayout.addWidget(btnCrawlerRun)
		btnsLayout.addWidget(self.btnShowData)
		layout.addLayout(btnsLayout)

		# actions on buttons click:
		self.btnShowData.clicked.connect(self.show_data)
		# btnCrawlerRun.clicked.connect(self.run_crawler)
		btnCrawlerRun.clicked.connect( self.crawler.run )

		# add spacer or just fixed spacing
		layout.addSpacing(10)
		# layout.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding))

		mainWidget = qtw.QWidget()
		mainWidget.setLayout(layout)

		self.setCentralWidget(mainWidget)

		self.show();

	def show_data(self):
		self.tableViewWidget = TableViewWidget(parent=self)

		self.tableViewWidget.show()

	def run_crawler(self):
		self.setCursor(qtc.Qt.WaitCursor)

		self.crawler.run()

		self.setCursor(qtc.Qt.ArrowCursor)


if __name__ == '__main__':
	app = qtw.QApplication(sys.argv);

	window = MainWindow()

	sys.exit(app.exec_())
