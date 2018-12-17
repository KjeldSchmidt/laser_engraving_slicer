from typing import Dict, Tuple

from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout, QLineEdit


class SlicerSettingsWindow( QMainWindow ):
	def __init__( self, parent ):
		super().__init__( parent )
		self.setWindowTitle( 'Slicer Settings' )
		self.attributes = self.get_empty_attributes()

		central_form_widget = QWidget()
		self.setCentralWidget( central_form_widget )
		self.form_layout = QFormLayout( central_form_widget )

		for key, value in self.attributes.items():
			value[ 6 ]( value[ 3 ], value[ 1 ] )
			self.form_layout.addRow( value[ 0 ], value[ 3 ] )

	def get_all_attributes( self ) -> Dict:
		settings = {
			key: val[ 2 ]( val[ 4 ]( val[ 3 ] ) ) for key, val in self.attributes.items()
		}
		return settings

	def set_all_attributes( self, settings: Dict ):
		for key, value in settings.items():
			current = list( self.attributes[ key ] )
			current[ 1 ] = current[ 5 ]( value )
			current[ 6 ]( current[ 3 ], current[ 1 ] )
			self.attributes[ key ] = tuple( current )

	def get_empty_attributes( self ):
		# Name, Form Name, Default Value, Input to Use Conversion, Input Type, Value Retrieval, Use to Input Conversion, Value Setter
		attributes = {
			'x_init': float_attribute( 'Bed Corner X', 0.00 ),
			'y_init': float_attribute( 'Bed Corner Y', 0.00 ),
			'focal_length': float_attribute( 'Laser Focal Length', 5.00 ),
			'plate_height': float_attribute( 'Height of engraving plate', 1.00 ),
			'move_speed': float_attribute( 'Move speed in mm/s', 0.5 )
		}
		return attributes


def float_attribute( desc: str, default: float = 0.0 ) -> Tuple:
	return desc, str( default ), float, QLineEdit(), get_text, str, set_text


def get_text( qle: QLineEdit ) -> str:
	return qle.text()


def set_text( qle: QLineEdit, text: str ):
	qle.setText( text )
