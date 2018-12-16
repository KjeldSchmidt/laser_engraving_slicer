from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

from SlicerSettingsWindow import SlicerSettingsWindow


class MainWindow( QMainWindow ):
	def __init__( self ):
		super().__init__()
		self.init_ui()
		self.slicer_settings = SlicerSettingsWindow( self )

	def init_ui( self ):
		self.setGeometry( 200, 200, 400, 600 )
		self.setWindowTitle( 'Laser Engraving Slicer' )

		self.central_widget = QWidget()
		self.setCentralWidget( self.central_widget )

		self.source_image_file_name = None
		self.source_image_label = QLabel()

		sidebar = self.make_sidebar()

		main_layout = QHBoxLayout( self.central_widget )
		main_layout.addWidget( sidebar )
		main_layout.addWidget( self.source_image_label )

		self.setLayout( main_layout )

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

	def make_sidebar( self ):
		sidebar_widget = QWidget()
		sidebar_layout = QVBoxLayout( sidebar_widget )
		sidebar_layout.setAlignment( Qt.AlignTop )

		open_source_image_button = QPushButton( 'Open Image', sidebar_widget )
		settings_button = QPushButton( 'Process Settings', sidebar_widget )
		slice_button = QPushButton( 'Save GCode', sidebar_widget )

		open_source_image_button.setToolTip( 'Open an image file for slicing' )
		settings_button.setToolTip( 'Change printer settings to ensure a quality result' )
		slice_button.setToolTip( 'Save GCode to control your engraver' )

		open_source_image_button.clicked.connect( self.open_source_file )
		settings_button.clicked.connect( self.open_slicer_settings )
		slice_button.clicked.connect( self.save_gcode )

		sidebar_layout.addWidget( open_source_image_button )
		sidebar_layout.addWidget( settings_button )
		sidebar_layout.addWidget( slice_button )

		return sidebar_widget

	@pyqtSlot()
	def open_source_file( self ):
		picked_file_name = QFileDialog.getOpenFileName( self, 'Open file',
			filter="All Graphics (*.png *.bmp *.jpeg *.jpg *.svg);;Pixel Graphics (*.png *.bmp *.jpeg *.jpg);;Vector Graphics (*.svg)" )

		if picked_file_name[ 0 ]:
			self.source_image_file_name = picked_file_name[ 0 ]
			self.show_source_image()

	@pyqtSlot()
	def open_slicer_settings( self ):
		self.slicer_settings.show()

	@pyqtSlot()
	def save_gcode( self ):
		file_name, file_type = QFileDialog.getSaveFileName( self, 'Save GCode', filter="GCode (*.gcode)" )
		if file_name:
			print( file_name )
			gcode = GCodeGenerator.make_gcode( self.slicer_settings.get_all_attributes() )
			print( gcode )

	def show_source_image( self ):
		print( 'setting image' )
		pixmap = QPixmap( self.source_image_file_name )
		self.source_image_label.setPixmap( pixmap )
