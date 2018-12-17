from typing import Dict

from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5.QtGui import QPixmap, QImage, QPainter


def process_image( pixmap: QPixmap, settings: Dict ) -> QPixmap:
	image = pixmap.toImage()
	image = binarize( image )
	image = to_cross_squares( image, settings )
	return QPixmap.fromImage( image )


def binarize( image: QImage ) -> QImage:
	image = image.convertToFormat( QImage.Format_Mono, Qt.ThresholdDither )
	return image


def to_cross_squares( image: QImage, settings: Dict ) -> QImage:
	source_image = image.copy()
	source_image_width = source_image.width()
	source_image_height = source_image.height()

	if source_image_width == 0 or source_image_height == 0:
		return source_image

	source_image_ratio = source_image_height / source_image_width

	pixel_box_size = settings[ 'pixel_box_size' ]
	plate_width = settings[ 'plate_width' ]
	plate_height = settings[ 'plate_height' ]

	result_image_width = int( plate_width / pixel_box_size )
	result_image_height = int( plate_height / pixel_box_size )
	result_image_ratio = result_image_height / result_image_width

	result = QImage( result_image_width, result_image_height, QImage.Format_Mono )

	if source_image_ratio < result_image_ratio:
		source_image = source_image.scaledToWidth( result_image_width )
		position = QPoint( 0, result_image_height / 2 - source_image.height() / 2 )
	else:
		source_image = source_image.scaledToHeight( result_image_height, Qt.FastTransformation )
		position = QPoint( result_image_width / 2 - source_image.width() / 2, 0 )

	result.fill( Qt.black )

	painter: QPainter = QPainter( result )
	painter.drawImage( position, source_image )
	painter.end()

	return result
