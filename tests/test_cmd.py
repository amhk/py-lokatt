import shlex
import unittest

from cmd import get_command


class TestCase(unittest.TestCase):
    def test_cmd_error_exists(self):
        cmd = get_command('error')
        self.assertIsNotNone(cmd)
        self.assertEqual('error', cmd.name)

    def test_cmd_foobar_does_not_exist(self):
        cmd = get_command('this-command-does-not-exist')
        self.assertIsNone(cmd)

    def test_goto_line(self):
        cmd = get_command('goto-line')
        self.assertIsNotNone(cmd)
        self.assertEqual('goto-line', cmd.name)
