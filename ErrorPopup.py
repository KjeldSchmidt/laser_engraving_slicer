from PyQt5.QtWidgets import QMessageBox


def error_popup( e: Exception, message: str ):
	box = QMessageBox()
	box.setText( message )
	box.setDetailedText( str( e ) )
	box.exec_()
