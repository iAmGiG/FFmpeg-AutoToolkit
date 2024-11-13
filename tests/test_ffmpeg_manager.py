import unittest
from ffmpeg_manager import FFmpegManager


class TestFFmpegManager(unittest.TestCase):
    def setUp(self):
        self.manager = FFmpegManager()

    def test_find_ffmpeg(self):
        path = self.manager.find_ffmpeg()
        self.assertTrue(isinstance(path, str) or path is None)

    def test_set_custom_ffmpeg_path_invalid(self):
        result = self.manager.set_custom_ffmpeg_path('/invalid/path')
        self.assertFalse(result)

    def test_set_custom_ffmpeg_path_valid(self):
        # Assuming ffmpeg is in PATH, get its path
        ffmpeg_path = self.manager.find_ffmpeg()
        if ffmpeg_path and ffmpeg_path != 'ffmpeg':
            result = self.manager.set_custom_ffmpeg_path(ffmpeg_path)
            self.assertTrue(result)
        else:
            self.skipTest("FFmpeg not found in system PATH for testing.")


if __name__ == '__main__':
    unittest.main()
