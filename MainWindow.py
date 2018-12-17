import json
from json import JSONDecodeError

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, \
	QMessageBox, QSizePolicy

import GCodeGenerator
import SlicerStyles
from ErrorPopup import error_popup
from ImageLabel import ImageLabel
from SlicerSettingsWindow import SlicerSettingsWindow


class MainWindow( QMainWindow ):
	def __init__( self ):
		super().__init__()

		self.slicer_settings = SlicerSettingsWindow( self, self.show_source_image )
		self.source_image_label = ImageLabel()
		self.result_image_label = ImageLabel()
		self.source_image_file_name = None
		self.central_widget = QWidget()

		self.init_ui()

	def init_ui( self ):
		self.setGeometry( 200, 200, 400, 600 )
		self.setWindowTitle( 'Laser Engraving Slicer' )

		self.setCentralWidget( self.central_widget )

		sidebar = self.make_sidebar()
		image_display = self.make_image_display()

		main_layout = QHBoxLayout( self.central_widget )
		main_layout.addWidget( sidebar )
		main_layout.addWidget( image_display )

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
		save_settings_button = QPushButton( 'Save Settings', sidebar_widget )
		load_settings_button = QPushButton( 'Load Settings', sidebar_widget )

		open_source_image_button.setToolTip( 'Open an image file for slicing' )
		settings_button.setToolTip( 'Change printer settings to ensure a quality result' )
		slice_button.setToolTip( 'Save GCode to control your engraver' )
		save_settings_button.setToolTip( 'Save Settings for quick and easy reuse' )
		load_settings_button.setToolTip( 'Load Settings for quick and easy reuse' )

		open_source_image_button.clicked.connect( self.open_source_file )
		settings_button.clicked.connect( self.open_slicer_settings )
		slice_button.clicked.connect( self.save_gcode )
		save_settings_button.clicked.connect( self.save_settings )
		load_settings_button.clicked.connect( self.load_settings )

		sidebar_layout.addWidget( open_source_image_button )
		sidebar_layout.addWidget( settings_button )
		sidebar_layout.addWidget( slice_button )
		sidebar_layout.addWidget( save_settings_button )
		sidebar_layout.addWidget( load_settings_button )

		return sidebar_widget

	def make_image_display( self ):
		image_display = QWidget()

		size_policy = QSizePolicy( QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding )
		size_policy.setHeightForWidth( True )

		self.source_image_label.setSizePolicy( size_policy )
		self.result_image_label.setSizePolicy( size_policy )

		image_layout = QVBoxLayout( image_display )

		image_layout.addWidget( self.source_image_label )
		image_layout.addWidget( self.result_image_label )

		return image_display

	@pyqtSlot()
	def open_source_file( self ):
		picked_file_name, file_type = QFileDialog.getOpenFileName( self, 'Open file',
			filter="All Graphics (*.png *.bmp *.jpeg *.jpg *.svg);;Pixel Graphics (*.png *.bmp *.jpeg *.jpg);;Vector Graphics (*.svg)" )

		if picked_file_name:
			self.source_image_file_name = picked_file_name
			self.show_source_image()

	@pyqtSlot()
	def open_slicer_settings( self ):
		self.slicer_settings.show()

	@pyqtSlot()
	def save_gcode( self ):
		file_name, file_type = QFileDialog.getSaveFileName( self, 'Save GCode', filter="GCode (*.gcode)" )
		if file_name:
			gcode = GCodeGenerator.make_gcode( self.slicer_settings.get_all_attributes() )
			with open( file_name, 'w' ) as gcode_outfile:
				gcode_outfile.write( gcode )

	@pyqtSlot()
	def save_settings( self ):
		file_name, file_type = QFileDialog.getSaveFileName( self, 'Save Settings', filter="JSON (*.json)" )
		if file_name:
			settings = self.slicer_settings.get_all_attributes()
			with open( file_name, 'w' ) as settings_file:
				json.dump( settings, settings_file )

	@pyqtSlot()
	def load_settings( self ):
		file_name, file_type = QFileDialog.getOpenFileName( self, 'Load Settings', filter="JSON (*.json)" )
		if file_name:
			with open( file_name, 'r' ) as settings_file:
				try:
					settings = json.load( settings_file )
					self.slicer_settings.set_all_attributes( settings )
				except JSONDecodeError as e:
					error_popup( e, 'Invalid Settings File, Sorry :(' )

	def show_source_image( self ):
		settings = self.slicer_settings.get_all_attributes()
		pixmap = QPixmap( self.source_image_file_name )

		self.source_image_label.pixmap = pixmap
		self.result_image_label.pixmap = SlicerStyles.process_image( pixmap, settings )
		self.repaint()
