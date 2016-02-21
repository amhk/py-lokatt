import os
import unittest

from adb import Device, LogcatEntry


class TestCase(unittest.TestCase):
    def setUp(self):
        root = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(root, 'nexus-5-android-5.1-regular-usage.bin')
        self._dev = Device(path)
        self._gen = self._dev.entries()

    def test_fields_first_entry(self):
        logcat = self._gen.next()

        self.assertEqual(int, type(logcat.pid))
        self.assertEqual(189, logcat.pid)

        self.assertEqual(int, type(logcat.tid))
        self.assertEqual(845, logcat.tid)

        self.assertEqual(int, type(logcat.sec))
        self.assertEqual(1427870072, logcat.sec)

        self.assertEqual(int, type(logcat.nsec))
        self.assertEqual(978108327, logcat.nsec)

        self.assertEqual(int, type(logcat.level))
        self.assertEqual(3, logcat.level)

        self.assertEqual(str, type(logcat.tag))
        self.assertEqual('audio_hw_primary', logcat.tag)

        a = 'disable_audio_route: reset and update mixer path: low-latency-playback'
        self.assertEqual(str, type(logcat.text))
        self.assertEqual(a, logcat.text)

    def test_entries_are_different(self):
        logcat = self._gen.next()
        a = logcat.text
        logcat = self._gen.next()
        b = logcat.text

        self.assertNotEqual(a, b)

    def test_invalid_path(self):
        with self.assertRaises(Exception):
            dev = Device('this-path-does-not-exist')
