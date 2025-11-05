import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QProgressBar
from PyQt6.QtGui import QPixmap, QColor, QImage
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Detection People")
        self.setMinimumSize(640, 480)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central.setLayout(layout)
        
        self.open_weights_btn = QPushButton("Open weights")
        self.open_weights_btn.setFixedWidth(150)
        self.open_weights_btn.clicked.connect(self.open_weights)
        layout.addWidget(self.open_weights_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.open_video_btn = QPushButton("Open video")
        self.open_video_btn.setFixedWidth(150)
        self.open_video_btn.setEnabled(False)
        self.open_video_btn.clicked.connect(self.open_video)
        layout.addWidget(self.open_video_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        """
        self.preview = QLabel()
        image = QImage(200, 200, QImage.Format.Format_RGB32)
        image.fill(QColor("black"))
        pixmap = QPixmap.fromImage(image)
        self.preview.setPixmap(pixmap)
        self.preview.show()
        layout.addWidget(self.preview)
        """

        self.preview = QLabel()
        pixmap = QPixmap(200, 200)
        pixmap.fill(QColor("black"))
        self.preview.setPixmap(pixmap)
        self.preview.show()
        layout.addWidget(self.preview, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setMinimumWidth(400)
        layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.save_video_btn = QPushButton("Save video")
        self.save_video_btn.setFixedWidth(150)
        self.save_video_btn.setEnabled(False)
        self.save_video_btn.clicked.connect(self.save_video)
        layout.addWidget(self.save_video_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    def open_weights(self):
        path = QFileDialog.getOpenFileName(self, "Open File")[0]

    def open_video(self):
        path = QFileDialog.getOpenFileName(self, "Open File")[0]
    
    def save_video(self):
        path = QFileDialog.getSaveFileName(self, "Save File")[0]

if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())