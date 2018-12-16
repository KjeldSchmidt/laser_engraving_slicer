from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter
from PyQt5.QtWidgets import QWidget


class ImageLabel( QWidget ):
	def __init__( self ):
		super().__init__()
		self._pixmap: QPixmap = None

	@property
	def pixmap( self ):
		return self._pixmap

	@pixmap.setter
	def pixmap( self, pixmap: QPixmap ):
		self._pixmap = pixmap

	def paintEvent( self, paint_event: QPaintEvent ):
		super().paintEvent( paint_event )

		if self._pixmap is None:
			return

		painter = QPainter( self )
		painter.setRenderHint( QPainter.Antialiasing )

		pix_size: QSize = self._pixmap.size()
		pix_size.scale( paint_event.rect().size(), Qt.KeepAspectRatio )

		scaled_pix: QPixmap = self._pixmap.scaled( pix_size, Qt.KeepAspectRatio, Qt.SmoothTransformation )
		painter.drawPixmap( QPoint(), scaled_pix )
