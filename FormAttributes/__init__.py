from typing import Any, List, Iterable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QComboBox
from abc import ABC, abstractmethod

from ErrorPopup import error_popup


class SettingsAttribute( ABC ):
	@abstractmethod
	def __init__( self, description: str, default: Any ):
		"""
		Creates an Attribute for a form.

		:param description: Label text in GUI
		:param default: Default initial value
		"""
		self.description = description
		self.value = default

	@abstractmethod
	def get_text_value( self ) -> str:
		"""
		Get the value as text

		:return: String representation of the current value
		"""

	@abstractmethod
	def get_value( self ) -> Any:
		"""
		Get actual value as correct type

		:return: Actual value
		"""

	@abstractmethod
	def set_value( self, new_value: Any ):
		"""
		Set value from internally used data type

		:param new_value: Value to set
		"""


class FloatAttribute( SettingsAttribute ):
	def __init__( self, description: str, default: float ):
		super().__init__( description, default )

		self.input = QLineEdit()
		self.input.setText( str( default ) )

	def get_text_value( self ) -> str:
		return str( self.input.text() )

	def get_value( self ) -> float:
		return float( self.input.text() )

	def set_value( self, new_value: float ):
		self.input.setText( str( new_value ) )


class BoolAttribute( SettingsAttribute ):
	def __init__( self, description: str, default: float ):
		super().__init__( description, default )

		self.input = QCheckBox()
		self.input.setCheckState( Qt.Checked if default else Qt.Unchecked )

	def get_text_value( self ) -> str:
		return str( self.input.checkState() )

	def get_value( self ) -> bool:
		return self.input.checkState() == Qt.Checked

	def set_value( self, new_value: bool ):
		self.input.setCheckState( Qt.Checked if new_value else Qt.Unchecked )


class ComboAttribute( SettingsAttribute ):
	def __init__( self, description: str, options: Iterable[ str ], default: str = None ):
		options = list( options )
		assert default in options or default is None, 'Default value is not in the options!'

		super().__init__( description, default )

		self.input = QComboBox()
		self.input.addItems( options )

		if default is not None:
			self.input.setCurrentIndex( options.index( default ) )

	def get_text_value( self ) -> str:
		return str( self.input.currentText() )

	def get_value( self ) -> int:
		return self.input.currentIndex()

	def set_value( self, new_value: int ):
		self.input.setCurrentIndex( new_value )
