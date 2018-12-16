from PyQt5.QtWidgets import QMainWindow


class SlicerSettingsWindow( QMainWindow ):
	def __init__( self, parent ):
		super().__init__( parent )
		self.setWindowTitle( 'Slicer Settings' )
