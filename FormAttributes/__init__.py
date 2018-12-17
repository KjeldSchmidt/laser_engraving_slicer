from PyQt5.QtWidgets import QLineEdit

from ErrorPopup import error_popup


class FloatAttribute:
	def __init__( self, description: str, default: float ):
		self.input = QLineEdit()
		self.input.setText( str( default ) )
		self.description = description
		self.value = default

	def get_text_value( self ) -> str:
		return str( self.input.text() )

	def set_value_from_text( self, text: str ):
		try:
			self.value = float( text )
			self.input.setText( text )
		except ValueError as e:
			error_popup( e, 'Invalid Value entered as floating point number' )

	def get_value( self ) -> float:
		return float( self.input.text() )

	def set_value( self, new_value: float ):
		self.value = new_value
		self.input.setText( str( new_value ) )
