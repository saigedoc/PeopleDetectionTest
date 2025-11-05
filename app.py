import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QProgressBar, QMessageBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from video import video_process

class Worker(QThread):
    def __init__(self, pathin, pathout, model_path, progress_bar, errors):
        super().__init__()
        self.pathin = pathin
        self.pathout = pathout
        self.model_path = model_path
        self.progress_bar = progress_bar
        self.errors = errors

    def run(self):
        try:
            video_process(self.pathin, self.pathout, self.model_path, self.progress_bar)
        except Exception as e:
            self.errors.append(e)

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
        self.open_video_btn.clicked.connect(self.open_video)
        layout.addWidget(self.open_video_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.save_video_btn = QPushButton("Choose save path")
        self.save_video_btn.setFixedWidth(150)
        self.save_video_btn.clicked.connect(self.save_video)
        layout.addWidget(self.save_video_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setMinimumWidth(400)
        layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.start_btn = QPushButton("Process video")
        self.start_btn.setFixedWidth(150)
        self.start_btn.clicked.connect(self.start)
        layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.weights_path = None
        self.video_path = None
        self.video_out_path = None

    def open_weights(self):
        self.weights_path = QFileDialog.getOpenFileName(self, "Open File", filter="Веса (*.pt);; Все файлы (*)")[0]

    def open_video(self):
        self.video_path = QFileDialog.getOpenFileName(self, "Open File", filter="Видео (*.mp4);; Все файлы (*)")[0]
    
    def save_video(self):
        self.video_out_path = QFileDialog.getSaveFileName(self, "Save File", filter="Видео (*.mp4);; Все файлы (*)")[0]
    
    def send_message(self, title, text):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def start(self):
        if (not self.weights_path):
            self.send_message("People Detection ERROR", "Отсутствует путь весов")
        if (not self.video_path):
            self.send_message("People Detection ERROR", "Отсутствует путь для открытия видео")
        if (not self.video_out_path):
            self.send_message("People Detection ERROR", "Отсутствует путь для сохранения видео")
        if self.weights_path and self.video_path and self.video_out_path:
            self.start_btn.setEnabled(False)
            self.errors = []
            self.worker = Worker(self.video_path, self.video_out_path, self.weights_path, self.progress, self.errors)
            #self.worker.error.connect(lambda text: self.send_message("People Detection ERROR", text))
            self.worker.finished.connect(self.finish)
            self.worker.start()
    
    def finish(self):
        if self.errors != []:
            for e in self.errors:
                self.send_message("People Detection ERROR", str(e))
        else:  
            self.start_btn.setEnabled(True)
            self.send_message("People Detection comlete", f"Обработка видео завершено, оно сохранено по пути: {self.video_out_path}.")

if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())