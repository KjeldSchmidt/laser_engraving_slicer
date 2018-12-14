import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

root = QWidget()
root.resize(400, 600)
root.setWindowTitle('Laser Engraving Slicer')
root.show()

sys.exit(app.exec_())
