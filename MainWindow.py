from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog


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
		file_menu = main_menu.addMenu( 'File' )

		close_app = QAction( 'Exit', self )
		close_app.setShortcut( 'Ctrl+Q' )
		close_app.setStatusTip( 'Exit this program' )
		close_app.triggered.connect( self.close )

		open_file = QAction( 'Open File', self )
		open_file.setStatusTip( 'Open a source file for slicing' )
		open_file.triggered.connect( self.open_source_file )

		file_menu.addAction( open_file )
		file_menu.addAction( close_app )

	def open_source_file( self ):
		picked_file_name = QFileDialog.getOpenFileName( self, 'Open file',
			filter="All Graphics (*.png *.bmp *.jpeg *.jpg *.svg);;Pixel Graphics (*.png *.bmp *.jpeg *.jpg);;Vector Graphics (*.svg)" )

		if picked_file_name[ 0 ]:
			with open( picked_file_name[ 0 ], 'rb' ) as source_file:
				data = source_file.read()
				print( data )
