from typing import Dict, Tuple

from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout, QLineEdit

from FormAttributes import FloatAttribute


def get_empty_attributes():
	# Name, Form Name, Default Value, Input to Use Conversion, Input Type, Value Retrieval, Use to Input Conversion, Value Setter
	attributes = {
		'x_init': FloatAttribute( 'Bed Corner X', 0.00 ),
		'y_init': FloatAttribute( 'Bed Corner Y', 0.00 ),
		'focal_length': FloatAttribute( 'Laser Focal Length', 5.00 ),
		'plate_thickness': FloatAttribute( 'Thickness of engraving plate', 8.5 ),
		'plate_width': FloatAttribute( 'Width in mm on X-axis', 110 ),
		'plate_height': FloatAttribute( 'Height in mm on Y-axis', 110 ),
		'move_speed': FloatAttribute( 'Move speed in mm/s', 0.5 ),
		'laser_pixel_size': FloatAttribute( 'Size of laser pixel in mm', 0.1 ),
	}
	return attributes


class SlicerSettingsWindow( QMainWindow ):
	def __init__( self, parent ):
		super().__init__( parent )
		self.setWindowTitle( 'Slicer Settings' )
		self.attributes = get_empty_attributes()

		central_form_widget = QWidget()
		self.setCentralWidget( central_form_widget )
		self.form_layout = QFormLayout( central_form_widget )

		for key, value in self.attributes.items():
			self.form_layout.addRow( value.description, value.input )

	def get_all_attributes( self ) -> Dict:
		settings = {
			key: val.get_value() for key, val in self.attributes.items()
		}
		return settings

	def set_all_attributes( self, settings: Dict ):
		for key, value in settings.items():
			current = self.attributes[ key ]
			current.set_value( value )
