import unittest

from cmd import get_command
from ctrl import Context


class TestCase(unittest.TestCase):
    def test_cmd_error_exists(self):
        cmd = get_command('error')
        self.assertEqual('error', cmd.name)

    def test_cmd_foobar_does_not_exist(self):
        cmd = get_command('this-command-does-not-exist')
        self.assertIsNone(cmd)
