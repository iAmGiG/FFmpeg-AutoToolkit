import subprocess
import logging

logger = logging.getLogger(__name__)


class VideoProcessor:
    def __init__(self, ffmpeg_command):
        self.ffmpeg_command = ffmpeg_command

    def convert_video_format(self, input_file, output_file, video_codec='libx264', audio_codec='aac', preset='medium'):
        logger.info(
            f"Converting {input_file} to {output_file} with video codec {video_codec} and audio codec {audio_codec}")
        cmd = [
            self.ffmpeg_command,
            '-i', input_file,
            '-c:v', video_codec,
            '-preset', preset,
            '-c:a', audio_codec,
            output_file
        ]
        subprocess.run(cmd, check=True)
        logger.info(f"Video file converted to {output_file}")

    def edit_metadata(self, input_file, output_file, metadata):
        logger.info(
            f"Editing metadata for {input_file} and saving to {output_file}")
        cmd = [self.ffmpeg_command, '-i', input_file]
        for key, value in metadata.items():
            cmd.extend(['-metadata', f'{key}={value}'])
        cmd.append(output_file)
        subprocess.run(cmd, check=True)
        logger.info(f"Metadata updated in {output_file}")
