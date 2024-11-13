import subprocess
import requests
import platform
import zipfile
import tarfile
from pathlib import Path
import platformdirs
import logging
import configparser

logger = logging.getLogger(__name__)


class FFmpegManager:
    def __init__(self):
        self.config_file = Path(
            platformdirs.user_config_dir()) / "ffmpeg_auto_toolkit" / "config.ini"
        self.ffmpeg_path = None
        self.config = configparser.ConfigParser()
        self.load_config()
        if not self.ffmpeg_path:
            self.ffmpeg_path = self.find_ffmpeg()

    def load_config(self):
        if self.config_file.exists():
            self.config.read(self.config_file)
            self.ffmpeg_path = self.config.get('FFmpeg', 'path', fallback=None)
        else:
            self.config['FFmpeg'] = {}
            self.save_config()

    def save_config(self):
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def find_ffmpeg(self):
        logger.info("Checking if FFmpeg is installed.")
        try:
            subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=True)
            logger.info("FFmpeg is available in the system PATH.")
            return 'ffmpeg'
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("FFmpeg not found in system PATH.")
            return None

    def download_ffmpeg(self):
        system = platform.system()
        arch = platform.machine()
        logger.info(f"Downloading FFmpeg for {system} {arch}.")
        download_url = self.get_download_url(system, arch)
        if not download_url:
            logger.error("Unsupported platform for automatic FFmpeg download.")
            return False

        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            ffmpeg_dir = Path(platformdirs.user_data_dir()) / \
                "ffmpeg_auto_toolkit" / "ffmpeg"
            ffmpeg_dir.mkdir(parents=True, exist_ok=True)
            archive_path = ffmpeg_dir / download_url.split('/')[-1]

            with open(archive_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info(f"Downloaded FFmpeg to {archive_path}.")

            self.extract_ffmpeg(archive_path, ffmpeg_dir)
            self.ffmpeg_path = str(ffmpeg_dir / 'ffmpeg')
            self.config['FFmpeg']['path'] = self.ffmpeg_path
            self.save_config()
            return True
        else:
            logger.error("Failed to download FFmpeg.")
            return False

    def get_download_url(self, system, arch):
        if system == 'Windows':
            return 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
        elif system == 'Linux':
            return 'https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz'
        else:
            return None

    def extract_ffmpeg(self, archive_path, ffmpeg_dir):
        if archive_path.suffixes[-1] == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(ffmpeg_dir)
        elif archive_path.suffixes[-1] in ['.tar', '.gz', '.xz']:
            with tarfile.open(archive_path, 'r:*') as tar_ref:
                tar_ref.extractall(ffmpeg_dir)
        else:
            logger.error("Unsupported archive format for FFmpeg.")
            return

        # Set executable permissions on Linux
        if platform.system() == 'Linux':
            ffmpeg_bin = ffmpeg_dir / 'ffmpeg'
            ffmpeg_bin.chmod(ffmpeg_bin.stat().st_mode | 0o111)

    def set_custom_ffmpeg_path(self, path):
        if Path(path).exists():
            self.ffmpeg_path = path
            self.config['FFmpeg']['path'] = self.ffmpeg_path
            self.save_config()
            logger.info(f"Set custom FFmpeg path: {self.ffmpeg_path}")
            return True
        else:
            logger.error("Provided FFmpeg path does not exist.")
            return False

    def get_ffmpeg_command(self):
        return self.ffmpeg_path if self.ffmpeg_path else 'ffmpeg'
