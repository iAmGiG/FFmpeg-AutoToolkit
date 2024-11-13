import subprocess
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class AudioProcessor:
    def __init__(self, ffmpeg_command):
        self.ffmpeg_command = ffmpeg_command

    def list_audio_tracks(self, input_file):
        logger.info(f"Listing audio tracks in {input_file}")
        cmd = [self.ffmpeg_command, '-i', input_file]
        result = subprocess.run(
            cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        stderr = result.stderr
        tracks = []
        for line in stderr.splitlines():
            if 'Stream' in line and 'Audio' in line:
                tracks.append(line.strip())
        logger.debug(f"Found audio tracks: {tracks}")
        return tracks

    def consolidate_audio_tracks(self, input_file, output_file):
        logger.info(
            f"Consolidating audio tracks from {input_file} to {output_file}")
        # Build the FFmpeg command to merge audio tracks
        cmd = [
            self.ffmpeg_command,
            '-i', input_file,
            '-filter_complex', '[0:a]amerge=inputs=2[aout]',
            '-map', '0:v',
            '-map', '[aout]',
            '-c:v', 'copy',
            '-c:a', 'aac',
            output_file
        ]
        subprocess.run(cmd, check=True)
        logger.info(f"Audio tracks consolidated into {output_file}")

    def convert_audio_format(self, input_file, output_file, codec='aac', bitrate='192k'):
        logger.info(
            f"Converting {input_file} to {output_file} with codec {codec} and bitrate {bitrate}")
        cmd = [
            self.ffmpeg_command,
            '-i', input_file,
            '-c:a', codec,
            '-b:a', bitrate,
            output_file
        ]
        subprocess.run(cmd, check=True)
        logger.info(f"Audio file converted to {output_file}")
