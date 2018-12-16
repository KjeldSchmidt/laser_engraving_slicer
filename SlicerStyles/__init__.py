from PyQt5.QtGui import QPixmap, QImage


def process_image( pixmap: QPixmap ) -> QPixmap:
	image = pixmap.toImage()
	image = binarize( image )
	return QPixmap.fromImage( image )


def binarize( image: QImage ) -> QImage:
	image = image.convertToFormat( QImage.Format_Mono )
	return image
