from PyQt5.QtWidgets import QMainWindow, QAction


class MainWindow( QMainWindow ):
	def __init__( self ):
		super().__init__()
		self.init_ui()

	def init_ui( self ):
		self.setGeometry( 200, 200, 400, 600 )
		self.setWindowTitle( 'Laser Engraving Slicer' )

		main_menu = self.menuBar()
		self.make_file_menu()

		self.show()

	def make_file_menu( self ):
		main_menu = self.menuBar()
		file_menu = main_menu.addMenu('File')

		close_app = QAction('Exit', self)
		close_app.setShortcut('Ctrl+Q')
		close_app.setStatusTip('Exit this program')
		close_app.triggered.connect(self.close)
		file_menu.addAction(close_app)

