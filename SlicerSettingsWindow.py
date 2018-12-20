from typing import Dict, Tuple

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout, QLineEdit

from FormAttributes import FloatAttribute, BoolAttribute, ComboAttribute


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
		'pixel_box_size': FloatAttribute( 'Size of black box (what?) in mm', 1 ),
		'move_z_axis': BoolAttribute( 'Home and move Z axis', True ),
		'burn_style': ComboAttribute( 'Style of burn', [ 'B/W Crosses', 'Parallel Lines' ] ),
		'lines_direction': ComboAttribute( 'Direction of burn', [ 'Vertical', 'Horizontal', 'Diagonal' ] ),
	}
	return attributes


class SlicerSettingsWindow( QMainWindow ):
	close_signal = pyqtSignal()

	def __init__( self, parent, show_image_slot ):
		super().__init__( parent )
		self.setWindowTitle( 'Slicer Settings' )
		self.attributes = get_empty_attributes()
		self.close_signal.connect( show_image_slot )

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

	def closeEvent( self, close_event ):
		super().closeEvent( close_event )
		self.close_signal.emit()
