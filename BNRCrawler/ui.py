from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from BNRCrawler.db import DB
import datetime

class TableView(qtw.QTableView):
	def __init__(self, *args, **kwargs):
		super().__init__()

		self.db = DB()

		if not self.db.conn:
			qtw.QMessageBox.critical(
				None,
				"Database Error!",
				"Database Error: %s" % con.lastError().databaseText(),
			)
			return False


		self.data = self.db.select_all_data()
		self.column_names = self.db.get_column_names()

		model = self.setup_model()

		self.filter_proxy_model = qtc.QSortFilterProxyModel()
		self.filter_proxy_model.setSourceModel(model)
		self.filter_proxy_model.setFilterCaseSensitivity(qtc.Qt.CaseInsensitive)
		self.filter_proxy_model.setFilterKeyColumn(1)

		self.setModel(self.filter_proxy_model)

		self.setup_gui()

	def setup_gui(self):
		### set table dimensions:
		# get rows and columns count from model:
		rows_count = self.model().rowCount()
		cols_count = self.model().columnCount()

		self.setMinimumWidth(cols_count*230);
		self.setMinimumHeight(rows_count*40);

		# self.resizeColumnToContents(0)
		self.resizeColumnToContents(1)
		self.setColumnWidth(3, 300)

		self.verticalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeToContents);

		# enable columns sort
		self.setSortingEnabled(True)
		self.sortByColumn(0,qtc.Qt.AscendingOrder)

	def setup_model(self):
		model = qtg.QStandardItemModel()
		model.setHorizontalHeaderLabels(self.column_names)

		for i, row in enumerate(self.data):
			# items = [qtg.QStandardItem(str(item)) for item in row]

			items = []
			for field in row:
				item = qtg.QStandardItem()
				if isinstance(field, datetime.date):
					field = field.strftime('%d.%m.%Y')
				elif isinstance(field, str) and len(field)>100:
					# set full string with UserRole for later use:
					item.setData(field, qtc.Qt.UserRole)
					# trim string for display
					field = field[0:50]+'...'

				item.setData(field, qtc.Qt.DisplayRole)
				items.append(item)

			model.insertRow(i, items)

		return model

	@qtc.pyqtSlot(int)
	def set_filter_column(self,index):
		self.filter_proxy_model.setFilterKeyColumn(index)

	def get_last_updated_date(self):
		last_updated_date=self.db.get_last_updated_date()
		return last_updated_date.strftime('%d.%m.%y, %H:%M:%S')

class TableViewWidget(qtw.QWidget):
	def __init__(self, parent, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.parent = parent

		self.setup_gui()

	def setup_gui(self):
		# table view:
		self.tableView = TableView()
		tableViewWidth = self.tableView.frameGeometry().width()
		tableViewHeight = self.tableView.frameGeometry().height()
		# print(tableViewWidth, tableViewHeight)

		# label
		lblTitle = qtw.QLabel()
		label_msg = f'Radiotheaters publications as crawlled on {self.tableView.get_last_updated_date()}'
		lblTitle.setText(label_msg)
		lblTitle.setStyleSheet('''
			font-size: 30px;
			margin:20px auto;
			color: purple;

		''')
		lblTitle.setAlignment(qtc.Qt.AlignCenter)

		# filter box layout:
		filterLabel = qtw.QLabel('Filter by column: ')

		filterLineEdit = qtw.QLineEdit()
		filterLineEdit.textChanged.connect(self.tableView.filter_proxy_model.setFilterRegExp)

		comboBox = qtw.QComboBox()
		comboBox.addItems(["{0}".format(col) for col in self.tableView.column_names])
		comboBox.setCurrentText('title')
		comboBox.currentIndexChanged.connect(lambda idx:self.tableView.set_filter_column(idx))

		filterBoxLayout = qtw.QHBoxLayout()
		filterBoxLayout.addWidget(filterLabel)
		filterBoxLayout.addWidget(comboBox)
		filterBoxLayout.addWidget(filterLineEdit)

		# close button
		btnClose = qtw.QPushButton('Close')
		# btnClose.clicked.connect(self.close_all)
		# or with lambda syntax
		btnClose.clicked.connect( lambda _:self.close() and self.parent.close() )

		# main layout
		layout = qtw.QVBoxLayout()
		layout.addWidget(lblTitle)
		layout.addLayout(filterBoxLayout)
		layout.addWidget(self.tableView)
		layout.addWidget(btnClose)

		self.setLayout(layout)

		self.setFixedWidth(tableViewWidth)
		# self.setFixedHeight(tableViewHeight)

	def close_all(self):
		self.parent.close()
		self.close()

	@qtc.pyqtSlot(int)
	def on_comboBox_currentIndexChanged(self,index):
		self.tableView.filter_proxy_model.setFilterKeyColumn(index)


	def get_current_datetime(self):
		return datetime.datetime.now().strftime('%d.%m.%y, %H:%M:%S')

