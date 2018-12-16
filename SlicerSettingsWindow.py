from typing import Dict

from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout, QLineEdit


class SlicerSettingsWindow( QMainWindow ):
	def __init__( self, parent ):
		super().__init__( parent )
		self.setWindowTitle( 'Slicer Settings' )

		central_form_widget = QWidget()
		self.setCentralWidget( central_form_widget )
		self.form_layout = QFormLayout( central_form_widget )

		self.x_init = QLineEdit( '0.00' )
		self.y_init = QLineEdit( '0.00' )
		self.z_init = QLineEdit( '0.00' )

		self.form_layout.addRow( 'Bed Corner X', self.x_init )
		self.form_layout.addRow( 'Bed Corner Y', self.y_init )
		self.form_layout.addRow( 'Z height', self.z_init )

	def get_all_attributes( self ) -> Dict:
		settings = {
			'x_init': float( self.x_init.text() ),
			'y_init': float( self.y_init.text() ),
			'z_init': float( self.z_init.text() ),
		}
		return settings
