import sys
import logging
from absl import app, flags
from ffmpeg_manager import FFmpegManager
from audio_processor import AudioProcessor
from video_processor import VideoProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FLAGS = flags.FLAGS

# Define command-line flags
flags.DEFINE_string(
    'action', None, 'Action to perform: check_ffmpeg, download_ffmpeg, set_ffmpeg_path, consolidate_audio, convert_audio, convert_video, edit_metadata')
flags.DEFINE_string('input', None, 'Input file path')
flags.DEFINE_string('output', None, 'Output file path')
flags.DEFINE_string('ffmpeg_path', None, 'Custom FFmpeg path')
flags.DEFINE_boolean('verbose', False, 'Enable verbose logging')
flags.DEFINE_string('codec', 'aac', 'Audio codec for conversion')
flags.DEFINE_string('bitrate', '192k', 'Audio bitrate for conversion')
flags.DEFINE_string('video_codec', 'libx264', 'Video codec for conversion')
flags.DEFINE_string('preset', 'medium', 'Preset for video conversion')
flags.DEFINE_string(
    'metadata', None, 'Metadata in key=value format, separated by commas')


def main(argv):
    if FLAGS.verbose:
        logger.setLevel(logging.DEBUG)

    ffmpeg_manager = FFmpegManager()

    if FLAGS.action == 'check_ffmpeg':
        if ffmpeg_manager.find_ffmpeg():
            logger.info("FFmpeg is installed and accessible.")
        else:
            logger.info("FFmpeg is not installed.")

    elif FLAGS.action == 'download_ffmpeg':
        success = ffmpeg_manager.download_ffmpeg()
        if success:
            logger.info("FFmpeg downloaded and set up successfully.")
        else:
            logger.error("Failed to download FFmpeg.")

    elif FLAGS.action == 'set_ffmpeg_path':
        if FLAGS.ffmpeg_path:
            success = ffmpeg_manager.set_custom_ffmpeg_path(FLAGS.ffmpeg_path)
            if success:
                logger.info("Custom FFmpeg path set.")
            else:
                logger.error("Failed to set custom FFmpeg path.")
        else:
            logger.error("Please provide a path using --ffmpeg_path")

    else:
        ffmpeg_command = ffmpeg_manager.get_ffmpeg_command()
        if not ffmpeg_command:
            logger.error(
                "FFmpeg is not available. Please run --action=download_ffmpeg")
            sys.exit(1)

        if FLAGS.action == 'consolidate_audio':
            if FLAGS.input and FLAGS.output:
                audio_processor = AudioProcessor(ffmpeg_command)
                audio_processor.consolidate_audio_tracks(
                    FLAGS.input, FLAGS.output)
            else:
                logger.error("Please provide --input and --output file paths.")

        elif FLAGS.action == 'convert_audio':
            if FLAGS.input and FLAGS.output:
                audio_processor = AudioProcessor(ffmpeg_command)
                audio_processor.convert_audio_format(
                    FLAGS.input,
                    FLAGS.output,
                    codec=FLAGS.codec,
                    bitrate=FLAGS.bitrate
                )
            else:
                logger.error("Please provide --input and --output file paths.")

        elif FLAGS.action == 'convert_video':
            if FLAGS.input and FLAGS.output:
                video_processor = VideoProcessor(ffmpeg_command)
                video_processor.convert_video_format(
                    FLAGS.input,
                    FLAGS.output,
                    video_codec=FLAGS.video_codec,
                    audio_codec=FLAGS.codec,
                    preset=FLAGS.preset
                )
            else:
                logger.error("Please provide --input and --output file paths.")

        elif FLAGS.action == 'edit_metadata':
            if FLAGS.input and FLAGS.output and FLAGS.metadata:
                video_processor = VideoProcessor(ffmpeg_command)
                metadata_dict = dict(item.split('=')
                                     for item in FLAGS.metadata.split(','))
                video_processor.edit_metadata(
                    FLAGS.input,
                    FLAGS.output,
                    metadata_dict
                )
            else:
                logger.error(
                    "Please provide --input, --output, and --metadata.")

        else:
            logger.error("Invalid action specified.")


if __name__ == '__main__':
    app.run(main)
