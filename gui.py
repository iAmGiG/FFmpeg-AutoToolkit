import sys
import logging
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox, QAction, QLabel, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from ffmpeg_manager import FFmpegManager
from audio_processor import AudioProcessor
from video_processor import VideoProcessor

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FFmpeg AutoToolkit")
        self.ffmpeg_manager = FFmpegManager()
        self.init_ui()

    def init_ui(self):
        # Menu actions
        self.create_actions()
        self.create_menus()

        # Status bar
        self.statusBar().showMessage("Ready")
        self.progress_bar = QProgressBar()
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.setVisible(False)

        # Central widget
        label = QLabel("Welcome to FFmpeg AutoToolkit!", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)

    def create_actions(self):
        self.check_ffmpeg_action = QAction("Check FFmpeg", self)
        self.check_ffmpeg_action.triggered.connect(self.check_ffmpeg)

        self.download_ffmpeg_action = QAction("Download FFmpeg", self)
        self.download_ffmpeg_action.triggered.connect(self.download_ffmpeg)

        self.consolidate_audio_action = QAction("Consolidate Audio", self)
        self.consolidate_audio_action.triggered.connect(self.consolidate_audio)

        self.convert_video_action = QAction("Convert Video", self)
        self.convert_video_action.triggered.connect(self.convert_video)

        self.set_ffmpeg_path_action = QAction("Set FFmpeg Path", self)
        self.set_ffmpeg_path_action.triggered.connect(self.set_ffmpeg_path)

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)

    def create_menus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.exit_action)

        ffmpeg_menu = menubar.addMenu("FFmpeg")
        ffmpeg_menu.addAction(self.check_ffmpeg_action)
        ffmpeg_menu.addAction(self.download_ffmpeg_action)
        ffmpeg_menu.addAction(self.set_ffmpeg_path_action)

        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction(self.consolidate_audio_action)
        tools_menu.addAction(self.convert_video_action)

    def check_ffmpeg(self):
        if self.ffmpeg_manager.find_ffmpeg():
            QMessageBox.information(
                self, "FFmpeg Check", "FFmpeg is installed and accessible.")
        else:
            QMessageBox.warning(self, "FFmpeg Check",
                                "FFmpeg is not installed.")

    def download_ffmpeg(self):
        self.statusBar().showMessage("Downloading FFmpeg...")
        self.progress_bar.setVisible(True)
        # Implement download progress and threading if needed
        success = self.ffmpeg_manager.download_ffmpeg()
        self.progress_bar.setVisible(False)
        if success:
            QMessageBox.information(
                self, "Download FFmpeg", "FFmpeg downloaded successfully.")
        else:
            QMessageBox.error(self, "Download FFmpeg",
                              "Failed to download FFmpeg.")
        self.statusBar().showMessage("Ready")

    def set_ffmpeg_path(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select FFmpeg Executable")
        if path:
            success = self.ffmpeg_manager.set_custom_ffmpeg_path(path)
            if success:
                QMessageBox.information(
                    self, "Set FFmpeg Path", "FFmpeg path set successfully.")
            else:
                QMessageBox.error(self, "Set FFmpeg Path",
                                  "Failed to set FFmpeg path.")

    def consolidate_audio(self):
        input_file, _ = QFileDialog.getOpenFileName(
            self, "Select Input Video File")
        if input_file:
            output_file, _ = QFileDialog.getSaveFileName(
                self, "Select Output Video File")
            if output_file:
                self.statusBar().showMessage("Consolidating audio tracks...")
                ffmpeg_command = self.ffmpeg_manager.get_ffmpeg_command()
                audio_processor = AudioProcessor(ffmpeg_command)
                try:
                    audio_processor.consolidate_audio_tracks(
                        input_file, output_file)
                    QMessageBox.information(
                        self, "Consolidate Audio", "Audio tracks consolidated successfully.")
                except Exception as e:
                    QMessageBox.critical(
                        self, "Consolidate Audio", f"An error occurred: {str(e)}")
                self.statusBar().showMessage("Ready")

    def convert_video(self):
        input_file, _ = QFileDialog.getOpenFileName(
            self, "Select Input Video File")
        if input_file:
            output_file, _ = QFileDialog.getSaveFileName(
                self, "Select Output Video File")
            if output_file:
                self.statusBar().showMessage("Converting video...")
                ffmpeg_command = self.ffmpeg_manager.get_ffmpeg_command()
                video_processor = VideoProcessor(ffmpeg_command)
                try:
                    video_processor.convert_video_format(
                        input_file, output_file)
                    QMessageBox.information(
                        self, "Convert Video", "Video converted successfully.")
                except Exception as e:
                    QMessageBox.critical(
                        self, "Convert Video", f"An error occurred: {str(e)}")
                self.statusBar().showMessage("Ready")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
